# Status board — banshee

_Derived from `work_orders/STATUS.jsonl` and `config/phases.json` by `ironclad-status`. Do not edit by hand._

Generated: 2026-11-02 02:32 UTC · ledger records: 95

## Phases

| Phase | Name | State | Exit tests (passed / frozen / total) | Prerequisites | Work orders |
|---|---|---|---|---|---|
| D0 | Operating envelope, platform proposal, compliance plan (no purchase) | **passed** | 6 / 6 / 6 | — | WO-001, WO-003, WO-006, WO-007, WO-008, WO-009, WO-011, WO-012 |
| D1 | PX4/Gazebo SITL, offboard velocity interface, logging to the contract, fault matrix | **passed** | 5 / 5 / 5 | D0 | WO-002, WO-004, WO-013, WO-014, WO-016 |
| D2 | Props-off sensor and localization walkthrough | **ready** | 0 / 5 / 5 | D1 | WO-005, WO-017, WO-018, WO-020 |
| D3 | Outdoor GPS-assisted checkout | **not_started** | 0 / 0 / 5 | D2 | WO-015, WO-019 |
| D4 | VIO position hold in a controlled setup | **not_started** | 0 / 0 / 5 | D3 | — |
| D5 | GPS-denied known route | **not_started** | 0 / 0 / 5 | D4 | — |
| D6 | Fixed-target inspection from N declared viewpoints and return | **not_started** | 0 / 0 / 4 | D5 | — |
| D7 | Further missions one at a time; learned-component integration gates | **not_started** | 0 / 0 / 2 | D6 | — |

## Exit tests

| Exit test | Phase | Statement | Threshold | State | Report |
|---|---|---|---|---|---|
| ET-D0-1 | D0 | The operating envelope page is complete: mission/site, airframe class, speed/height/clearance limits with justification, sensors, compute, energy, reference, containment, human control, compliance, data/privacy. | zero empty fields; every unknown is a named owner question | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-2 | D0 | A priced BOM with dated sources covers at least two compatible airframe options (a 500 mm class kit and a 3-5 inch indoor frame) with landed cost including shipping, tax, spares, batteries, compliance, reference equipment and compute. | every line has a source and a date; totals per option; no purchase | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-3 | D0 | A compatible stack version matrix (PX4, ROS 2, Gazebo, bridge, QGroundControl, sensor drivers) is proposed with each pin labelled proposed or tested, and a D1 verification plan is written. | no latest-by-default pins; every entry labelled | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-4 | D0 | The compliance plan covers the Part 107 path, registration, Remote ID route, indoor-only applicability, site permission and visual-line-of-sight limits, with sources. | complete and sourced; recheck dates recorded | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-5 | D0 | The outside-in reference qualification plan (accuracy target, coverage, synchronization, session check) and the airframe-specific containment method are written. | accuracy target stated numerically; containment chosen per airframe/test configuration | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D0-6 | D0 | The owner has recorded a decision (or an explicit deferral) on test space and airframe candidate. | one recorded decision or deferral | passed | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| ET-D1-1 | D1 | SITL launches reproducibly from a script with a version manifest. | 2/2 launches identical versions; zero null pins | passed | reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md |
| ET-D1-2 | D1 | A waypoint mission completes through the offboard velocity/yaw-rate interface and its outcome is checked by independent code from the logged state. | proposed default: 10/10 nominal runs reach every waypoint within 0.5 m; freeze before running | passed | reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md |
| ET-D1-3 | D1 | Each run is exported through contracts/v1/writer.py with correct frames and timebase (capture, receive, decision, sent times) and validates. | 100% contract_valid | passed | reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md |
| ET-D1-4 | D1 | The simulated fault matrix is executed: stale setpoint while heartbeat continues, lost command stream, stale sensor data, missing depth, localization reset/loss, delayed planner, low energy, operator takeover; each behaves as specified and is logged, with configured versus tested behaviour distinguished. | all listed cases executed; any deviation from spec is reported, not hidden | passed | reports/WO-004-d1-fault-matrix-and-freshness-gate.md |
| ET-D1-5 | D1 | A setpoint-freshness and estimator-validity gate with frozen bounds sits in the command path and is unit-tested; heartbeat continuity never counts as setpoint freshness. | tests green; bounds documented with their justification | passed | reports/WO-004-d1-fault-matrix-and-freshness-gate.md |
| ET-D2-1 | D2 | Camera/IMU timestamp offsets, frame consistency and end-to-end latency are measured hand-carried. | offset estimate with CI; frame check passes; latency distribution reported | frozen | — |
| ET-D2-2 | D2 | VIO tracks through the test volume; dropouts and resets are counted; drift is measured against the outside-in reference. | proposed default: end-of-route drift <= 0.2 m; loss/recovery counts reported | frozen | — |
| ET-D2-3 | D2 | The outside-in reference is qualified: static survey residuals, dynamic latency, coverage map, session check procedure. | proposed default: static residual RMS <= 2 cm; coverage >= 90% of the test volume; inadequate coverage is inconclusive, not a pass | frozen | — |
| ET-D2-4 | D2 | With motors disarmed, the actual link is cut: PX4's offboard-loss flag sets no later than COM_OF_LOSS_T + 200 ms after the cut, with the time logged, and the project's freshness gate stops sending, independently of the laptop. PX4 selects no action while disarmed, so the action itself is tested in ET-D4-4. | 3/3 trials match the specified behaviour | frozen | — |
| ET-D2-5 | D2 | With propellers removed and motors disarmed, the RC link over CRSF, the kill switch and the mode switch are recognised on the actual Pixhawk 6X. Requires a dated owner approval to connect. | each control recognised; 3/3 power cycles | frozen | — |
| ET-D3-1 | D3 | Compliance is in place for the site: certificate if applicable, registration, Remote ID route, airspace and site permission. | all applicable items recorded with dates | not_run | — |
| ET-D3-2 | D3 | Manual flight checkout in Position mode and GPS position hold within the frozen tolerance. | proposed default: position hold RMS <= 1.0 m over 60 s on 3/3 flights | not_run | — |
| ET-D3-3 | D3 | Emergency procedures (RTL, land, kill) are rehearsed and logged. | each procedure exercised once | not_run | — |
| ET-D3-4 | D3 | Before the first arm: distance and geofence containment, exclusion, checklists, roles and emergency procedures are in place and signed off, and a parameter dump from the real aircraft matches the frozen values. | complete before first arm | not_run | — |
| ET-D3-5 | D3 | At low height on GPS: operator takeover, a geofence breach and RC loss each behave as specified on the real aircraft. | each 3/3; any deviation reported | not_run | — |
| ET-D4-1 | D4 | Containment, checklists, roles and emergency procedures are in place and signed off for the airframe and test configuration. | complete before first arm | not_run | — |
| ET-D4-2 | D4 | VIO position hold error against the outside-in reference stays within the frozen bound over repeated flights. | proposed default: RMS <= 0.3 m over 60 s on 5/5 flights | not_run | — |
| ET-D4-3 | D4 | Operator takeover works in flight. | 3/3 takeovers succeed | not_run | — |
| ET-D4-4 | D4 | Offboard loss in flight triggers the specified behaviour (hold or land depending on estimator validity), first with GPS aiding on, before VIO is relied on. | 3/3 trials match spec | not_run | — |
| ET-D4-5 | D4 | VIO health under flight vibration is revalidated; hand-carry results are not reused as flight qualification. | loss/recovery counts and drift reported under flight conditions | not_run | — |
| ET-D5-1 | D5 | Route completion rate and path error against the reference meet the frozen bounds. | proposed default: >= 8/10 completions with path error RMS <= 0.5 m | not_run | — |
| ET-D5-2 | D5 | Degraded modes are exercised in flight (stale planner output, localization loss) and the drone responds as specified. | every listed case executed; outcomes match spec | not_run | — |
| ET-D5-3 | D5 | Minimum clearance to obstacles stays above the frozen bound, excluding the staked reference equipment. | proposed default: >= 0.5 m on all completed runs | not_run | — |
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
| WO-001 | D0 operating envelope, platform proposal, stack matrix, compliance plan | D0 | **accepted** | 2026-11-01T01:55:46.389532Z | reports/WO-001-d0-operating-envelope-and-platform-proposal.md |
| WO-002 | D1 SITL: pinned launch, offboard velocity mission, independent outcome, contract export | D1 | **accepted** | 2026-11-01T05:58:17.128905Z | reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md |
| WO-003 | Supervised resource and spend enforcement (local, no paid execution) | D0 | **superseded** | 2026-11-01T00:39:54.551053Z | — |
| WO-004 | D1 fault matrix in simulation and the freshness gate in the command loop | D1 | **accepted** | 2026-11-01T12:10:07.957019Z | reports/WO-004-d1-fault-matrix-and-freshness-gate.md |
| WO-005 | D2 props-off sensor, localization and reference checkout | D2 | **created** | 2026-10-31T07:51:52.215726Z | — |
| WO-006 | Program-wide rename of this repository and package to banshee | D0 | **accepted** | 2026-10-31T22:15:35.944907Z | reports/WO-006-program-rename-banshee.md |
| WO-007 | Designate the private GitHub remote and create the repository | D0 | **accepted** | 2026-10-31T09:11:55.829902Z | VERIFICATION.md |
| WO-008 | Fix three starter-kit tooling defects found during the rename review | D0 | **accepted** | 2026-10-31T22:15:35.975976Z | reports/WO-008-starter-kit-tooling-fixes.md |
| WO-009 | Protect accepted work orders and widen the secret scan | D0 | **accepted** | 2026-10-31T22:15:36.002410Z | reports/WO-009-status-freeze-and-token-scan.md |
| WO-011 | Lock the shared tooling files (superseded, never started) | D0 | **superseded** | 2026-10-31T22:54:36.820454Z | — |
| WO-012 | Extract the shared material into ironclad (superseded, never started) | D0 | **superseded** | 2026-10-31T22:54:36.847240Z | — |
| WO-013 | Adopt ironclad v1.1.0 and remove the vendored shared files | D1 | **accepted** | 2026-11-01T04:25:51.348734Z | reports/WO-013-adopt-ironclad.md |
| WO-014 | Correct AGENTS.md sections 13.8 and 13.9 | D1 | **accepted** | 2026-11-01T04:35:48.715239Z | reports/WO-014-section-13-wording.md |
| WO-015 | Record the owner's decisions after D1: ADR-0010, D3 standoffs, VM bounds | D3 | **accepted** | 2026-11-01T23:53:22.656911Z | reports/WO-015-owner-decisions-after-d1.md |
| WO-016 | Stop the node overriding a mode chosen while disarmed | D1 | **accepted** | 2026-11-01T23:53:22.750471Z | reports/WO-016-preflight-mode-override.md |
| WO-017 | Purchase request for Option A, and freeze D2's exit tests | D2 | **accepted** | 2026-11-02T00:02:15.827420Z | reports/WO-017-purchase-request-and-d2-freeze.md |
| WO-018 | Record the owner's purchase approval and write the buy list | D2 | **accepted** | 2026-11-02T01:23:37.444448Z | reports/WO-018-purchase-approval.md |
| WO-019 | Close the stale-status offboard-command window in the mode-override fix | D3 | **created** | 2026-11-02T01:22:35.987284Z | — |
| WO-020 | Record the owner's buy-list decisions and the C2 correction | D2 | **in_progress** | 2026-11-02T02:32:27.058221Z | — |

