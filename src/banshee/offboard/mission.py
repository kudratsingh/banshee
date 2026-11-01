"""ROS 2 mission node: takeoff, route and land through the offboard velocity interface. SITL only.

Runs inside the VM, with ROS 2 and ``px4_msgs`` sourced. The heartbeat and the setpoint stream are
separate, and the planner stamps its own setpoints, so a stalled planner goes stale at the gate
while the heartbeat continues. The gate's verdict then latches a response (``response.py``). Each
tick logs one JSON line to ``steps.jsonl``. It never connects to hardware, and it stops at a wall
clock limit. With ``--case`` it runs one fault case, on this same path (``banshee.faults``).
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import IO, Any

import rclpy
from px4_msgs.msg import (
    FailsafeFlags,
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleCommand,
    VehicleOdometry,
    VehicleStatus,
)
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

from ..faults.injection import Injection, from_case, load_case
from ..freshness import GateInputs
from .frames import (
    Vec3,
    enu_to_ned,
    ned_to_enu,
    yaw_enu_from_ned,
    yaw_ned_from_quaternion,
    yaw_rate_flu_to_frd,
)
from .gate import decide, load_frozen
from .guidance import RouteFollower, load_route
from .response import NAV_OFFBOARD, TARGET_NAV, Latch, respond

TICK_S = 0.05
STREAM_BEFORE_SWITCH_S = 1.5
SETTLE_SPEED_M_S = 0.2
SETTLE_MAX_S = 10.0
ABORT_OBSERVE_S = 30.0
# EKF2 resets routinely on the way up, at about 1.5 m, with no real jump. Only a jump counts.
RESET_JUMP_M = 0.5
ARMING_STATE_ARMED = 2
CMD_SET_MODE = 176
CMD_ARM = 400
CMD_LAND = 21
MODE_CUSTOM = 1.0
MODE_OFFBOARD = 6.0
MODE_AUTO = 4.0
SUB_MODE_LOITER = 3.0


class Mission(Node):  # type: ignore[misc]
    """One flight: wait for the estimator, stream, switch to offboard, arm, fly the route, land."""

    def __init__(self, args: argparse.Namespace, log: IO[str]) -> None:
        super().__init__("banshee_mission")
        self.bounds, self.limits = load_frozen(Path(args.evals))
        self.fault = (
            from_case(load_case(Path(args.matrix), args.case)) if args.case else Injection()
        )
        self.follower = RouteFollower(self.fault.route or load_route(Path(args.route)))
        self.out = Path(args.out)
        self.deadline_ns = time.monotonic_ns() + int(args.timeout_s * 1e9)
        self.log = log
        self.phase = "wait_estimator"
        self.phase_start_ns = time.monotonic_ns()
        self.last_command_ns = 0
        self.odom: dict[str, Any] | None = None
        self.px4_offset_ns: int | None = None
        self.px4_us = 0
        self.local_position_valid = False
        self.nav_state = -1
        self.arming_state = -1
        self.was_armed = False
        self.finished = False
        self.result = "timeout"
        self.request: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
        self.setpoint_ns: int | None = None
        self.sensor_ns: int | None = None
        self.latch: Latch = "none"
        self.reached_target = False
        self.latch_ns: int | None = None
        self.waypoint_passed_ns: int | None = None
        self.trigger_ns: int | None = None
        self.reset_jump = False
        out = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self.create_subscription(VehicleOdometry, "/fmu/out/vehicle_odometry", self.on_odom, out)
        self.create_subscription(VehicleStatus, "/fmu/out/vehicle_status_v1", self.on_status, out)
        self.create_subscription(FailsafeFlags, "/fmu/out/failsafe_flags", self.on_flags, out)
        self.mode_pub = self.create_publisher(
            OffboardControlMode, "/fmu/in/offboard_control_mode", out
        )
        self.setpoint_pub = self.create_publisher(
            TrajectorySetpoint, "/fmu/in/trajectory_setpoint", out
        )
        self.command_pub = self.create_publisher(VehicleCommand, "/fmu/in/vehicle_command", out)
        self.create_timer(TICK_S, self.tick)

    def since_trigger(self, now: int) -> float | None:
        return None if self.trigger_ns is None else (now - self.trigger_ns) / 1e9

    def on_odom(self, msg: Any) -> None:
        received = time.monotonic_ns()
        self.px4_us = int(msg.timestamp_sample)
        # A sample in any other frame is dropped, so the state goes stale and the gate holds.
        if msg.pose_frame != msg.POSE_FRAME_NED or msg.velocity_frame != msg.VELOCITY_FRAME_NED:
            return
        if self.fault.freeze_estimator.active(self.since_trigger(received)):
            return
        if not self.fault.freeze_sensor.active(self.since_trigger(received)):
            self.sensor_ns = received
        px4_ns = int(msg.timestamp_sample) * 1000
        offset = received - px4_ns
        # The smallest offset seen keeps a mapped capture time at or before its receipt.
        self.px4_offset_ns = (
            offset if self.px4_offset_ns is None else min(self.px4_offset_ns, offset)
        )
        px, py, pz = (float(v) for v in msg.position)
        vx, vy, vz = (float(v) for v in msg.velocity)
        position = ned_to_enu((px, py, pz))
        velocity = ned_to_enu((vx, vy, vz))
        w, x, y, z = (float(v) for v in msg.q)
        reset_counter = int(msg.reset_counter)
        if self.trigger_ns is not None and self.fault.position_jump_m is not None:
            jump = self.fault.position_jump_m
            position = (position[0] + jump[0], position[1] + jump[1], position[2] + jump[2])
            reset_counter += 1
        before = self.odom
        if before is not None and before["reset_counter"] != reset_counter:
            self.reset_jump = self.reset_jump or (
                self.arming_state == ARMING_STATE_ARMED
                and math.dist(before["position"], position) > RESET_JUMP_M
            )
        self.odom = {
            "position": position,
            "velocity": velocity,
            "yaw": yaw_enu_from_ned(yaw_ned_from_quaternion(w, x, y, z)),
            "capture_ns": px4_ns + self.px4_offset_ns,
            "received_ns": received,
            "reset_counter": reset_counter,
        }

    def on_status(self, msg: Any) -> None:
        self.nav_state = int(msg.nav_state)
        self.arming_state = int(msg.arming_state)
        if self.arming_state == ARMING_STATE_ARMED:
            self.was_armed = True

    def on_flags(self, msg: Any) -> None:
        self.local_position_valid = not (msg.local_position_invalid or msg.local_velocity_invalid)

    def command(
        self, command: int, param1: float = 0.0, param2: float = 0.0, param3: float = 0.0
    ) -> None:
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = command
        msg.param1 = param1
        msg.param2 = param2
        msg.param3 = param3
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        self.command_pub.publish(msg)

    def heartbeat(self) -> None:
        msg = OffboardControlMode()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = False
        msg.velocity = True
        self.mode_pub.publish(msg)

    def set_phase(self, phase: str, now: int) -> None:
        self.phase = phase
        self.phase_start_ns = now

    def stop(self, result: str) -> None:
        self.result = result
        self.finished = True

    def maybe_trigger(self, now: int) -> None:
        """Start the case's faults once the aircraft has passed the chosen waypoint and delay."""
        if not self.fault.is_case or self.trigger_ns is not None or self.phase == "stream":
            return
        if self.waypoint_passed_ns is None:
            passed = self.follower.index > self.fault.after_waypoint
            self.waypoint_passed_ns = now if passed else None
            return
        if (now - self.waypoint_passed_ns) / 1e9 >= self.fault.delay_s:
            self.trigger_ns = now
            record = {"px4_us": self.px4_us, "monotonic_ns": now, "phase": self.phase}
            (self.out / "trigger.json").write_text(json.dumps(record) + "\n", encoding="utf-8")

    def plan(self, position: Vec3, velocity: Vec3, now: int) -> None:
        """The planner, stamping what it produces. A frozen planner stamps nothing."""
        since = self.since_trigger(now)
        if self.fault.freeze_planner.active(since):
            return
        elapsed = (now - self.phase_start_ns) / 1e9
        request: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
        if self.phase == "route":
            step = self.follower.step(position)
            if step is None:
                self.set_phase("hover" if self.fault.is_case else "settle", now)
            else:
                request = (*step, 0.0)
        elif self.phase == "settle":
            # Brake at the last waypoint first: Land does not stop where it starts.
            slow = math.hypot(velocity[0], velocity[1]) < SETTLE_SPEED_M_S
            if slow or elapsed >= SETTLE_MAX_S:
                self.set_phase("land", now)
        if since is not None and self.fault.yaw_rate_rad_s:
            request = (request[0], request[1], request[2], self.fault.yaw_rate_rad_s)
        if self.fault.scale != 1.0:
            scale = self.fault.scale
            request = (request[0] * scale, request[1] * scale, request[2] * scale, request[3])
        self.request = request
        self.setpoint_ns = now

    def advance(self, now: int) -> None:
        """Mission steps that command PX4 directly, outside the setpoint stream."""
        elapsed = (now - self.phase_start_ns) / 1e9
        repeat = now - self.last_command_ns > 1_000_000_000
        if self.phase == "wait_estimator" and self.local_position_valid:
            self.set_phase("stream", now)
        elif self.phase == "stream" and elapsed >= STREAM_BEFORE_SWITCH_S:
            if repeat:
                self.command(CMD_SET_MODE, MODE_CUSTOM, MODE_OFFBOARD)
                self.command(CMD_ARM, 1.0)
                self.last_command_ns = now
            if self.nav_state == NAV_OFFBOARD and self.arming_state == ARMING_STATE_ARMED:
                self.set_phase("route", now)
        elif self.phase == "land":
            if repeat and self.latch == "none":
                self.command(CMD_LAND)
                self.last_command_ns = now
            if self.was_armed and self.arming_state != ARMING_STATE_ARMED:
                self.stop("completed")

    def finish_checks(self, now: int) -> None:
        since = self.since_trigger(now)
        if since is not None and since >= self.fault.observe_s:
            self.stop("case_end")
        elif self.fault.is_case and self.was_armed and self.arming_state != ARMING_STATE_ARMED:
            self.stop("disarmed")
        elif self.latch != "none" and not self.fault.is_case:
            assert self.latch_ns is not None
            disarmed = self.arming_state != ARMING_STATE_ARMED
            if disarmed or (now - self.latch_ns) / 1e9 >= ABORT_OBSERVE_S:
                self.stop(f"aborted_{self.latch}")

    def send_response(self, command: str, now: int) -> None:
        if command == "none" or now - self.last_command_ns <= 1_000_000_000:
            return
        if command == "land":
            self.command(CMD_LAND)
        else:
            self.command(CMD_SET_MODE, MODE_CUSTOM, MODE_AUTO, SUB_MODE_LOITER)
        self.last_command_ns = now

    def transmit(self, action: tuple[float, ...], now: int) -> int:
        vx, vy, vz = enu_to_ned((action[0], action[1], action[2]))
        if self.fault.swap_axes:
            vx, vy = vy, vx
        if self.fault.flip_east:
            vy = -vy
        msg = TrajectorySetpoint()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = [math.nan, math.nan, math.nan]
        msg.velocity = [vx, vy, vz]
        msg.acceleration = [math.nan, math.nan, math.nan]
        msg.yaw = math.nan
        msg.yawspeed = yaw_rate_flu_to_frd(action[3])
        self.setpoint_pub.publish(msg)
        return time.monotonic_ns()

    def tick(self) -> None:
        now = time.monotonic_ns()
        if now >= self.deadline_ns:
            self.stop("timeout")
            return
        since = self.since_trigger(now)
        silent = self.fault.stop_publishing.active(since)
        odom = self.odom
        if odom is None:
            if not silent:
                self.heartbeat()
            return
        self.maybe_trigger(now)
        self.plan(odom["position"], odom["velocity"], now)
        if not silent:
            self.advance(now)
        inputs = GateInputs(
            now_ns=now,
            last_setpoint_ns=self.setpoint_ns,
            last_sensor_ns=self.sensor_ns,
            estimator_valid=self.local_position_valid,
            last_estimator_ns=odom["capture_ns"],
        )
        decision = decide(self.request, inputs, self.bounds, self.limits)
        mode = decision.mode
        reasons = list(decision.reasons)
        armed = self.arming_state == ARMING_STATE_ARMED
        flying = armed and self.phase in ("route", "settle", "hover")
        if self.reset_jump:
            reasons.append("estimator position reset in flight")
            mode = "hold" if mode == "continue" else mode
        if self.fault.gate_response:
            reached = self.reached_target
            if self.latch in TARGET_NAV and self.nav_state == TARGET_NAV[self.latch]:
                reached = True
            response = respond(
                self.latch, mode, self.nav_state, in_flight=flying, reached_target=reached
            )
            if response.latch != self.latch:
                reached = False
                self.latch_ns = self.latch_ns or now
            self.latch, self.reached_target = response.latch, reached
            send_setpoint, send_heartbeat = response.send_setpoint, response.send_heartbeat
            if not silent:
                self.send_response(response.command, now)
        else:
            # The control case: the setpoints stop, the heartbeat runs, and nothing else is sent.
            send_setpoint = decision.forward
            send_heartbeat = True
        in_stream = self.phase in ("stream", "route", "settle", "hover")
        if send_heartbeat and not silent:
            self.heartbeat()
        transmit = send_setpoint and decision.forward and in_stream and not silent
        sent_ns = self.transmit(decision.filtered, now) if transmit else None
        record = {
            "t_ns": now,
            "phase": self.phase,
            "waypoint_index": self.follower.index,
            "position_enu_m": list(odom["position"]),
            "velocity_enu_m_s": list(odom["velocity"]),
            "yaw_enu_rad": odom["yaw"],
            "capture_t_ns": odom["capture_ns"],
            "received_t_ns": odom["received_ns"],
            "estimator_valid": self.local_position_valid,
            "nav_state": self.nav_state,
            "arming_state": self.arming_state,
            "requested": list(self.request),
            "filtered": list(decision.filtered),
            "transmitted": list(decision.filtered) if transmit else None,
            "sent_t_ns": sent_ns,
            "valid_until_t_ns": now + self.bounds.max_setpoint_age_ns,
            "gate_mode": mode,
            "gate_reasons": reasons,
            "latch": self.latch,
            "since_trigger_s": since,
        }
        self.log.write(json.dumps(record, separators=(",", ":")) + "\n")
        self.finish_checks(now)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", required=True)
    parser.add_argument("--evals", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    parser.add_argument("--matrix")
    parser.add_argument("--case")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rclpy.init()
    with (out / "steps.jsonl").open("x", encoding="utf-8", buffering=1) as log:
        node = Mission(args, log)
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.01)
        result = node.result
        node.destroy_node()
    rclpy.shutdown()
    (out / "mission_result.json").write_text(
        json.dumps({"result": result}) + "\n", encoding="utf-8"
    )
    print(f"mission result: {result}")
    return 0 if result in ("completed", "case_end") else 1


if __name__ == "__main__":
    raise SystemExit(main())
