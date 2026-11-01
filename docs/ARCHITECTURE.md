# ARCHITECTURE.md — Omni Drone

Program context: `PROGRAM.md §5.1, §6`. Ladder and exit tests: `docs/PHASES.md`.

## 1. What this system is
A general-purpose aerial autonomy platform built **conventionally first** and extended one mission at a time. Proven components (PX4 flight control, ROS 2, visual-inertial odometry, mapping, a mission executive) carry every mission; learned components enter only through evidence gates, and the drone can always run without them.

## 2. Layered architecture (proposed default; fixed by evidence in D0–D1)

```
 Mission executive (goals → subgoals → skills; success detection; recovery; operator interface)
        │ skill requests (go to, hold, inspect viewpoint, search region, return)
 Local planner / skills (conventional: route planning, obstacle avoidance, viewpoint selection)
        │ bounded velocity + yaw-rate setpoints  [u = (vx, vy, vz, yaw_rate), body or local frame, units, limits, expiry]
 Command gate (setpoint freshness, estimator validity, limits, geometric clearance, operator override)
        │ offboard setpoints (PX4 offboard mode; heartbeat separate from setpoint stream)
 PX4 flight controller (attitude/rate control, failsafes, offboard-loss behaviour)
        │
 Aircraft + sensors (IMU, camera(s), depth, GPS when outdoors, battery)  → state estimation (EKF2 + VIO) → maps
```

| Layer | Owner | Conventional implementation (D1–D6) | Where learning may enter later (D7+) |
|---|---|---|---|
| Mission executive | this project | explicit state machine (reuses the Incident Commander pattern: deterministic guards, independent success detector, bounded recovery) | an LLM may interpret requests into subgoals; spatial facts always come from the estimator and map |
| Local planner / skills | this project | conventional route planning and avoidance on the map | learned residual dynamics inside MPC, **gated by calibrated uncertainty** (the research question) |
| Command gate | this project | `src/banshee/freshness.py` + limits + clearance + operator override | never learned |
| Flight control | PX4 | stock firmware, pinned | never |
| State estimation | this project (configuration) | PX4 EKF2 with external VIO input | never in the loop; the world model may consume logs offline |
| Reference (evaluation only) | this project | outside-in cameras + AprilTags, independent clocks | — |

## 3. Interfaces that must be exact
- **Action:** bounded velocity and yaw-rate commands with explicit frame, units, duration/expiry and limits (`contracts/v1` action_spec). Requested, filtered, transmitted and measured-applied values are logged separately with their times.
- **Frames:** one internal convention (ROS: ENU/FLU) with conversion at the PX4 boundary (NED/FRD); the convention is an ADR written in D1 and tested with sign checks.
- **Timing:** capture, arrival, decision, transmit and (where known) application times, in a declared monotonic clock; unknown times are `null`, never guessed. At 2 m/s a 100 ms delay is 20 cm of travel before braking.
- **Freshness:** sensor age, estimator validity and setpoint age are checked independently of the ROS 2 offboard heartbeat; expired commands are not sent.

## 4. Safety and command authority
- Only this project's command gate and PX4 may command the aircraft. World-model outputs are proposals; the gate can reject them; the drone runs without them.
- Failure response depends on which estimates remain valid: hold if position is valid and only the planner is stale; land if localization is lost; operator takeover is always available on an independent link.
- Loss handling must work without the laptop: PX4's offboard-loss failsafe is configured and tested on the real link (D2 for the flag, D4 for the action).
- Operating envelope (`docs/OPERATING_ENVELOPE.md`) bounds speed, height, clearance, payload and energy reserve; exit tests check them.

## 5. Modules (what exists, what is specified)

| Module | Path | Status |
|---|---|---|
| Core record helpers (append-only ledgers, artifact store, run dirs, logs, config) | `src/banshee/core/` | implemented, tested |
| Setpoint freshness / estimator validity gate (pure logic) | `src/banshee/freshness.py` | implemented, tested; bounds to be frozen in D1 |
| Typed interfaces (estimator, gate, mission executive, skill, learned-proposal adapter) | `src/banshee/interfaces.py` | implemented as Protocols |
| SITL launch + version manifest | `src/banshee/sitl/` | **not implemented** (WO-002) |
| Offboard velocity bridge + mission runner | `src/banshee/offboard/` | **not implemented** (WO-002) |
| Contract export of flight logs | `src/banshee/export/` | **not implemented** (WO-002) |
| Fault-matrix harness | `src/banshee/faults/` | **not implemented** (WO-004) |
| Outside-in reference pipeline | `src/banshee/reference/` | **not implemented** (D2) |
| Mission executive | `src/banshee/mission/` | **not implemented** (D5–D6) |
| World-model adapter (manifest consumer; shadow only) | `src/banshee/learned/` | **not implemented** (D7+) |

## 6. Compute placement
Laptop for SITL in D1. Jetson Orin Nano Super from D2, hand-carried, then flown from D4, linked to the Pixhawk 6X by TELEM2 or Ethernet. Telemetry is 915 MHz, because Wi-Fi will not reach in a field (owner, 2026-10-31; ADR-0007). The aircraft's loss response never depends on the laptop or the Jetson.

## 7. Data
Every flight (SITL or real) is exported through `contracts/v1/writer.py` as a `physics_sim` or `real` episode with the drone's configuration, controller version and calibration ids; raw PX4 logs (ulog) are retained alongside. These exports are the drone's only interface to the world-model project (M4). Reference streams carry `role: reference_only`.
