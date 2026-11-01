# WO-002 | D1 SITL: pinned launch, offboard velocity mission, independent outcome, contract export
**Phase:** D1
**Exit tests advanced:** ET-D1-1, ET-D1-2, ET-D1-3
**Size:** L (split into PRs: launch + lock → offboard bridge + mission → outcome + export)
**Prerequisites:** WO-001 accepted (`config/stack-lock.proposed.json` exists); an Ubuntu machine, VM or container for the flight stack (`docs/ENVIRONMENT.md`); `evals/D1-exit-tests.json` waypoint tolerance and run count frozen before mission runs.
**Authorization:** AGENTS §2.1 only. Simulation only: no physical flight controller may be connected; no hardware endpoint may be present (stop condition).
**Files:** `src/banshee/sitl/`, `src/banshee/offboard/`, `src/banshee/export/`, `src/banshee/outcome/`, `tests/`, `config/stack-lock.resolved.json`, `docs/adr/ADR-0005-frame-and-timebase-convention.md`, `reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md`, ignored `runs/`, `data/`.

## Objective
Stand up a reproducible software-in-the-loop environment on the proposed pins, fly a waypoint mission through the bounded velocity/yaw-rate offboard interface, judge the mission by independent code from the logged state, and export every run through the contract — the foundation every later stage and the world model's M4 depend on.

## Scope
1. **Launch + lock** (`src/banshee/sitl/launch.py`): one script starts PX4 SITL + Gazebo + the bridge with the pinned versions, writes a version manifest into the run directory, and refuses to start if any reported version differs from `config/stack-lock.resolved.json`. Two clean launches must report identical versions (ET-D1-1). Mark tested entries `tested` in the lock.
2. **Offboard bridge** (`src/banshee/offboard/`): publish the offboard heartbeat and a separate setpoint stream of bounded velocity + yaw-rate commands with explicit frame, units, limits and expiry; log requested/filtered/transmitted values with decision and send times; route every command through `freshness.assess` and the limits before sending.
3. **Frame and timebase ADR** (ADR-0005): ROS ENU/FLU internally, converted at the PX4 boundary (NED/FRD); monotonic clock mapping; sign tests that would catch a swapped axis.
4. **Mission runner**: takeoff → waypoint route → land, with per-step logging of state estimates (position, velocity, attitude, estimator validity), commands and timing.
5. **Independent outcome** (`src/banshee/outcome/waypoints.py`): from the logged state alone, decide whether each waypoint was reached within the frozen tolerance and whether the mission completed; no dependency on the planner.
6. **Contract export** (`src/banshee/export/`): each run → a `physics_sim` episode via `ironclad.contracts.v1.writer` with the drone's configuration, controller version, simulator identity (initial state + assets), reference streams tagged `reference_only`; `ironclad-validate` must pass (ET-D1-3). Retain raw ulog alongside.
7. Run the frozen number of nominal missions (proposed 10); report completion with Wilson interval, waypoint errors, latency distribution, export validation (ET-D1-2).

## Out of scope
The fault matrix and freshness bounds in the loop (WO-004), hardware, VIO, purchases, paid compute, learned components.

## Verification
```bash
make check
python -m banshee.sitl.launch --check-versions          # twice, on a clean machine; identical manifests
python -m banshee.offboard.mission --route evals/D1-route.json --runs 10 --out runs/
python -m banshee.outcome.waypoints --run runs/<id> --tolerance-file evals/D1-exit-tests.json
ironclad-validate data/derived/d1/<episode>/episode.json
ironclad-status --render > docs/STATUS_BOARD.md
```
Expected: version manifests identical; ≥ frozen completion count; every episode `contract_valid`; frame sign tests pass; report lists latency quantiles and any deviation from spec.

## Exit criteria
ET-D1-1, ET-D1-2, ET-D1-3 pass with evidence. ET-D1-4 and ET-D1-5 are WO-004; phase D1 passes after both WOs.

## Stop conditions
Unsupported stack pairing on the proposed pins (record, propose an alternative in a new lock version, do not use latest); ambiguous frame or action semantics (write the ADR first); any physical flight-controller endpoint detected; any need for paid resources.

## Report
`reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md`
