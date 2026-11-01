# WO-004 — D1 fault matrix in simulation and the freshness gate in the command loop

**Status:** results recorded; independent review pending. Later results are appended below, dated.
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-004 · **Phase:** D1 · **Protocol version:** `evals/D1-exit-tests.json`, sha256 `1f4900194371c9124b3aa0e6ef29c438d947fe931fc513baba698948ae758180`; `evals/D1-fault-matrix.json`, sha256 `d9262da5cc307198fc363c3211b35928d833e53f4b3028a35c4a84fcef73b32e`
**Program link:** PROGRAM §5.1, §6 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
Every case in the D1 fault matrix was executed against the real command path (mission node, gate, offboard velocity interface, XRCE-DDS bridge, PX4 SITL, Gazebo), with one log and one contract export each. Configured and tested behaviour are reported per case, and deviations are listed, not hidden. The freshness gate with the frozen bounds sits in that path and decides independently of the heartbeat.

This is simulation only. It is not flight readiness. No hardware was connected and nothing was bought. Untested: see §9.

## 2. Frozen method
- **Bounds:** `evals/D1-exit-tests.json`, unchanged: setpoint 200 ms, sensor 150 ms, estimator 100 ms.
- **Matrix:** 47 cases, one trial per case in each recording. Expected values were written before the recording. A deviation is a result, not a failure of the run.
- **Measures:** Modes and motion come from the ULog, with motion taken from Gazebo ground truth. Gate decisions come from the node's step log. The two clocks are joined through `timesync_status.estimated_offset`. Each VM run is fresh and bounded.
- **No sample-based claim:** one trial per case gives behaviour examples, not rates. Differences between the recordings show how much a single trial can vary.

### Changes to the matrix before it was frozen (debug pass, `runs/fault-debug/`)
| Change | Why (measured) |
|---|---|
| E-01, E-02, E-03 `needs_trigger` false | These faults prevent station-keeping, so the waypoint trigger may never fire |
| P-01 changed to 100 ms, new P-03 at 150 ms | A 150 ms stall plus a tick crosses the 200 ms bound, so 150 ms is an edge case, not an inside-the-bound case |
| G-04 delay 13 s | So that the drift reaches past 40 m |
| `RC_CHAN_CNT` 8 in the RC cases | PX4 did not treat the simulated RC as calibrated without it |
| Vision cases: origin sends delayed, timeouts 75 s | Repeated origin sends caused repeated resets. Arming was refused anyway |

Expected values that the debug pass showed to be wrong were kept, and appear as deviations in §4.

### Changes after the first recording
The first recording (commit `59796346887cf833c34107c0cba3c86f883af0d8`) found a bug in the agent's code, described in §5. The fix is commit `6216f0ddbebb55a86d0cbd444841c23be0a6f86b`, and every case was recorded again at that commit. **Results of record are the second recording.** The first stays in the record at `runs/fault-matrix-recorded/`.

The same commit changed the matrix after its results had been seen. R-01, R-02, R-06, T-03 and T-04 gained `holds_s`, which requires a mode to last and not just appear. R-06 also gained `final_latch: operator`, and its configured text now says the mode stays selected. These changes only tighten the checks.

## 3. Reproduction
Commit `6216f0ddbebb55a86d0cbd444841c23be0a6f86b`, stack lock `config/stack-lock.resolved.json`, sha256 `42afc415f5a3b1e52be974fd5bd0631572f3a50dd489ff2d7385b08568d81a4f`. PX4 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`, ROS 2 Jazzy, Gazebo Harmonic, gz-sim 8.15.0, in the Lima VM `banshee-sitl` on arm64. `PYTHONPATH=src` throughout, with `pyulog==1.2.0`.

```bash
make check
python -m banshee.sitl.bounded --log L --max-log-bytes 2000000 --timeout-s 9000 \
  --min-free-bytes 20000000000 --vm banshee-sitl -- \
  python -m banshee.faults.run_matrix --matrix evals/D1-fault-matrix.json --summary S
python -m pytest tests/test_freshness.py -q
python -m banshee.sitl.campaign --runs 10
```

**Deviation from the WO's command:** it names `--out runs/`. `run_matrix` has no such option, because `ironclad.core.runs.new_run_dir` always writes under `runs/`. `--summary` writes the combined file. Summaries: `runs/fault-matrix-recorded-2/matrix.jsonl` and, for the first recording, `runs/fault-matrix-recorded/matrix.jsonl`. These paths are ignored by git and stay on this machine. Run IDs are in §4.

**PX4 failsafe parameters.** Each case read its parameters back after start, into `params-readback.txt` in its run directory, beside `env.lock.json` and `versions.json`. `NAV_DLL_ACT` needs this: `gz_x500` raises it to 2 after the override, so it is set again after the airframe loads.

## 4. Results
All measured, in the VM. Times are seconds from the fault's trigger.

| Measure | Result |
|---|---|
| Cases executed and logged | 47/47, each with a clean VM run |
| Contract exports valid (`ironclad-validate`) | 47/47; the 5 cases that never armed hold only pre-arming steps |
| Cases with no deviation | 40/47. V-04 and V-05 are among them but do not discriminate (see below), and five cases only measure, with no specified values (P-03, H-03, H-04, G-04, W-01) |
| Cases with a deviation | 7: L-02, R-04, G-01, G-02, V-01, V-02, V-03 |
| Regression on the route, at the fixed commit | 10/10 (Wilson 95%: 0.722–1.000); worst 0.210 m by estimate, 0.247 m by ground truth; tolerance unchanged |
| False gate latches on the nominal route | 0 of 10 at the fixed commit, 0 of 10 at the first |
| Freshness and fault unit tests | `tests/test_freshness.py` and `tests/test_faults.py` pass, in `make check` |

### Deviations
| Case | Specified | Tested | Reading |
|---|---|---|---|
| L-02 | Land (18) within 8 s | Descend (12) at 0.09 s; landed and disarmed at 10.05 s | The expected value was wrong. With no position PX4 flies Land as Descend. The safe outcome is reached earlier than specified |
| R-04 | Return within 2 s of RC loss | Hold at 0.50 s, Return at 5.50 s | PX4 holds for `COM_FAIL_ACT_T` (5 s, default) first. The envelope's time was missing this |
| G-01 | Land within 20 s | Hold at 16.82 s, Land at 21.82 s | Same 5 s hold |
| G-02 | Land within 14 s | Hold at 11.46 s, Land at 16.47 s | Same 5 s hold |
| V-01, V-02, V-03 | Vision-only flight, then a fault | Arming refused: "heading estimate not stable" and "Global position estimate required", so no fault was injected | Not a test of the specified response. See the proposal below |

**Proposal on the vision cases (WO stop condition).** The specified responses for V-01 to V-03 were not shown on this stack, whether the cause is `gz_x500_vision` set-up or the stack itself. Their refusals also mean V-04 and V-05 ("never armed") pass without discriminating, because nothing armed in the vision world at all. No specification was changed. These cases come from WO-001's proposals and are not in ET-D1-4's list. The proposal is to carry them to D4, where vision is in scope, with the vision set-up as that work order's first task. The vision-only rows of `docs/OPERATING_ENVELOPE.md` stay estimated.

### Heartbeat is not freshness
| Case | Setpoints stop, heartbeat continues, at | Response | Hold at | Horizontal travel after the fault |
|---|---|---|---:|---:|
| H-01 | 1.0 m/s | gate on | 0.18 s | 1.17 m |
| H-02 | 2.5 m/s | gate on | 0.19 s | 3.61 m |
| H-03 (control) | 1.0 m/s | gate response off | none in 12 s, then the node exits | 12.09 m |
| H-04 (control) | 2.5 m/s | gate response off | none until the fence, 10.55 s | 29.72 m |

Without the response, PX4 keeps flying the last setpoint for as long as the heartbeat runs, which is the failure the gate exists for.

### Measured against the envelope's estimates
These do not change `docs/OPERATING_ENVELOPE.md`, which is outside this WO's files. They are inputs for the work that freezes D3.

| Item | Estimated | Measured | Consequence |
|---|---|---|---|
| Offboard loss to Hold (`COM_OF_LOSS_T` 1.0 s) | 1.0 s, 1.35 s worst | 1.02–1.28 s (C-01..06, R-05) | agrees |
| Travel after lost stream, 1.0 m/s | 1.85 m (reaction plus braking) | 2.03–2.24 m (C-01, C-03, C-04, R-05) | above estimate |
| Travel after lost stream, 2.5 m/s | 5.36 m | 5.81 m (C-02) | above estimate. With the 2.0 m error term this is 7.81 m, over the 7.35 m standoff and the 7.5 m margin |
| Hold braking from 2.5 m/s, less 0.2 s of reaction | 1.98 m | about 3.2 m (H-02, K-01) | the braking estimate is low by about 60% |
| Hold braking from 1.0 m/s, less 0.2 s of reaction | 0.50 m | about 0.8–1.0 m (H-01, K-02) | low; `MPC_XY_VEL_MAX` 1.0 changes it little |
| Fence overrun, horizontal, at 2.5 m/s | inside 7.5 m | 3.6–3.9 m (G-01) | inside |
| Fence overrun, vertical, at 1.0 m/s | not estimated | 0.53–0.55 m (G-02) | ceiling plus about 0.6 m |
| Stale climb after loss, at the limit | not estimated | +1.46–1.48 m (C-05) | add to height margin |
| Stale descent after loss, at the limit | not estimated | 0.70–0.72 m (C-06) | add to low-height margin |
| Drift after estimator position loss, no wind, from 2.5 m/s | not in the formula | 12.4–12.5 m (G-04), and the fence did not act at 44.07 m | the formula has no term for carried speed |
| Same at 5.4 m/s wind, 10 m descent, from hover | 75 m (*estimated*, wind × height ÷ 0.7, with no operator delay here) | 40.9 m and 46.1 m (W-01, two recordings); descent took 16.9 s and 22.8 s, so slower than 0.7 m/s | inside the estimate, but past the 40 m fence with no fence action |
| Return against the ceiling | under 10 m | 9.89–9.91 m (T-01) | agrees |
| `MPC_XY_VEL_MAX` holds at 2.5 | ≤ 2.5 m/s | peak 2.51 stick, 2.68 Return | up to 7% over |
| `MPC_XY_VEL_MAX` holds at 1.0 | ≤ 1.0 m/s | peak 1.01 stick, 1.18 Return | up to 18% over |
| `EKF2_NOAID_TOUT` 1 s false triggers | test | none in 20 nominal missions and the no-fault cases | none seen |
| Operator: Altitude after position loss | "holds altitude until commanded" | Altitude kept for 22.9 s of the 25 s window (R-06). Height fell from 3.16 m to 3.00 m at the end of the log (lowest 2.86 m), and it drifted 1.52 m | holds, in no wind |

**Proposed for D3 (estimated from the above; not applied):** at 2.5 m/s, reaction 1.35 s × 2.5 + measured braking 3.2 m + error 2.0 m = **8.6 m** in place of 7.35 m. At 1.0 m/s, 1.35 + 1.0 + 1.0 = **3.35 m** in place of 2.85 m. Exclusion radius: 40 + 9 + 100 = 149 m, so the rounded 150 m still holds. Also: add a carried-speed term to the drift formula, and add `COM_FAIL_ACT_T`'s 5 s to the fence and RC-loss times. The fence did not act once position was lost (G-04, W-01), so the exclusion radius has to cover that case on its own.

### Gate bounds, as measured (ET-D1-5)
Over the 10 regression missions in flight (7,142 ticks): tick gap median 50.0 ms, p99 50.9 ms, worst 57.2 ms. Estimator age median 14.1 ms, p99 36.8 ms, worst 44.7 ms. So there is no false latch at 200 ms and 100 ms, and each bound has margin. A 336 ms tick gap occurred in 3 of the 10 missions, always in the `stream` phase before flight, where no latch can form.

The planner stall series brackets the setpoint bound: at 100 ms (P-01) no latch in either recording, at 500 ms (P-02) a latch at 0.23 s, and at 150 ms (P-03) no latch in the first recording and a latch in the second (`setpoint stale: 200174380 ns > 200000000 ns`). So a stall plus a tick is at the bound's edge, and a 150 ms stall should be treated as able to latch. The sensor bound's justification rests on a VIO rate not in use in this stack, so it stays *estimated*; the stream that drives it in simulation is a stand-in.

### Variation between recordings
| Case | First recording | Second recording | Reading |
|---|---|---|---|
| E-01 | Never reached waypoint 0; fence at 42.62 m; Land | Passed through waypoint 0, so the trigger fired and the case ended at 28.6 m, node stopped | The judge failed the route in both. Whether the fence is reached is chance |
| E-03 | Oscillated, radius 3.43 m | Passed through waypoint 0, then flew on, radius 25.84 m | The clamp held in both: transmitted peak 2.5 m/s, flown peak 2.60 and 2.59 m/s |
| P-03 | No latch | Hold latch | See above |
| W-01 | Drift 40.9 m | Drift 46.1 m, peak 6.15 m/s | Wind case: one trial is not a bound |

### Every case: configured and tested
In N-01, E-01, E-03, E-04, P-01, H-03 and G-05 the Hold shown is PX4's response to the node exiting at the end of the observation window, about 1 s later. It is not a response to the fault. In H-04 the Hold is the fence.

| Case | Configured | Tested (second recording, measured) | Deviation |
|---|---|---|---|
| N-01 Nominal hover | Stays in offboard at the hover point; the gate continues. | Hold 16.14 s; travel 0.037 m; radius 0.073 m, up 5.317 m, peak 0.049 m/s; latch none | none |
| E-01 Frame error injected: east and north swapped at the boundary | The gate cannot see a frame error. The independent judge must fail the route. It cannot hold station either, so the fault acts from takeoff; no trigger is needed. | Hold 5.17 s; travel 7.991 m; radius 28.605 m, up 5.156 m, peak 2.079 m/s; latch none | none |
| E-02 Sign error injected: east flipped at the boundary | The gate cannot see a sign error. The independent judge must fail the route. It cannot hold station either, so the fault acts from takeoff; no trigger is needed. | armed; not triggered: Offboard 7.61 s, Hold 41.10 s, Land 46.11 s, disarmed 56.98 s; radius 42.528 m, up 4.998 m, peak 2.086 m/s; latch operator | none |
| E-03 Unit error injected: requests ten times too large | The gate clamps every transmitted setpoint to the frozen limits. The trigger is not needed, because the fault acts from takeoff. | Hold 5.14 s; travel 10.242 m; radius 25.841 m, up 5.064 m, peak 2.585 m/s; latch none | none |
| E-04 Yaw rate sign: +0.3 rad/s FLU | Positive FLU yaw rate turns counter-clockwise from above. | Hold 6.06 s; travel 0.042 m; radius 0.12 m, up 4.66 m, peak 0.053 m/s; latch none | none |
| S-01 Stale sensor data | Position valid, sensor stale: the gate holds and the node commands Hold. | Hold 0.19 s; travel 0.071 m; radius 0.089 m, up 4.712 m, peak 0.045 m/s; latch hold | none |
| S-02 Missing depth (no depth sensor in this stack; injected as a sensor stream that never updates) | As stale sensor. The gate's sensor input is what depth would feed. | Hold 0.19 s; travel 0.056 m; radius 0.086 m, up 4.715 m, peak 0.079 m/s; latch hold | none |
| L-01 Localization loss: estimator samples stop reaching the node | Estimator stale: the gate says land and the node commands Land. | Land 0.14 s, disarmed 10.86 s; travel 0.042 m; radius 0.056 m, up 4.888 m, peak 0.037 m/s; latch land | none |
| L-02 Localization loss: EKF2 stops using GPS in flight (EKF2_GPS_CTRL 0), so position goes invalid | Within EKF2_NOAID_TOUT 1 s position is invalid; the gate says land, or PX4's own failsafe lands first. | Descend 0.09 s, disarmed 10.05 s; travel 0.116 m; radius 0.092 m, up 4.708 m, peak 0.035 m/s; latch land | nav 18 within 8.0 s |
| L-03 Localization reset: a 3 m jump and a reset counter change, injected in the node | A reset in flight: the node holds and does not chase the jump. | Hold 0.08 s; travel 0.051 m; radius 0.068 m, up 4.648 m, peak 0.055 m/s; latch hold | none |
| P-01 Delayed planner, inside the bound: 100 ms stalls each second | Setpoint age stays under 200 ms; the mission continues. | Hold 11.07 s; travel 0.055 m; radius 0.057 m, up 4.734 m, peak 0.071 m/s; latch none | none |
| P-03 Delayed planner, at the edge of the bound: 150 ms stalls each second | A 150 ms stall plus a 50 ms tick can cross 200 ms. Measure whether and when it latches. | Hold 0.18 s; travel 0.055 m; radius 0.125 m, up 4.678 m, peak 0.035 m/s; latch hold | none |
| P-02 Delayed planner, over the bound: one 500 ms stall | Setpoint age passes 200 ms: the gate holds. The latch stays after the planner recovers. | Hold 0.23 s; travel 0.064 m; radius 0.116 m, up 4.772 m, peak 0.048 m/s; latch hold | none |
| H-01 Stale setpoint while the heartbeat continues, gate response on, at 1.0 m/s | Heartbeat is not freshness. The gate holds and the node commands Hold. | Hold 0.18 s; travel 1.168 m; radius 5.729 m, up 4.734 m, peak 1.09 m/s; latch hold | none |
| H-02 Stale setpoint while the heartbeat continues, gate response on, at 2.5 m/s | As H-01 at the GPS limit. | Hold 0.19 s; travel 3.614 m; radius 17.289 m, up 4.758 m, peak 2.625 m/s; latch hold | none |
| H-03 Control: setpoints stop, heartbeat continues, no gate response, at 1.0 m/s | Measure what PX4 does alone. docs/OPERATING_ENVELOPE.md says the last setpoint may be applied throughout. | Hold 13.06 s; travel 12.092 m; radius 18.353 m, up 5.185 m, peak 1.044 m/s; latch none | none |
| H-04 Control: setpoints stop, heartbeat continues, no gate response, at 2.5 m/s | As H-03. The fence is the only limit left, so this also shows that. | Hold 10.55 s, Land 15.56 s; travel 29.718 m; radius 43.365 m, up 4.994 m, peak 2.587 m/s; latch none | none |
| C-01 Lost command stream, no manual control at arming, at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.07 s; travel 2.086 m; radius 6.543 m, up 4.97 m, peak 1.073 m/s; latch operator | none |
| C-02 Lost command stream at 2.5 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.06 s; travel 5.805 m; radius 19.327 m, up 4.868 m, peak 2.622 m/s; latch operator | none |
| C-03 Companion death: the node is killed at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.28 s; travel 2.235 m; radius 6.754 m, up 4.709 m, peak 1.093 m/s; latch none | none |
| C-04 Network interruption: the agent stops at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.18 s; travel 2.167 m; radius 6.579 m, up 5.026 m, peak 1.089 m/s; latch land | none |
| C-05 Stale climb at the vertical limit, stream lost | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold. Measure the height gained. | Hold 1.02 s; travel 0.048 m; radius 0.109 m, up 7.034 m, peak 0.082 m/s; latch operator | none |
| C-06 Stale descent at the commanded limit, stream lost | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold. Measure the height lost. | Hold 1.07 s; travel 0.031 m; radius 0.053 m, up 11.769 m, peak 0.036 m/s; latch operator | none |
| B-01 Low energy: fast simulated drain | COM_LOW_BAT_ACT 3: Return at critical (0.35), Land at emergency (0.15). | Hold 11.55 s, Return 16.55 s, Land 19.48 s, disarmed 27.08 s; travel 0.103 m; radius 0.076 m, up 4.69 m, peak 0.058 m/s; latch operator | none |
| R-01 Operator takeover by the mode switch, at 1.0 m/s | The mode switch moves to Position; the node stops commanding. | Position 0.08 s; travel 0.878 m; radius 5.289 m, up 4.806 m, peak 1.133 m/s; latch operator | none |
| R-02 Operator takeover by the sticks, COM_RC_OVERRIDE 3 | Moving the sticks in offboard switches to Position; the node stops commanding. | Position 0.05 s; travel 8.535 m; radius 14.844 m, up 4.765 m, peak 1.076 m/s; latch operator | none |
| R-03 Kill switch in flight | Motors stop at once; the aircraft falls; disarm follows at COM_KILL_DISARM 5 s. | disarmed 5.10 s; travel 0.018 m; radius 0.064 m, up 4.671 m, peak 0.058 m/s; latch none | none |
| R-04 RC removed in flight, with manual control present at arming | NAV_RCL_ACT 2 Return. With offboard not excepted from RC loss (COM_RCL_EXCEPT 0). | Hold 0.50 s, Return 5.50 s; travel 4.396 m; radius 5.943 m, up 5.623 m, peak 2.677 m/s; latch operator | nav 5 within 2.0 s |
| R-05 Lost command stream with manual control present at arming | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.06 s; travel 2.027 m; radius 6.504 m, up 4.797 m, peak 1.08 m/s; latch operator | none |
| R-06 Operator reaction in the drift case: Altitude mode after estimator position loss | Altitude mode stays selected and holds height until commanded. Measure the height change. | Descend 0.08 s, Altitude 2.12 s; travel 1.301 m; radius 1.508 m, up 4.652 m, peak 0.104 m/s; latch operator | none |
| K-01 Hold braking from 2.5 m/s | Measure stop distance; replaces the envelope's estimate. | Hold 0.23 s; travel 3.715 m; radius 17.318 m, up 4.947 m, peak 2.636 m/s; latch hold | none |
| K-02 Hold braking from 1.0 m/s, with MPC_XY_VEL_MAX 1.0 | Measure stop distance at the VIO-stage limit. | Hold 0.18 s; travel 1.166 m; radius 5.679 m, up 4.791 m, peak 1.075 m/s; latch hold | none |
| G-01 Geofence breach, horizontal, at 2.5 m/s | GF_ACTION 5 Land at 40 m. Measure the overrun. | Hold 16.82 s, Land 21.82 s, disarmed 32.48 s; travel 43.99 m; radius 43.941 m, up 4.894 m, peak 2.581 m/s; latch operator | nav 18 within 20.0 s |
| G-02 Geofence breach, vertical, at 1.0 m/s | GF_ACTION 5 Land at 14 m. Measure the overrun. | Hold 11.46 s, Land 16.46 s, disarmed 40.56 s; travel 0.09 m; radius 0.068 m, up 14.53 m, peak 0.194 m/s; latch operator | nav 18 within 14.0 s |
| G-03 Home invalid at arming: EKF2 with no GPS from start | COM_ARM_WO_GPS 0: arming denied. | never armed | none |
| G-04 Fence with position lost mid-flight: EKF2 stops GPS at about 32 m, with the drift reaching past 40 m | Record the mode entered and whether the fence still acts. Raw GPS stays live here; a lost receiver is not injectable on this stack. | Descend 0.31 s, disarmed 10.34 s; travel 12.535 m; radius 44.067 m, up 4.827 m, peak 2.59 m/s; latch none | none |
| G-05 Moved takeoff point: spawned 20 m east | The fence is centred on Home, so 30 m from the new Home stays inside. | Hold 6.06 s; travel 0.264 m; radius 50.404 m, up 5.036 m, peak 2.582 m/s; latch none | none |
| T-01 Return against the ceiling at the GPS limit | RTL_RETURN_ALT 10 m; no breach of the 30 m ceiling; speed obeys MPC_XY_VEL_MAX 2.5. | Return 0.09 s, disarmed 30.48 s; travel 13.611 m; radius 16.344 m, up 9.908 m, peak 2.68 m/s; latch operator | none |
| T-02 Return at MPC_XY_VEL_MAX 1.0 | Speed obeys 1.0 m/s. | Return 0.23 s, disarmed 16.13 s; travel 4.434 m; radius 5.422 m, up 5.036 m, peak 1.175 m/s; latch operator | none |
| T-03 Full-stick Position at MPC_XY_VEL_MAX 2.5 | Position mode obeys 2.5 m/s at full stick. | Position 0.11 s; travel 20.628 m; radius 26.062 m, up 4.859 m, peak 2.506 m/s; latch operator | none |
| T-04 Full-stick Position at MPC_XY_VEL_MAX 1.0 | Position mode obeys 1.0 m/s at full stick. | Position 0.11 s; travel 8.493 m; radius 10.594 m, up 4.725 m, peak 1.01 m/s; latch operator | none |
| W-01 Wind: drift during a descent after EKF2 stops GPS | Measure horizontal drift to the ground in simulated wind. | Descend 0.17 s, disarmed 22.78 s; travel 46.071 m; radius 46.255 m, up 9.723 m, peak 6.154 m/s; latch land | none |
| V-01 Vision only (gz_x500_vision, EKF2_GPS_CTRL 0, global origin set): offboard loss | Record the mode entered. Confirm aiding is off. Hold if global position stays valid. | never armed | fault injected |
| V-02 Vision only, origin wrong by under 40 m | Record what the fence does. | never armed | fault injected |
| V-03 Vision only, origin too high | Record what the fence does. | never armed | fault injected |
| V-04 Vision only, no origin | Expected to be refused at arming. | never armed | none |
| V-05 SYS_HAS_GPS 0 | Expected to be refused at arming. | never armed | none |

### Run IDs (second recording)
N-01 `20261101T084002Z_a0bffa8e`, E-01 `20261101T084058Z_0523b383`, E-02 `20261101T084148Z_f7fa9234`, E-03 `20261101T084302Z_aea99e8d`, E-04 `20261101T084347Z_08934db6`, S-01 `20261101T084432Z_d8565fcf`, S-02 `20261101T084522Z_9dfb7494`, L-01 `20261101T084612Z_89a99e50`, L-02 `20261101T084716Z_fc3a7b14`, L-03 `20261101T084836Z_bb9b3783`, P-01 `20261101T084926Z_fbaad66a`, P-03 `20261101T085017Z_d5852829`, P-02 `20261101T085116Z_0cff5e71`, H-01 `20261101T085207Z_c59028c7`, H-02 `20261101T085258Z_a4a7c7d9`, H-03 `20261101T085352Z_8a3d0405`, H-04 `20261101T085446Z_63479169`, C-01 `20261101T085549Z_3970a05e`, C-02 `20261101T085643Z_f3a9a922`, C-03 `20261101T085737Z_bb4f6bc1`, C-04 `20261101T085832Z_3f1c6a2e`, C-05 `20261101T085925Z_7564b8aa`, C-06 `20261101T090013Z_97dcb628`, B-01 `20261101T090125Z_fa276945`, R-01 `20261101T090315Z_8cb7f3ef`, R-02 `20261101T090407Z_49f954b4`, R-03 `20261101T090459Z_930b4bcb`, R-04 `20261101T090549Z_3f0e5797`, R-05 `20261101T090646Z_9e488d93`, R-06 `20261101T090740Z_d93bf434`, K-01 `20261101T090845Z_71194adb`, K-02 `20261101T090938Z_782aa97f`, G-01 `20261101T091030Z_aa015ff1`, G-02 `20261101T091142Z_e2c41f9e`, G-03 `20261101T091303Z_e6fddd26`, G-04 `20261101T091406Z_4d936951`, G-05 `20261101T091526Z_18df67f7`, T-01 `20261101T091622Z_776a0825`, T-02 `20261101T091735Z_7172de4b`, T-03 `20261101T091842Z_2fd4231f`, T-04 `20261101T091932Z_29681ccb`, W-01 `20261101T092022Z_09df05ba`, V-01 `20261101T092152Z_d8140fb5`, V-02 `20261101T092311Z_8f9a5135`, V-03 `20261101T092430Z_0652ddac`, V-04 `20261101T092549Z_836783c7`, V-05 `20261101T092653Z_af010af7`

Regression at the fixed commit: `20261101T092757Z_8e90c809`, `20261101T092908Z_c608f6fa`, `20261101T093019Z_1ae0fe12`, `20261101T093131Z_1eace15c`, `20261101T093242Z_a07cdc55`, `20261101T093354Z_268c2c00`, `20261101T093505Z_8fb7a2cd`, `20261101T093617Z_e2f51f9e`, `20261101T093728Z_afcb1bd8`, `20261101T093839Z_510ebce0`.

## 5. Failure analysis
### The node overrode the operator (found in the first recording, fixed)
**What happened.** In the first recording R-06 passed its check, "Altitude within 4 s", at 2.10 s. The log showed Altitude lasted 84 ms before the aircraft returned to Descend and landed. PX4's log repeats "Landing at current position" once a second. The fault was in the agent's code, not PX4: the node had latched `land`, PX4 was flying that as Descend, and Descend was not counted as the target. So the node kept repeating Land, including over the operator's switch. The protocol says always allow operator takeover, so this was a safety defect.

The check passed because it asked only whether the mode was entered.

**Fix.**
- The node now commands only while the vehicle is in the state it decided from, and any other state is the operator or PX4. Descend counts as the land response (ADR-0009, `src/banshee/offboard/response.py`).
- In the nominal `land` phase, Land repeats only while the vehicle is still in Offboard (`src/banshee/offboard/mission.py`).
- `holds_s` was added to the checks, and to the takeover cases.

**Evidence.** Recorded again: R-06 stays in Altitude from 2.12 s to the end of the window, with `final_latch` operator (run ID in §4). First-recording failure: `20261101T080344Z_1245da95`. New unit tests cover each path.

**Not measured:** the nominal `land` phase change has no fault case. The 10 regression missions show landing still works. An operator takeover during a nominal landing was **not run**.

**Retro.** Read the timeline, not just the check, for every case; this finding came from doing that. A check that a state was reached says nothing about whether it lasted.

### A second gap found while closing the recording
The WO's scope asks for one contract export per case, and the first recording had none. `run_matrix.export_case` now writes one to `data/derived/d1-faults/<run id>`. Success there means "as specified", not "route flown". `tolerance_m` is 0 in those rubrics, because the case's checks are held in `outcome.json`.

### What the deviations have in common
Four of the seven are expected values that the frozen matrix had wrong about PX4 (L-02, plus the 5 s hold in R-04, G-01 and G-02), and the vehicle reached the specified outcome in each, some seconds later in the last three. The other three are the vision cases, which show nothing about the specified response.

### Other behaviour worth knowing
- C-04 (the agent stops): the node latches `land`, but cannot reach PX4. PX4's own Hold at 1.18 s is the response. What happens after Hold when the link never returns was **not run**, apart from low energy in B-01.
- G-05: the fence moves with Home. At 30 m from the moved Home, 50.4 m from the world origin, it does not act, as the envelope said.
- G-03: arming is refused with no global position.
- S-02: this stack has no depth sensor, so "missing depth" is injected as a sensor stream that stops updating. It tests the gate path, not a depth pipeline.

### Carried over from WO-002's review (unchanged, open)
- A corrupt ULog aborts a campaign rather than recording a failure.
- A sample dropped by the frame guard is not logged.
- The settle phase reads a velocity that can be stale.
- Mode and arm commands do not pass the freshness gate.
- The node's timeout stops it without a land command.
- In `stream`, before flight, the node repeats mode and arm commands once a second. No operator input was tested there.

## 6. Cost and latency
No paid compute and no spending, so there is no cost record. Each recording took about 48 minutes of VM time for 47 cases, and the 10 regression missions about 12 minutes. Gate reaction, from fault to Hold: 0.08–0.23 s (S, L-03, P-02, H, K).

## 7. Sealed access
None.

## 8. Exit tests and acceptance
| Exit test | Threshold (frozen) | Result | Evidence | Pass? |
|---|---|---|---|---|
| ET-D1-4 | All cases executed; deviations reported; configured and tested distinguished | 47/47 executed, 7 deviations reported; 5 vision cases did not reach flight, as reported | `runs/fault-matrix-recorded-2/matrix.jsonl`, §4 | yes, pending review |
| ET-D1-5 | Gate with frozen bounds in the command path, unit-tested; heartbeat ≠ freshness; bounds justified | Gate in the path; tests green; H-01 to H-04 show the difference; setpoint and estimator bounds measured against flight; sensor bound still estimated | `tests/test_freshness.py`, `tests/test_faults.py`, §4 | yes, pending review |

Phase D1 is `passed` once ET-D1-1 to 5 are all recorded, which needs the independent review first (`AGENTS.md §13.9`).

## 9. Limits
- Simulation only. Nothing here shows flight readiness, and real links, RC hardware and sensors were not used. Real link cuts belong to D2.
- One trial per case in each recording. §4's variation table shows that a trial is not a bound, most of all in wind.
- Simulated RC arrives through `RC_CHANNELS_OVERRIDE`, not a receiver. Stick and switch latency here says nothing about a radio.
- **Not run:** vision-only flight, and with it the origin-error cases and the 0.5 m `COM_POS_FS_EPH` setting; takeover during a nominal landing; long-duration Hold after link loss; QGroundControl, and the second clean build, carried from WO-002.
- World wind was one setting, 5,2,0 m/s, with no gusts.
