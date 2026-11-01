"""ROS 2 mission node: takeoff, route and land through the offboard velocity interface. SITL only.

Runs inside the VM, with ROS 2 and ``px4_msgs`` sourced. The heartbeat and the setpoint stream are
separate: the heartbeat always goes out, and a setpoint goes out only if the gate forwards it. Each
tick logs one JSON line to ``steps.jsonl``. It never connects to hardware, and it stops at a wall
clock limit.
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

from ..freshness import GateInputs
from .frames import (
    enu_to_ned,
    ned_to_enu,
    yaw_enu_from_ned,
    yaw_ned_from_quaternion,
    yaw_rate_flu_to_frd,
)
from .gate import decide, load_frozen
from .guidance import RouteFollower, load_route

TICK_S = 0.05
STREAM_BEFORE_SWITCH_S = 1.5
NAV_STATE_OFFBOARD = 14
ARMING_STATE_ARMED = 2
CMD_SET_MODE = 176
CMD_ARM = 400
CMD_LAND = 21


class Mission(Node):  # type: ignore[misc]
    """One flight: wait for the estimator, stream, switch to offboard, arm, fly the route, land."""

    def __init__(self, args: argparse.Namespace, log: IO[str]) -> None:
        super().__init__("banshee_mission")
        self.bounds, self.limits = load_frozen(Path(args.evals))
        self.follower = RouteFollower(load_route(Path(args.route)))
        self.deadline_ns = time.monotonic_ns() + int(args.timeout_s * 1e9)
        self.log = log
        self.phase = "wait_estimator"
        self.phase_start_ns = time.monotonic_ns()
        self.last_command_ns = 0
        self.odom: dict[str, Any] | None = None
        self.px4_offset_ns: int | None = None
        self.local_position_valid = False
        self.nav_state = -1
        self.arming_state = -1
        self.was_armed = False
        self.finished = False
        self.result = "timeout"
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

    def on_odom(self, msg: Any) -> None:
        received = time.monotonic_ns()
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
        self.odom = {
            "position": position,
            "velocity": velocity,
            "yaw": yaw_enu_from_ned(yaw_ned_from_quaternion(w, x, y, z)),
            "capture_ns": px4_ns + self.px4_offset_ns,
            "received_ns": received,
        }

    def on_status(self, msg: Any) -> None:
        self.nav_state = int(msg.nav_state)
        self.arming_state = int(msg.arming_state)
        if self.arming_state == ARMING_STATE_ARMED:
            self.was_armed = True

    def on_flags(self, msg: Any) -> None:
        self.local_position_valid = not (msg.local_position_invalid or msg.local_velocity_invalid)

    def command(self, command: int, param1: float = 0.0, param2: float = 0.0) -> None:
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = command
        msg.param1 = param1
        msg.param2 = param2
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

    def next_request(self, position: tuple[float, float, float], now: int) -> tuple[float, ...]:
        """Advance the mission state and return the requested action."""
        elapsed = (now - self.phase_start_ns) / 1e9
        repeat = now - self.last_command_ns > 1_000_000_000
        if self.phase == "wait_estimator" and self.local_position_valid:
            self.set_phase("stream", now)
        elif self.phase == "stream" and elapsed >= STREAM_BEFORE_SWITCH_S:
            if repeat:
                self.command(CMD_SET_MODE, 1.0, 6.0)
                self.command(CMD_ARM, 1.0)
                self.last_command_ns = now
            if self.nav_state == NAV_STATE_OFFBOARD and self.arming_state == ARMING_STATE_ARMED:
                self.set_phase("route", now)
        elif self.phase == "route":
            velocity = self.follower.step(position)
            if velocity is None:
                self.set_phase("land", now)
            else:
                return (*velocity, 0.0)
        elif self.phase == "land":
            if repeat:
                self.command(CMD_LAND)
                self.last_command_ns = now
            if self.was_armed and self.arming_state != ARMING_STATE_ARMED:
                self.stop("completed")
        return (0.0, 0.0, 0.0, 0.0)

    def tick(self) -> None:
        now = time.monotonic_ns()
        if now >= self.deadline_ns:
            self.stop("timeout")
            return
        self.heartbeat()
        odom = self.odom
        if odom is None:
            return
        requested = self.next_request(odom["position"], now)
        inputs = GateInputs(
            now_ns=now,
            last_setpoint_ns=now,
            last_sensor_ns=odom["received_ns"],
            estimator_valid=self.local_position_valid,
            last_estimator_ns=odom["capture_ns"],
        )
        decision = decide(
            (requested[0], requested[1], requested[2], requested[3]),
            inputs,
            self.bounds,
            self.limits,
        )
        transmit = decision.forward and self.phase in ("stream", "route")
        sent_ns = None
        if transmit:
            msg = TrajectorySetpoint()
            msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
            msg.position = [math.nan, math.nan, math.nan]
            msg.velocity = list(enu_to_ned(decision.filtered[:3]))
            msg.acceleration = [math.nan, math.nan, math.nan]
            msg.yaw = math.nan
            msg.yawspeed = yaw_rate_flu_to_frd(decision.filtered[3])
            self.setpoint_pub.publish(msg)
            sent_ns = time.monotonic_ns()
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
            "requested": list(requested),
            "filtered": list(decision.filtered),
            "transmitted": list(decision.filtered) if transmit else None,
            "sent_t_ns": sent_ns,
            "valid_until_t_ns": now + self.bounds.max_setpoint_age_ns,
            "gate_mode": decision.mode,
            "gate_reasons": list(decision.reasons),
        }
        self.log.write(json.dumps(record, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", required=True)
    parser.add_argument("--evals", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout-s", type=float, default=180.0)
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
    return 0 if result == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
