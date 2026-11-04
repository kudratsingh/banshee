# Banshee — Omni Drone

An aerial autonomy platform built from conventional flight control outward: PX4, offboard guidance, independent outcome checks, and a command gate that can refuse a planner's request. The goal is a robot that earns broader mission capability through demonstrated steps, from waypoint flight to GPS-denied navigation and inspection.

**Current milestone: simulation passed; hardware qualification remains open.** D0 (operating envelope) and D1 (PX4/Gazebo simulation, offboard control, logging and fault testing) have passed their recorded exit tests. D2 props-off sensing and localization is ready, with no exit tests passed. See the [status board](docs/STATUS_BOARD.md).

## What works today

- **Pinned PX4/Gazebo SITL.** Bounded launch and campaign tooling, offboard velocity/yaw-rate missions, and independent waypoint judging from recorded state.
- **A command gate in the control path.** Speed limits, setpoint age, sensor age and estimator validity are checked separately. A continuing heartbeat cannot make an expired command fresh.
- **Fault injection and analysis.** Stale commands, lost links, sensor/localization faults, planner delays, low energy and operator takeover are exercised in simulation, with deviations retained in the reports.
- **Traceable trajectory exports.** Raw PX4 logs, explicit frames and timestamps, contract validation, and append-only run records.
- **Separate onboard code.** The ROS-facing node and pure command logic live in a Python 3.10 package, separate from the host's Python 3.12+ research tooling.

```text
Mission / planner request
    → command limits + freshness / estimator gate
    → offboard velocity interface → PX4 → simulated aircraft
    → raw logs + trajectory export → independent outcome check
```

## Evidence and next milestone

The [D1 mission report](reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md) records reproducible launches, waypoint outcomes and validated exports. The [fault-matrix report](reports/WO-004-d1-fault-matrix-and-freshness-gate.md) records executed cases, failures, corrections and review findings. Later platform and compatibility checks are linked from the [status board](docs/STATUS_BOARD.md).

These are simulator results. They do not establish flight readiness, unaided visual-inertial odometry, obstacle avoidance or reliable operation on an aircraft. The next milestone measures sensing, timing, localization and independent reference quality with propellers off. GPS-denied routes, inspection missions and learned-component integration remain later stages.

The development ladder is **D0 envelope → D1 simulation → D2 props-off sensing → D3 outdoor checkout → D4 VIO hold → D5 GPS-denied route → D6 inspection**. “Omni” means growing mission capability, not an omnidirectional airframe. [Phases and exit tests](docs/PHASES.md) define what each stage must demonstrate.

## Inspect and run checks

Host checks need Python **3.12+** and access to the pinned `ironclad-kit` dependency in the **private** `kudratsingh/ironclad` repository. Public source and reports are available here, but dependency installation is access-controlled.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e . -r requirements-dev.txt
make check
ironclad contract-info
```

The CPU tier runs lint, types, unit/contract tests, policy verification, secrets scanning and link checks. It does not launch PX4 or connect to hardware. SITL and onboard setup use separate pinned environments; follow the [environment guide](docs/ENVIRONMENT.md) and [onboard package](onboard/pyproject.toml). Simulator evidence does not authorize an aircraft test.

## Code and documentation

| Area | Entry point |
|---|---|
| Onboard mission, guidance and command gate | [onboard/src/banshee_onboard](onboard/src/banshee_onboard/) |
| Simulator launch and resource bounds | [src/banshee/sitl](src/banshee/sitl/) |
| Fault campaigns and analysis | [src/banshee/faults](src/banshee/faults/) |
| Independent outcomes and exports | [outcome](src/banshee/outcome/), [export](src/banshee/export/) |
| System design and operating limits | [Architecture](docs/ARCHITECTURE.md), [operating envelope](docs/OPERATING_ENVELOPE.md) |
| Current evidence | [Status board](docs/STATUS_BOARD.md), [reports](reports/) |

Part of the [Physical AI Program](PROGRAM.md). Contributors should read [AGENTS.md](AGENTS.md) before making changes.
