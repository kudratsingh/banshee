# Status board — banshee

_Derived from `work_orders/STATUS.jsonl` and `config/phases.json` by `tools/status_board.py`. Do not edit by hand._

Generated: 2026-11-01 00:40 UTC · ledger records: 38

## Phases

| Phase | Name | State | Exit tests (passed / frozen / total) | Prerequisites | Work orders |
|---|---|---|---|---|---|
| D0 | Operating envelope, platform proposal, compliance plan (no purchase) | **in_progress** | 4 / 6 / 6 | — | WO-001, WO-003, WO-006, WO-007, WO-008, WO-009, WO-011, WO-012 |
| D1 | PX4/Gazebo SITL, offboard velocity interface, logging to the contract, fault matrix | **not_started** | 0 / 0 / 5 | D0 | WO-002, WO-004 |
| D2 | Props-off sensor and localization walkthrough | **not_started** | 0 / 0 / 4 | D1 | WO-005 |
| D3 | Optional outdoor GPS-assisted checkout | **not_started** | 0 / 0 / 3 | D2 | — |
| D4 | Indoor VIO position hold in a controlled setup | **not_started** | 0 / 0 / 5 | D2 | — |
| D5 | GPS-denied known route | **not_started** | 0 / 0 / 5 | D4 | — |
| D6 | Fixed-target inspection from N declared viewpoints and return | **not_started** | 0 / 0 / 4 | D5 | — |
| D7 | Further missions one at a time; learned-component integration gates | **not_started** | 0 / 0 / 2 | D6 | — |

## Exit tests

| Exit test | Phase | Statement | Threshold | State | Report |
|---|---|---|---|---|---|
| ET-D0-1 | D0 | The operating envelope page is complete: mission/site, airframe class, speed/height/clearance limits with justification, sensors, compute, energy, reference, containment, human control, compliance, data/privacy. | zero empty fields; every unknown is a named owner question | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-2 | D0 | A priced BOM with dated sources covers at least two compatible airframe options (a 500 mm class kit and a 3-5 inch indoor frame) with landed cost including shipping, tax, spares, batteries, compliance, reference equipment and compute. | every line has a source and a date; totals per option; no purchase | frozen | — |
| ET-D0-3 | D0 | A compatible stack version matrix (PX4, ROS 2, Gazebo, bridge, QGroundControl, sensor drivers) is proposed with each pin labelled proposed or tested, and a D1 verification plan is written. | no latest-by-default pins; every entry labelled | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-4 | D0 | The compliance plan covers the Part 107 path, registration, Remote ID route, indoor-only applicability, site permission and visual-line-of-sight limits, with sources. | complete and sourced; recheck dates recorded | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-5 | D0 | The outside-in reference qualification plan (accuracy target, coverage, synchronization, session check) and the airframe-specific containment method are written. | accuracy target stated numerically; containment chosen per airframe/test configuration | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-6 | D0 | The owner has recorded a decision (or an explicit deferral) on test space and airframe candidate. | one recorded decision or deferral | frozen | — |
| ET-D1-1 | D1 | SITL launches reproducibly from a script with a version manifest. | 2/2 launches identical versions; zero null pins | not_run | — |
| ET-D1-2 | D1 | A waypoint mission completes through the offboard velocity/yaw-rate interface and its outcome is checked by independent code from the logged state. | proposed default: 10/10 nominal runs reach every waypoint within 0.5 m; freeze before running | not_run | — |
| ET-D1-3 | D1 | Each run is exported through contracts/v1/writer.py with correct frames and timebase (capture, receive, decision, sent times) and validates. | 100% contract_valid | not_run | — |
| ET-D1-4 | D1 | The simulated fault matrix is executed: stale setpoint while heartbeat continues, lost command stream, stale sensor data, missing depth, localization reset/loss, delayed planner, low energy, operator takeover; each behaves as specified and is logged, with configured versus tested behaviour distinguished. | all listed cases executed; any deviation from spec is reported, not hidden | not_run | — |
| ET-D1-5 | D1 | A setpoint-freshness and estimator-validity gate with frozen bounds sits in the command path and is unit-tested; heartbeat continuity never counts as setpoint freshness. | tests green; bounds documented with their justification | not_run | — |
| ET-D2-1 | D2 | Camera/IMU timestamp offsets, frame consistency and end-to-end latency are measured hand-carried. | offset estimate with CI; frame check passes; latency distribution reported | not_run | — |
| ET-D2-2 | D2 | VIO tracks through the test volume; dropouts and resets are counted; drift is measured against the outside-in reference. | proposed default: end-of-route drift <= 0.2 m; loss/recovery counts reported | not_run | — |
| ET-D2-3 | D2 | The outside-in reference is qualified: static survey residuals, dynamic latency, coverage map, session check procedure. | proposed default: static residual RMS <= 2 cm; coverage >= 90% of the test volume; inadequate coverage is inconclusive, not a pass | not_run | — |
| ET-D2-4 | D2 | With motors disarmed, the actual link is cut and the PX4 offboard-loss failsafe plus the project's freshness gate behave as specified independently of the laptop. | 3/3 trials match the specified behaviour | not_run | — |
| ET-D3-1 | D3 | Compliance is in place for the site: certificate if applicable, registration, Remote ID route, airspace and site permission. | all applicable items recorded with dates | not_run | — |
| ET-D3-2 | D3 | Manual flight checkout and GPS position hold within the frozen tolerance. | proposed default: position hold RMS <= 1.0 m over 60 s on 3/3 flights | not_run | — |
| ET-D3-3 | D3 | Emergency procedures (RTL, land, kill) are rehearsed and logged. | each procedure exercised once | not_run | — |
| ET-D4-1 | D4 | Containment, checklists, roles and emergency procedures are in place and signed off for the airframe and test configuration. | complete before first arm | not_run | — |
| ET-D4-2 | D4 | VIO position hold error against the outside-in reference stays within the frozen bound over repeated flights. | proposed default: RMS <= 0.3 m over 60 s on 5/5 flights | not_run | — |
| ET-D4-3 | D4 | Operator takeover works in flight. | 3/3 takeovers succeed | not_run | — |
| ET-D4-4 | D4 | Offboard loss in flight triggers the specified behaviour (hold or land depending on estimator validity). | 3/3 trials match spec | not_run | — |
| ET-D4-5 | D4 | VIO health under flight vibration is revalidated; hand-carry results are not reused as flight qualification. | loss/recovery counts and drift reported under flight conditions | not_run | — |
| ET-D5-1 | D5 | Route completion rate and path error against the reference meet the frozen bounds. | proposed default: >= 8/10 completions with path error RMS <= 0.5 m | not_run | — |
| ET-D5-2 | D5 | Degraded modes are exercised in flight (stale planner output, localization loss) and the drone responds as specified. | every listed case executed; outcomes match spec | not_run | — |
| ET-D5-3 | D5 | Minimum clearance to obstacles stays above the frozen bound. | proposed default: >= 0.5 m on all completed runs | not_run | — |
| ET-D5-4 | D5 | Planning latency quantiles, deadline misses and command expiries are reported. | reported; frozen bounds on p95 latency and expiry rate | not_run | — |
| ET-D5-5 | D5 | Energy reserve at landing is at or above the frozen reserve. | proposed default: >= 25% remaining on every run | not_run | — |
| ET-D6-1 | D6 | Mission rubric declared before flight (N viewpoints, coverage/visibility, dwell or image quality, target identity, start/return region, permitted route, timeout, reserve); completion requires every component. | proposed default: >= 7/10 complete missions | not_run | — |
| ET-D6-2 | D6 | Independent review of reference, log and video evidence confirms completions; a waypoint list alone is not success. | reviewer agrees on 100% of claimed completions | not_run | — |
| ET-D6-3 | D6 | Failure cases (occluded target, localization loss mid-mission, low energy) are handled as specified. | each case executed; behaviour matches spec | not_run | — |
| ET-D6-4 | D6 | Cost per mission attempt and per flight hour is reported. | reported | not_run | — |
| ET-D7-1 | D7 | Each mission is defined with a rubric and frozen thresholds before flight, and its degradation tests are listed. | to be frozen per mission when it becomes next | not_run | — |
| ET-D7-2 | D7 | A learned component is integrated only after held-out log evaluation, shadow-mode logging, and a controlled closed-loop comparison against the conventional baseline, with a kill switch and drone-owned acceptance. | to be frozen when a learned component is proposed; the uncertainty-gated trust question from PROGRAM section 8.2 is the first candidate | not_run | — |

## Work orders

| WO | Title | Phase | State | Last event (UTC) | Report |
|---|---|---|---|---|---|
| WO-001 | D0 operating envelope, platform proposal, stack matrix, compliance plan | D0 | **in_progress** | 2026-10-31T22:44:11.327280Z | — |
| WO-002 | D1 SITL: pinned launch, offboard velocity mission, independent outcome, contract export | D1 | **created** | 2026-10-31T07:51:52.077382Z | — |
| WO-003 | Supervised resource and spend enforcement (local, no paid execution) | D0 | **superseded** | 2026-11-01T00:39:54.551053Z | — |
| WO-004 | D1 fault matrix in simulation and the freshness gate in the command loop | D1 | **created** | 2026-10-31T07:51:52.172244Z | — |
| WO-005 | D2 props-off sensor, localization and reference checkout | D2 | **created** | 2026-10-31T07:51:52.215726Z | — |
| WO-006 | Program-wide rename of this repository and package to banshee | D0 | **accepted** | 2026-10-31T22:15:35.944907Z | reports/WO-006-program-rename-banshee.md |
| WO-007 | Designate the private GitHub remote and create the repository | D0 | **accepted** | 2026-10-31T09:11:55.829902Z | VERIFICATION.md |
| WO-008 | Fix three starter-kit tooling defects found during the rename review | D0 | **accepted** | 2026-10-31T22:15:35.975976Z | reports/WO-008-starter-kit-tooling-fixes.md |
| WO-009 | Protect accepted work orders and widen the secret scan | D0 | **accepted** | 2026-10-31T22:15:36.002410Z | reports/WO-009-status-freeze-and-token-scan.md |
| WO-011 | Lock the shared tooling files (superseded, never started) | D0 | **superseded** | 2026-10-31T22:54:36.820454Z | — |
| WO-012 | Extract the shared material into ironclad (superseded, never started) | D0 | **superseded** | 2026-10-31T22:54:36.847240Z | — |

