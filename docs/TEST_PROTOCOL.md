# TEST_PROTOCOL.md — mission and failure tests

Rules: `AGENTS.md §5, §7`. Exit tests that cite this protocol: `docs/PHASES.md`. Freeze numbers in `evals/<stage>-exit-tests.json` before each stage.

## 1. D1 simulator matrix (every case executed and logged)
Nominal hover and waypoint route; frame-sign and unit errors (injected); stale sensor data; missing depth; localization reset/loss; delayed planner; **stale setpoint while heartbeat continues**; lost command stream; network interruption; low-energy condition; operator takeover. Test the command path actually used (the offboard velocity interface through the chosen bridge). Document exact firmware and parameter versions; behaviour depends on the stack [S6]. Report *configured* behaviour and *tested* behaviour separately.

## 2. Timing and command freshness
- Log capture, receive, decision, transmit and known application times; unavailable times are `null`, never guessed; monotonic mapped time with clock-alignment evidence (`ironclad.contracts.v1`).
- `onboard/src/banshee_onboard/freshness.py` decides from sensor age, estimator validity and setpoint age, independently of the heartbeat. Bounds are frozen in `evals/D1-exit-tests.json` from the measured operating envelope before flight. *Proposed defaults:* max setpoint age 200 ms; max sensor age 150 ms; estimator gap 100 ms — justify or replace with measurements.
- Response depends on valid estimates: hold when position is valid and only the planner is stale; land when localization is lost; always allow operator takeover. No generic hover-on-every-fault rule.

## 3. Physical progression
Props-off tests precede any armed test. Revalidate sensing under vibration in the controlled flight gate (D4); hand-carry success is not flight qualification. Test actual laptop/link failure with a staged procedure; loss handling must remain available without a working laptop. The external reference is an evaluator, never an operational localization input in unaided-VIO tests. Never remove a bad run from the record; retain intervention, timeout and abort counts.

## 4. Pre-flight and session checklist (D3+; on GPS, the reference and VIO items do not apply)
1. Containment inspected; people excluded; observer briefed; operator on the independent link with takeover tested on the ground.
2. Battery voltage and cell balance recorded; reserve threshold set in PX4.
3. Reference cameras: known-pose check recorded; calibration ids logged.
4. Estimator health: VIO tracking before arm; EKF2 status logged.
5. Freshness gate bounds and failsafe parameters match the frozen `evals/` file (hash recorded).
6. Run id created (`core.runs.new_run_dir`), video started, flight log recording confirmed.
7. Abort criteria read aloud: who calls it, what the response is.
8. Handheld wind reading recorded and checked against the height and wind limits in `docs/OPERATING_ENVELOPE.md`.
9. Exclusion and crew distances confirmed; fence parameters checked from telemetry for this stage, including `MPC_XY_CRUISE` and `MPC_VEL_MANUAL`.
10. In VIO stages: global origin set from a checked GPS fix at the takeoff point (latitude, longitude, MSL altitude), and raw GPS against Home within 5 m horizontal and 10 m vertical, read from telemetry.

## 5. First mission rubric (D6)
Declare N viewpoints, coverage/visibility requirement, dwell or image-quality criterion, target identity, start/return region, permitted route, timeout and energy reserve. Completion requires every declared component. Independent review of reference, log and video evidence; a planned waypoint list alone is not mission success.

## 6. Exit metrics (every stage report)
Completion and intervention rates; path/position error with reference uncertainty stated; minimum clearance; latency quantiles and deadline misses; estimator loss/recovery; command expiries; energy reserve; cost per flight hour and per attempt. Numerical thresholds come from D0 and are frozen before testing, never chosen after a flight.

## 7. Statistics
Report counts with denominators and Wilson intervals; a 7/10 mission success rate has a 95% interval of roughly 40–89%, so small-N results are reported as such. Block by session (battery, light, operator); predeclare exclusions and how aborted runs are counted.
