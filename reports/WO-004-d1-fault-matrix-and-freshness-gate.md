# WO-004 — D1 fault matrix in simulation and the freshness gate in the command loop

**Status:** results recorded; independent review recorded in §10. Later results are appended below, dated.
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-004 · **Phase:** D1 · **Protocol version:** `evals/D1-exit-tests.json`, sha256 `1f4900194371c9124b3aa0e6ef29c438d947fe931fc513baba698948ae758180`; `evals/D1-fault-matrix.json`, sha256 `856d6b83ad1d4b9360e8c169202ea10055853e23119dd61d60b2e87c7bc588f7`
**Program link:** PROGRAM §5.1, §6 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
All 47 cases in the D1 fault matrix were executed against the real command path (mission node, gate, offboard velocity interface, XRCE-DDS bridge, PX4 SITL, Gazebo), with one log and one contract export each. 41 reached flight with the fault applied. 6 never armed, and of those only G-03 tests what it specifies (§4). Configured and tested behaviour are reported per case, and deviations are listed, not hidden. The freshness gate with the frozen bounds sits in that path and decides independently of the heartbeat.

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

### Four recordings, and why
**Results of record are the fourth recording.** The others stay in the record. Each one after the first exists because the one before it found a defect in the agent's code (§5).

| Recording | Commit | Matrix sha256 | Summary | What it showed |
|---|---|---|---|---|
| First | `59796346887cf833c34107c0cba3c86f883af0d8` | earlier | `runs/fault-matrix-recorded/` | The node overrode the operator (R-06). No contract exports yet |
| Second | `6216f0ddbebb55a86d0cbd444841c23be0a6f86b` | `d9262da5…` | `runs/fault-matrix-recorded-2/` | Reviewed. The review found the items in §10 |
| Third | `2ce9126c5c87b5fb9ae63cc603fb0c6fc115914a` | `856d6b83…` | `runs/fault-matrix-recorded-3/` | One review fix broke R-06: it armed in Hold and never reached offboard |
| Fourth | `9a2571f88f85d8c937311701873d6e018cbf6f14` | `856d6b83…` | `runs/fault-matrix-recorded-4/` | **Results of record** |

The matrix changed twice after results had been seen. Both changes only tighten the checks:
- At the second recording, R-01, R-02, R-06, T-03 and T-04 gained `holds_s`, which requires a mode to last and not just appear. R-06 also gained `final_latch: operator`, and its configured text now says the mode stays selected.
- At the third, G-03 and V-01 to V-05 gained `node.arm_attempt_after_s` and `expect.arm_attempted`. Before that, these cases recorded "never armed" without the node ever having asked.

## 3. Reproduction
Commit `9a2571f88f85d8c937311701873d6e018cbf6f14`, stack lock `config/stack-lock.resolved.json`, sha256 `42afc415f5a3b1e52be974fd5bd0631572f3a50dd489ff2d7385b08568d81a4f`. PX4 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`, ROS 2 Jazzy, Gazebo Harmonic, gz-sim 8.15.0, in the Lima VM `banshee-sitl` on arm64. `PYTHONPATH=src` throughout, with `pyulog==1.2.0`.

```bash
make check
python -m banshee.sitl.bounded --log L --max-log-bytes 2000000 --timeout-s 9000 \
  --min-free-bytes 20000000000 --vm banshee-sitl -- \
  python -m banshee.faults.run_matrix --matrix evals/D1-fault-matrix.json --summary S
python -m pytest tests/test_freshness.py -q
python -m banshee.sitl.campaign --runs 10
```

**Deviation from the WO's command:** it names `--out runs/`. `run_matrix` has no such option, because `ironclad.core.runs.new_run_dir` always writes under `runs/`. `--summary` writes the combined file. These paths are ignored by git and stay on this machine. Run IDs are in §4.

**Deviation from the WO's file list:** the gate's response has to live in the command path, so this WO also changed `src/banshee/offboard/response.py` (new), `src/banshee/offboard/mission.py` and `src/banshee/export/episode.py`, and added `evals/D1-fault-matrix.json`, two ADRs and a `CHANGES.md` entry. `src/banshee/freshness.py` was not changed. The nominal export's content did not change.

**Git state in the run records.** `git.json` reads `dirty: true` from the second run of each recording on, because each run appends to `ledgers/runs.jsonl`. `git status` before and after the fourth recording showed that file as the only change.

**PX4 failsafe parameters.** Each case read its parameters back after start, into `params-readback.txt` in its run directory, beside `env.lock.json` and `versions.json`. `NAV_DLL_ACT` needs this: `gz_x500` raises it to 2 after the override, so it is set again after the airframe loads. `COM_FAIL_ACT_T` is not in that file. Its 5 s comes from PX4's log line "entering Hold for 5 seconds" and the measured gaps.

## 4. Results
All measured, in the VM, from the fourth recording unless a row says otherwise. Times are seconds from the fault's trigger. In a case that did not trigger, they are seconds from the first `vehicle_status` sample in the ULog.

| Measure | Result |
|---|---|
| Cases executed and logged | 47/47, each with a clean VM run |
| Reached flight with the fault applied | 41/47 |
| Never armed | 6: G-03, V-01 to V-05. The node sent 25 arm commands in each, and PX4 logged "Arming denied: Resolve system health failures first" |
| Contract exports valid (`ironclad-validate`) | 47/47; the 6 cases that never armed hold only pre-arming steps |
| Cases with no deviation | 40/47. V-04 and V-05 are among them but do not discriminate (see below), and five cases only measure, with no specified values (P-03, H-03, H-04, G-04, W-01) |
| Cases with a deviation | 7: L-02, R-04, G-01, G-02, V-01, V-02, V-03 |
| Regression on the route, at the fixed commit | 10/10 (Wilson 95%: 0.722–1.000); worst 0.206 m by estimate, 0.306 m by ground truth; tolerance unchanged |
| False gate latches on the nominal route | 0 of 40 missions, 10 at each recording's commit |
| Freshness and fault unit tests | `tests/test_freshness.py` and `tests/test_faults.py` pass, in `make check` |

### Deviations
| Case | Specified | Tested | Reading |
|---|---|---|---|
| L-02 | Land (18) within 8 s | Descend (12) at 0.06 s; landed and disarmed at 10.70 s | The expected value was wrong. With no position PX4 flies Land as Descend. The safe outcome is reached earlier than specified |
| R-04 | Return within 2 s of RC loss | Hold at 0.48 s, Return at 5.48 s | PX4 holds for `COM_FAIL_ACT_T` (5 s) first. The envelope's time was missing this |
| G-01 | Land within 20 s | Hold at 16.70 s, Land at 21.70 s | Same 5 s hold |
| G-02 | Land within 14 s | Hold at 11.51 s, Land at 16.51 s | Same 5 s hold |
| V-01, V-02, V-03 | Vision-only flight, then a fault | Arming refused, so no fault was injected | Not a test of the specified response. See the proposal below |

B-01 shows the same 5 s hold (Hold 11.33 s, Return 16.34 s, Land 19.37 s). Its limits are 60 s and 70 s, so it is not a deviation, but the hold is there.

### Never-armed cases
G-03 discriminates, because the other 41 cases arm through the same node and commands. V-04 and V-05 do not: nothing armed in the vision world at all, so their "refused at arming" shows nothing about their own conditions.

**Proposal on the vision cases (WO stop condition; ADR-0010, proposed).** The specified responses for V-01 to V-03 were not shown on this stack, whether the cause is `gz_x500_vision` set-up or the stack itself. No specification was changed. These cases come from WO-001's proposals and are not in ET-D1-4's list or `docs/TEST_PROTOCOL.md`. The proposal is to carry them to D4, where vision is in scope, with the vision set-up as that work order's first task. The vision-only rows of `docs/OPERATING_ENVELOPE.md` stay estimated.

### Heartbeat is not freshness
| Case | Setpoints stop, heartbeat continues, at | Response | Hold at | Horizontal travel after the fault |
|---|---|---|---:|---:|
| H-01 | 1.0 m/s | gate on | 0.23 s | 1.23 m |
| H-02 | 2.5 m/s | gate on | 0.18 s | 3.53 m |
| H-03 (control) | 1.0 m/s | gate response off | none in 12 s, then the node exits | 12.14 m |
| H-04 (control) | 2.5 m/s | gate response off | none until the fence, 10.64 s | 29.88 m |

Without the response, PX4 keeps flying the last setpoint for as long as the heartbeat runs, which is the failure the gate exists for.

### Measured against the envelope's estimates
These do not change `docs/OPERATING_ENVELOPE.md`, which is outside this WO's files. They are inputs for the work that freezes D3. Ranges cover the second, third and fourth recordings, except that the third's R-06 is excluded because it never flew.

| Item | Estimated | Measured | Consequence |
|---|---|---|---|
| Offboard loss to Hold (`COM_OF_LOSS_T` 1.0 s) | 1.0 s, 1.35 s worst | 1.02–1.28 s (C-01..06, R-05) | agrees |
| Travel after lost stream, 1.0 m/s | 1.85 m (reaction plus braking) | 2.03–2.26 m (C-01, C-03, C-04, R-05) | above estimate |
| Travel after lost stream, 2.5 m/s | 5.36 m | 5.70–5.92 m (C-02) | above estimate. With the 2.0 m error term the largest is 7.92 m, over the 7.35 m standoff and the 7.5 m margin |
| Hold braking from 2.5 m/s, less 0.2 s of reaction | 1.98 m | 3.0–3.2 m (H-02, K-01) | the braking estimate is low by about 50–60% |
| Hold braking from 1.0 m/s, less 0.2 s of reaction | 0.50 m | 0.93–1.02 m (H-01, K-02) | low by about double; `MPC_XY_VEL_MAX` 1.0 changes it little |
| Fence overrun, horizontal, at 2.5 m/s | inside 7.5 m | 3.82–3.94 m (G-01) | inside |
| Fence overrun, vertical, at 1.0 m/s | not estimated | 0.53–0.68 m (G-02) | ceiling plus about 0.7 m |
| Stale climb after loss, at the limit | not estimated | +1.45–1.50 m (C-05) | add to height margin |
| Stale descent after loss, at the limit | not estimated | 0.70–0.71 m (C-06) | add to low-height margin |
| Drift after estimator position loss, no wind, from 2.5 m/s, PX4 alone (no gate response) | not in the formula | 12.5–13.1 m (G-04), and the fence did not act at 44.07–44.57 m | the formula has no term for carried speed |
| Same at 5.4 m/s wind, 10 m descent, from hover | 77 m (*estimated*, 5.385 × 10 ÷ 0.7, with no operator delay here) | 41.5–46.1 m (W-01), 40.9 m in the first recording; descent took 17.1–22.6 s, so slower than 0.7 m/s | inside the estimate, but past the 40 m fence with no fence action |
| Return against the ceiling | under 10 m | 9.91–9.97 m (T-01) | agrees, with little to spare |
| `MPC_XY_VEL_MAX` holds at 2.5 | ≤ 2.5 m/s | peak 2.50–2.51 stick, 2.67–2.69 Return | up to 7.5% over, in Return |
| `MPC_XY_VEL_MAX` holds at 1.0 | ≤ 1.0 m/s | peak 1.00–1.01 stick, 1.14–1.18 Return | up to 18% over, in Return |
| `EKF2_NOAID_TOUT` 1 s false triggers | test | none in 40 nominal missions and the no-fault cases | none seen |
| Operator: Altitude after position loss | "holds altitude until commanded" | Altitude from 2.12 s to the end of the window, 22.9 s. Measured from Altitude entry to the end of the log: height 3.21 m to 3.11 m, lowest 2.86 m, horizontal drift 1.84 m. Before that, about 1.4 m of height went in the 1.8 s of Descend (R-06) | holds, in no wind. The operator has to allow for the height lost before the switch |

**Proposed for D3 (estimated from the above; not applied):** at 2.5 m/s, reaction 1.35 s × 2.5 + measured braking 3.2 m + error 2.0 m = **8.6 m** in place of 7.35 m. At 1.0 m/s, 1.35 + 1.0 + 1.0 = **3.35 m** in place of 2.85 m. Exclusion radius: 40 + 9 + 100 = 149 m, so the rounded 150 m still holds. Also: add a carried-speed term to the drift formula, and add `COM_FAIL_ACT_T`'s 5 s to the fence and RC-loss times. The fence did not act once position was lost (G-04, W-01), so the exclusion radius has to cover that case on its own.

### Gate bounds, as measured (ET-D1-5)
Over the 10 regression missions of the fourth recording, armed, from takeoff to touchdown (9,346 ticks), with the highest of the four regressions beside it:

| Measure | Bound | Median | p99 | Worst | Worst in any of the 4 regressions |
|---|---:|---:|---:|---:|---:|
| Tick gap | 200 ms | 50.0 ms | 50.9 ms | 59.4 ms | 73.9 ms |
| Estimator age, route phase | 100 ms | 14.2 ms | 53.2 ms | 59.7 ms | 61.1 ms |
| Estimator age, settle phase | 100 ms | 26.1 ms | 59.1 ms | 59.3 ms | 60.8 ms |
| Estimator age, land phase | 100 ms | 29.6 ms | 73.8 ms | 77.4 ms | **92.2 ms** |

**So the estimator bound's margin is thin during landing.** 40 missions produced no false latch, but the worst landing tick was within 8 ms of the bound, and WO-002 already states these ages are lower bounds, because capture time uses the smallest offset seen in a run. The landing worst moved between recordings (65.6, 58.8, 92.2, 77.4 ms), and why the age rises in landing is not established. The bound stays frozen. D2 needs a real measurement of this. A latch here would be a `land` verdict on an aircraft already landing; that path was **not run**.

**Correction to an earlier draft of this report:** it gave a worst age of 44.7 ms over 7,142 ticks. That count covered only the route and settle phases, and left landing out, without saying so.

A tick gap of about 335 ms occurred in 2, 3, 4 and 4 of the 10 missions across the four regressions, always at the start of the node's log, in `stream`, before flight. On the next tick the estimator age is about 340 ms and the gate says `land`. Nothing latches, because the node is not in flight. The cause is not established.

The planner stall series brackets the setpoint bound: at 100 ms (P-01) no latch in any recording, at 500 ms (P-02) a latch at 0.24 s, and at 150 ms (P-03) a latch at a different time each recording (§4, variation). So a 150 ms stall should be treated as able to latch at any stall.

The sensor bound stays *estimated*. Its justification rests on a VIO rate not in use in this stack, and the sensor stream here is the odometry receive time, so it has no independent real source. S-01 and S-02 therefore test the gate path, not a sensor. S-02 stands in for missing depth, since this stack has no depth sensor. L-01, L-03, S-01 and S-02 are injected in the node.

### Variation between recordings
| Case | First | Second | Third | Fourth | Reading |
|---|---|---|---|---|---|
| E-01 | Fence at 42.6 m | Trigger fired; ended at 28.6 m | Fence at 42.4 m | Fence at 42.4 m | The judge failed the route in all. Whether the fence is reached is chance |
| E-03 | Radius 3.43 m | 25.84 m | 26.45 m | 3.27 m | The clamp held in all: transmitted peak 2.5 m/s, flown 2.59–2.60 m/s |
| P-03 | No latch | Hold at 0.18 s | Hold at 7.18 s | Hold at 14.18 s | A 150 ms stall can latch at any stall, or not at all in the window |
| W-01 | Drift 40.9 m | 46.1 m, peak 6.15 m/s | 41.5 m, 4.82 m/s | 42.8 m, 4.84 m/s | Wind case: one trial is not a bound |
| L-02 | — | Latch `land` | Latch `operator` | Latch `land` | PX4's Descend and the node's latch race. Either order lands |

### Every case: configured and tested
In N-01, E-03, E-04, P-01, H-03 and G-05 the Hold shown is PX4's response to the node exiting at the end of the observation window, about 1 s later. It is not a response to the fault. In E-01, E-02, H-04 and G-01 the Hold is the fence. E-01, E-02 and E-03 show "not triggered" because they do not need the trigger, and the fault acts from takeoff.

| Case | Configured | Tested (fourth recording, measured) | Deviation |
|---|---|---|---|
| N-01 Nominal hover | Stays in offboard at the hover point; the gate continues. | Hold 16.09 s; travel 0.077 m; radius 0.068 m, up 5.143 m, peak 0.064 m/s; latch none | none |
| E-01 Frame error injected: east and north swapped at the boundary | The gate cannot see a frame error. The independent judge must fail the route. It cannot hold station either, so the fault acts from takeoff; no trigger is needed. | armed; not triggered: Offboard 8.69 s, Hold 40.82 s, Land 45.82 s, disarmed 56.67 s; radius 42.429 m, up 4.999 m, peak 2.079 m/s; latch operator | none |
| E-02 Sign error injected: east flipped at the boundary | The gate cannot see a sign error. The independent judge must fail the route. It cannot hold station either, so the fault acts from takeoff; no trigger is needed. | armed; not triggered: Offboard 8.74 s, Hold 42.97 s, Land 47.98 s, disarmed 58.87 s; radius 42.857 m, up 5.01 m, peak 2.096 m/s; latch operator | none |
| E-03 Unit error injected: requests ten times too large | The gate clamps every transmitted setpoint to the frozen limits. The trigger is not needed, because the fault acts from takeoff. | armed; not triggered: Offboard 9.02 s, Hold 48.00 s; radius 3.274 m, up 5.046 m, peak 2.591 m/s; latch none | none |
| E-04 Yaw rate sign: +0.3 rad/s FLU | Positive FLU yaw rate turns counter-clockwise from above. | Hold 6.03 s; travel 0.063 m; radius 0.114 m, up 4.815 m, peak 0.047 m/s; latch none | none |
| S-01 Stale sensor data | Position valid, sensor stale: the gate holds and the node commands Hold. | Hold 0.19 s; travel 0.041 m; radius 0.09 m, up 4.697 m, peak 0.073 m/s; latch hold | none |
| S-02 Missing depth (no depth sensor in this stack; injected as a sensor stream that never updates) | As stale sensor. The gate's sensor input is what depth would feed. | Hold 0.16 s; travel 0.071 m; radius 0.058 m, up 4.721 m, peak 0.043 m/s; latch hold | none |
| L-01 Localization loss: estimator samples stop reaching the node | Estimator stale: the gate says land and the node commands Land. | Land 0.13 s, disarmed 10.55 s; travel 0.071 m; radius 0.091 m, up 4.687 m, peak 0.048 m/s; latch land | none |
| L-02 Localization loss: EKF2 stops using GPS in flight (EKF2_GPS_CTRL 0), so position goes invalid | Within EKF2_NOAID_TOUT 1 s position is invalid; the gate says land, or PX4's own failsafe lands first. | Descend 0.06 s, disarmed 10.70 s; travel 0.046 m; radius 0.095 m, up 4.809 m, peak 0.072 m/s; latch land | nav 18 within 8.0 s |
| L-03 Localization reset: a 3 m jump and a reset counter change, injected in the node | A reset in flight: the node holds and does not chase the jump. | Hold 0.08 s; travel 0.075 m; radius 0.088 m, up 4.661 m, peak 0.052 m/s; latch hold | none |
| P-01 Delayed planner, inside the bound: 100 ms stalls each second | Setpoint age stays under 200 ms; the mission continues. | Hold 11.12 s; travel 0.038 m; radius 0.093 m, up 5.095 m, peak 0.054 m/s; latch none | none |
| P-03 Delayed planner, at the edge of the bound: 150 ms stalls each second | A 150 ms stall plus a 50 ms tick can cross 200 ms. Measure whether and when it latches. | Hold 14.18 s; travel 0.037 m; radius 0.047 m, up 5.046 m, peak 0.042 m/s; latch hold | none |
| P-02 Delayed planner, over the bound: one 500 ms stall | Setpoint age passes 200 ms: the gate holds. The latch stays after the planner recovers. | Hold 0.24 s; travel 0.042 m; radius 0.064 m, up 4.671 m, peak 0.056 m/s; latch hold | none |
| H-01 Stale setpoint while the heartbeat continues, gate response on, at 1.0 m/s | Heartbeat is not freshness. The gate holds and the node commands Hold. | Hold 0.23 s; travel 1.23 m; radius 5.707 m, up 4.909 m, peak 1.087 m/s; latch hold | none |
| H-02 Stale setpoint while the heartbeat continues, gate response on, at 2.5 m/s | As H-01 at the GPS limit. | Hold 0.18 s; travel 3.531 m; radius 17.086 m, up 4.817 m, peak 2.64 m/s; latch hold | none |
| H-03 Control: setpoints stop, heartbeat continues, no gate response, at 1.0 m/s | Measure what PX4 does alone. docs/OPERATING_ENVELOPE.md says the last setpoint may be applied throughout. | Hold 13.04 s; travel 12.138 m; radius 18.452 m, up 5.188 m, peak 1.062 m/s; latch none | none |
| H-04 Control: setpoints stop, heartbeat continues, no gate response, at 2.5 m/s | As H-03. The fence is the only limit left, so this also shows that. | Hold 10.64 s, Land 15.64 s; travel 29.88 m; radius 43.654 m, up 5.232 m, peak 2.59 m/s; latch none | none |
| C-01 Lost command stream, no manual control at arming, at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.08 s; travel 2.067 m; radius 6.554 m, up 4.756 m, peak 1.101 m/s; latch operator | none |
| C-02 Lost command stream at 2.5 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.11 s; travel 5.921 m; radius 19.702 m, up 4.829 m, peak 2.624 m/s; latch operator | none |
| C-03 Companion death: the node is killed at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.16 s; travel 2.155 m; radius 6.636 m, up 4.961 m, peak 1.075 m/s; latch none | none |
| C-04 Network interruption: the agent stops at 1.0 m/s | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.23 s; travel 2.255 m; radius 6.733 m, up 4.723 m, peak 1.082 m/s; latch land | none |
| C-05 Stale climb at the vertical limit, stream lost | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold. Measure the height gained. | Hold 1.07 s; travel 0.059 m; radius 0.05 m, up 7.065 m, peak 0.043 m/s; latch operator | none |
| C-06 Stale descent at the commanded limit, stream lost | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold. Measure the height lost. | Hold 1.08 s; travel 0.057 m; radius 0.097 m, up 11.736 m, peak 0.084 m/s; latch operator | none |
| B-01 Low energy: fast simulated drain | COM_LOW_BAT_ACT 3: Return at critical (0.35), Land at emergency (0.15). | Hold 11.33 s, Return 16.34 s, Land 19.37 s, disarmed 26.97 s; travel 0.074 m; radius 0.106 m, up 4.768 m, peak 0.05 m/s; latch operator | none |
| R-01 Operator takeover by the mode switch, at 1.0 m/s | The mode switch moves to Position; the node stops commanding. | Position 0.09 s; travel 0.913 m; radius 5.297 m, up 4.857 m, peak 1.147 m/s; latch operator | none |
| R-02 Operator takeover by the sticks, COM_RC_OVERRIDE 3 | Moving the sticks in offboard switches to Position; the node stops commanding. | Position 0.04 s; travel 8.444 m; radius 14.646 m, up 4.737 m, peak 1.073 m/s; latch operator | none |
| R-03 Kill switch in flight | Motors stop at once; the aircraft falls; disarm follows at COM_KILL_DISARM 5 s. | disarmed 5.10 s; travel 0.01 m; radius 0.089 m, up 4.623 m, peak 0.07 m/s; latch none | none |
| R-04 RC removed in flight, with manual control present at arming | NAV_RCL_ACT 2 Return. With offboard not excepted from RC loss (COM_RCL_EXCEPT 0). | Hold 0.48 s, Return 5.48 s; travel 4.544 m; radius 5.952 m, up 5.673 m, peak 2.655 m/s; latch operator | nav 5 within 2.0 s |
| R-05 Lost command stream with manual control present at arming | px4 offboard loss, COM_OF_LOSS_T 1.0 s, then COM_OBL_RC_ACT 5 Hold | Hold 1.06 s; travel 2.079 m; radius 6.496 m, up 4.815 m, peak 1.086 m/s; latch operator | none |
| R-06 Operator reaction in the drift case: Altitude mode after estimator position loss | Altitude mode stays selected and holds height until commanded. Measure the height change. | Descend 0.32 s, Altitude 2.12 s; travel 1.579 m; radius 1.895 m, up 4.616 m, peak 0.14 m/s; latch operator | none |
| K-01 Hold braking from 2.5 m/s | Measure stop distance; replaces the envelope's estimate. | Hold 0.23 s; travel 3.693 m; radius 17.28 m, up 4.946 m, peak 2.635 m/s; latch hold | none |
| K-02 Hold braking from 1.0 m/s, with MPC_XY_VEL_MAX 1.0 | Measure stop distance at the VIO-stage limit. | Hold 0.24 s; travel 1.198 m; radius 5.7 m, up 4.907 m, peak 1.089 m/s; latch hold | none |
| G-01 Geofence breach, horizontal, at 2.5 m/s | GF_ACTION 5 Land at 40 m. Measure the overrun. | Hold 16.70 s, Land 21.70 s, disarmed 32.48 s; travel 43.836 m; radius 43.819 m, up 4.914 m, peak 2.602 m/s; latch operator | nav 18 within 20.0 s |
| G-02 Geofence breach, vertical, at 1.0 m/s | GF_ACTION 5 Land at 14 m. Measure the overrun. | Hold 11.51 s, Land 16.51 s, disarmed 40.77 s; travel 0.099 m; radius 0.069 m, up 14.588 m, peak 0.064 m/s; latch operator | nav 18 within 14.0 s |
| G-03 Home invalid at arming: EKF2 with no GPS from start | COM_ARM_WO_GPS 0: arming denied. | never armed | none |
| G-04 Fence with position lost mid-flight: EKF2 stops GPS at about 32 m, with the drift reaching past 40 m | Record the mode entered and whether the fence still acts. Raw GPS stays live here; a lost receiver is not injectable on this stack. | Descend 0.28 s, disarmed 10.36 s; travel 12.669 m; radius 44.068 m, up 4.884 m, peak 2.602 m/s; latch none | none |
| G-05 Moved takeoff point: spawned 20 m east | The fence is centred on Home, so 30 m from the new Home stays inside. | Hold 6.17 s; travel 0.283 m; radius 50.39 m, up 5.116 m, peak 2.611 m/s; latch none | none |
| T-01 Return against the ceiling at the GPS limit | RTL_RETURN_ALT 10 m; no breach of the 30 m ceiling; speed obeys MPC_XY_VEL_MAX 2.5. | Return 0.07 s, disarmed 30.78 s; travel 13.645 m; radius 16.34 m, up 9.958 m, peak 2.688 m/s; latch operator | none |
| T-02 Return at MPC_XY_VEL_MAX 1.0 | Speed obeys 1.0 m/s. | Return 0.25 s, disarmed 15.98 s; travel 4.521 m; radius 5.498 m, up 4.812 m, peak 1.153 m/s; latch operator | none |
| T-03 Full-stick Position at MPC_XY_VEL_MAX 2.5 | Position mode obeys 2.5 m/s at full stick. | Position 0.09 s; travel 20.682 m; radius 26.198 m, up 4.746 m, peak 2.5 m/s; latch operator | none |
| T-04 Full-stick Position at MPC_XY_VEL_MAX 1.0 | Position mode obeys 1.0 m/s at full stick. | Position 0.10 s; travel 8.569 m; radius 10.783 m, up 4.82 m, peak 1.006 m/s; latch operator | none |
| W-01 Wind: drift during a descent after EKF2 stops GPS | Measure horizontal drift to the ground in simulated wind. | Descend 0.11 s, disarmed 17.24 s; travel 42.754 m; radius 42.784 m, up 9.758 m, peak 4.843 m/s; latch land | none |
| V-01 Vision only (gz_x500_vision, EKF2_GPS_CTRL 0, global origin set): offboard loss | Record the mode entered. Confirm aiding is off. Hold if global position stays valid. | never armed | fault injected |
| V-02 Vision only, origin wrong by under 40 m | Record what the fence does. | never armed | fault injected |
| V-03 Vision only, origin too high | Record what the fence does. | never armed | fault injected |
| V-04 Vision only, no origin | Expected to be refused at arming. | never armed | none |
| V-05 SYS_HAS_GPS 0 | Expected to be refused at arming. | never armed | none |

### Run IDs (fourth recording)
N-01 `20261101T105612Z_aaa2dd17`, E-01 `20261101T105708Z_c07a82c8`, E-02 `20261101T105822Z_564e9875`, E-03 `20261101T105938Z_eddc8f98`, E-04 `20261101T110042Z_b0963f08`, S-01 `20261101T110128Z_f6d29bfa`, S-02 `20261101T110219Z_33e77381`, L-01 `20261101T110310Z_83dc34aa`, L-02 `20261101T110416Z_f97f6d1d`, L-03 `20261101T110537Z_40b2dbfa`, P-01 `20261101T110628Z_57b2db9e`, P-03 `20261101T110719Z_29d06196`, P-02 `20261101T110821Z_ecbe0008`, H-01 `20261101T110912Z_8187bfa7`, H-02 `20261101T111005Z_e5abb2e6`, H-03 `20261101T111059Z_623cb884`, H-04 `20261101T111154Z_aab44f9d`, C-01 `20261101T111259Z_23f957f1`, C-02 `20261101T111354Z_ffc40f9f`, C-03 `20261101T111450Z_f640bac2`, C-04 `20261101T111545Z_083cc6c2`, C-05 `20261101T111640Z_0846d6a8`, C-06 `20261101T111728Z_bfd3d6c2`, B-01 `20261101T111842Z_c57cae8c`, R-01 `20261101T112033Z_ba529291`, R-02 `20261101T112126Z_a08c322c`, R-03 `20261101T112219Z_63bb3d04`, R-04 `20261101T112310Z_9cee0db4`, R-05 `20261101T112408Z_aa81303f`, R-06 `20261101T112504Z_cdd4ffc4`, K-01 `20261101T112610Z_03ba9d55`, K-02 `20261101T112704Z_4947ca0f`, G-01 `20261101T112757Z_5d24f0ff`, G-02 `20261101T112910Z_d6c90d46`, G-03 `20261101T113031Z_8b866808`, G-04 `20261101T113135Z_e6d7dd5c`, G-05 `20261101T113257Z_cc5bde49`, T-01 `20261101T113353Z_05ccc2b6`, T-02 `20261101T113507Z_ee472972`, T-03 `20261101T113616Z_5c5e84e5`, T-04 `20261101T113707Z_c062011e`, W-01 `20261101T113758Z_02c88488`, V-01 `20261101T113929Z_6df50147`, V-02 `20261101T114048Z_e252e762`, V-03 `20261101T114207Z_44335a7c`, V-04 `20261101T114326Z_0c22712a`, V-05 `20261101T114430Z_428a541f`

Regression at the fixed commit: `20261101T114534Z_c9f24edc`, `20261101T114646Z_e0ede21d`, `20261101T114758Z_9d1f54ee`, `20261101T114911Z_b661f969`, `20261101T115023Z_45f4cf13`, `20261101T115135Z_c80335a3`, `20261101T115247Z_bae3698c`, `20261101T115400Z_ce353427`, `20261101T115512Z_52929ef7`, `20261101T115624Z_2cb08618`.

## 5. Failure analysis
### The node overrode the operator (first recording, fixed)
**What happened.** In the first recording R-06 passed its check, "Altitude within 4 s", at 2.10 s. The log showed Altitude lasted 84 ms before the aircraft returned to Descend and landed. PX4's log repeats "Landing at current position" once a second. The fault was in the agent's code, not PX4: the node had latched `land`, PX4 was flying that as Descend, and Descend was not counted as the target. So the node kept repeating Land, including over the operator's switch. The protocol says always allow operator takeover, so this was a safety defect.

The check passed because it asked only whether the mode was entered.

**Fix.**
- The node now commands only while the vehicle is in the state it decided from, and any other state is the operator or PX4. Descend counts as the land response (ADR-0009, `src/banshee/offboard/response.py`).
- In the nominal `land` phase, Land repeats only while the vehicle is still in Offboard (`src/banshee/offboard/mission.py`).
- `holds_s` was added to the checks, and to the takeover cases.

**Evidence.** In the fourth recording R-06 stays in Altitude from 2.12 s to the end of the window, 22.88 s against the 15 s check, with `final_latch` operator. First-recording failure: `20261101T080344Z_1245da95`. New unit tests cover each path.

**Not measured:** the nominal `land` phase change has no fault case. The 40 regression missions show landing still works. If PX4 leaves offboard first in a nominal landing, the node yields and sends no Land, by design. An operator takeover during a nominal landing was **not run**.

**Retro.** Read the timeline, not just the check, for every case; this finding came from doing that. A check that a state was reached says nothing about whether it lasted.

### A fix for a review finding broke R-06 (third recording, fixed)
**What happened.** The review found that the node re-armed over the operator in `stream`. The fix stopped repeating commands after the first arm. In R-06 at `2ce9126` PX4 had refused the mode, so the node armed in Hold, stopped asking, never reached offboard, and PX4's preflight check disarmed it: `20261101T102246Z_c14f509c`. Nothing flew, and the check reported it as deviations.

**Fix.** `arming_step` (`src/banshee/offboard/response.py`, commit `9a2571f`) enters offboard first, arms only from offboard, and sends neither after the first arm. Recorded again; R-06 flew.

**Retro.** A change to the arming path is not covered by the fix's unit tests alone. Only the recording showed this, so any later change there needs one.

### A gap in the scope
The WO asks for one contract export per case, and the first recording had none. `run_matrix.export_case` now writes one to `data/derived/d1-faults/<run id>`. What an export means here:
- Success means "as specified", not "route flown".
- `tolerance_m` is 0 in those rubrics, because the case's checks are held in `outcome.json`.
- `terminated` means disarmed, which includes the kill switch.
- `context.mode` is the node's phase, and `context.intervention` is null, because the latch cannot tell the operator from PX4.

### What the deviations have in common
Four of the seven are expected values that the frozen matrix had wrong about PX4 (L-02, plus the 5 s hold in R-04, G-01 and G-02), and the vehicle reached the specified outcome in each, some seconds later in the last three. The other three are the vision cases, which show nothing about the specified response.

### Weak checks and controls
Passing these says less than the row suggests:
- E-01 and E-02 pass on any failure of the judge. They do not show why it failed.
- R-03's check is only "not armed at the end". Ground truth shows the aircraft fell in about 1.2 s, with disarm at 5.10 s.
- `holds_s` looks only up to the end of the observation window.
- G-04 is PX4 alone, with the gate response off, as are the controls H-03 and H-04.

### Other behaviour worth knowing
- C-04 (the agent stops): the node latches `land`, but cannot reach PX4. PX4's own Hold at 1.23 s is the response. What happens after Hold when the link never returns was **not run**, apart from low energy in B-01.
- G-05: the fence moves with Home. At 30 m from the moved Home, 50.4 m from the world origin, it does not act, as the envelope said.
- G-03: arming is refused with no global position.

### Landing offset (carried here by WO-002, still open)
The aircraft lands 0.34–0.44 m from the route's end by ground truth in the fourth regression, and 0.33–0.49 m across all four, against 0.31–0.43 m at WO-002's close. This WO found no cause for what remains. The D3 landing zone should allow for it.

### Carried over from WO-002's review (unchanged, open)
- A corrupt ULog aborts a campaign rather than recording a failure.
- A sample dropped by the frame guard is not logged.
- The settle phase reads a velocity that can be stale.
- Mode and arm commands do not pass the freshness gate.
- The node's timeout stops it without a land command.
- Before flight, no operator input was tested. The node now repeats its mode command until PX4 accepts, and arms once from offboard.

## 6. Cost and latency
No paid compute and no spending, so there is no cost record. Each recording took about 49 minutes of VM time for 47 cases, and the 10 regression missions about 12 minutes. Gate reaction, from fault to Hold or Land: 0.08–0.24 s (S, L-01, L-03, P-02, H, K).

## 7. Sealed access
None.

## 8. Exit tests and acceptance
| Exit test | Threshold (frozen) | Result | Evidence | Pass? |
|---|---|---|---|---|
| ET-D1-4 | All cases executed; deviations reported; configured and tested distinguished | 47/47 executed, 41 with the fault in flight, 6 never armed; 7 deviations reported | `runs/fault-matrix-recorded-4/matrix.jsonl`, §4 | yes |
| ET-D1-5 | Gate with frozen bounds in the command path, unit-tested; heartbeat ≠ freshness; bounds justified | Gate in the path; tests green; H-01 to H-04 show the difference; setpoint and estimator bounds measured against flight, with the landing margin thin; sensor bound still estimated | `tests/test_freshness.py`, `tests/test_faults.py`, §4 | yes |

Phase D1 is `passed` once ET-D1-1 to 5 are all recorded, after the independent review (`AGENTS.md §13.9`, §10 below).

## 9. Limits
- Simulation only. Nothing here shows flight readiness, and real links, RC hardware and sensors were not used. Real link cuts belong to D2.
- One trial per case in each recording. §4's variation table shows that a trial is not a bound, most of all in wind.
- Simulated RC arrives through `RC_CHANNELS_OVERRIDE`, not a receiver. Stick and switch latency here says nothing about a radio.
- **Not run:** vision-only flight, and with it the origin-error cases and the 0.5 m `COM_POS_FS_EPH` setting; takeover during a nominal landing; takeover before flight; a false latch during landing; long-duration Hold after link loss; QGroundControl, and the second clean build, carried from WO-002.
- World wind was one setting, 5,2,0 m/s, with no gusts.

## 10. Independent review
Under `AGENTS.md §13.9`. A second agent, in a fresh session and a clean clone, reviewed the branch at `50406c3` (second recording) with no access to this author's reasoning. It reported no blockers. Each finding was checked against the code or logs before acting on it.

| Finding | Verified | Outcome |
|---|---|---|
| Never-armed cases never sent an arm command, so "never armed" tested nothing | Yes, and 6 cases, not the 5 reported | Fixed in `2ce9126`: 25 arm commands each, refusals logged |
| A Hold latch could get stuck, because the phase still advanced to land | Yes | Fixed in `2ce9126` |
| In `stream` the node could re-arm over the operator | Yes | Fixed in `2ce9126` and `9a2571f` (§5) |
| `transmitted` was logged before the frame fault was applied | Yes | Fixed in `2ce9126`; what is sent is what is logged |
| Fault episodes' notes described a nominal mission | Yes | Fixed in `2ce9126` |
| The headline overstated how many cases flew | Yes | §1 and §4 now separate them |
| Number errors: R-06's measure undefined, W-01's estimate 75 m, ranges inconsistent | Yes | Corrected from the recordings by script |
| Items to disclose (5 s hold in B-01, weak checks, what the export fields mean, dirty flag, 336 ms gap, parameter not read back) | Yes | Disclosed in §3, §4 and §5 |

The recheck of the fixes is recorded below.

