# WO-002 — D1 SITL: pinned launch, offboard velocity mission, independent outcome, contract export

**Status:** in progress. No exit test has run. Later results are appended below, dated.
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-002 · **Phase:** D1 · **Protocol version:** `evals/D1-exit-tests.json`, sha256 `1f4900194371c9124b3aa0e6ef29c438d947fe931fc513baba698948ae758180` when frozen
**Program link:** PROGRAM §5.1, §6 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## Incident, 2026-10-31: setup filled the owner's disk
**Impact.** The Mac's disk filled, and the Mac then quit unexpectedly at about 21:45 PDT. The link between the two is likely but not proven: no shutdown cause was found in the system log. All four repositories are intact and the Mac has about 90 GB free (owner's check). The other agents' work was not affected (owner). This repository's ledgers parse and `git fsck` is clean (measured). Setup logs and scratch files were lost in the reboot's `/private/tmp` cleanup, including the two logs that were the direct evidence of this incident. The full account, with paths, is in `ledgers/corrections.jsonl`. No run record was lost, because no run had happened.

**Cause.** The fault was the agent's.
- `provision.sh` ran `DONT_RUN=1 make px4_sitl gz_x500`, expecting a build. PX4 appears to have started anyway. With no terminal, its `pxh>` prompt repeated without end. The cause of the prompt loop is read from what the log showed before the crash; the log itself is gone.
- The agent sent that output to a log file on the Mac, with no size cap and no time limit, which `AGENTS.md §8.8` requires. The log reached at least 34,249,662,532 bytes (measured, shortly before the disk filled).
- A status check shortly before saw the repeating prompt at the end of the log, and did not look at its size.

**Fix.**
| Bound | Where | Evidence |
|---|---|---|
| Build only: `make px4_sitl_default` | `provision.sh` | the build completed in the partial rerun, and PX4 did not start (measured) |
| 200 MB log cap, which stops the run | `banshee.sitl.bounded` on the host; `head -c` in the VM | `tests/test_sitl_bounded.py`: a chatty process, and a prompt loop like this one, each stop at the cap, and so do their children (measured) |
| 3-hour limit | `banshee.sitl.bounded`; `timeout` in the VM | same test file (measured, with a short limit) |
| No stdin | both | same test file (measured) |
| Refuses to start under 20 GB free, on the host or in the VM | `banshee.sitl.bounded` | same test file for the refusal; `run_provision.sh` passes `--vm` |
| VM disk fixed at 60 GiB | `banshee-sitl.yaml` | read back from the VM on restart |

The VM disk cap would not have stopped this incident, because the log was on the host. The log cap is what prevents a repeat.

**Disclosure.** After the crash the agent reran setup with the first three bounds. The owner then asked for this work to be done before any rerun, and the agent stopped that run, which had reached the agent build.

**Retro.** Check size as well as content when checking a log. Treat "will only build" as something to confirm, and keep bounds on regardless.

## Results
Not run. Later entries follow.

## Results, 2026-10-31
**Status:** ET-D1-1, ET-D1-2 and ET-D1-3 met on the frozen thresholds, in simulation. ET-D1-4 and ET-D1-5 belong to WO-004. A simulation pass is not flight readiness. No hardware was connected and nothing was bought.

### Claim and scope
A locked PX4, Gazebo and ROS 2 stack launches from a script on arm64, flies a declared route through the offboard velocity interface, and each run is judged by separate code and exported as a valid contract episode. This covers nominal flight only.

### Frozen method
`evals/D1-exit-tests.json`, unchanged. `evals/D1-route.json` (take off to 5 m, a 10 m square, return, land) was committed before the counted runs. Two trial runs used the same route first, and they stay in the record and out of the count.

### Reproduction
Counted runs flew at commit `9019ae44d6789d0ad5a489af0be946393d6fd6ad`, the judge included. `PYTHONPATH=src` throughout.
- `python -m banshee.sitl.launch --check-versions`, in the VM.
- `python -m banshee.sitl.campaign --runs 10`, through `banshee.sitl.bounded`.
- `python -m banshee.outcome.truth_check --ulog <file>`, with `pyulog==1.2.0` in a separate environment.
- `ironclad-validate data/derived/d1/<run id>/episode.json`.
- `bash src/banshee/sitl/vm/compile_target.sh`, in the VM.

Run IDs: `20261101T051934Z_1779f115`, `20261101T052044Z_cafc3dbe`, `20261101T052154Z_b31db8c4`, `20261101T052305Z_a3e94dbd`, `20261101T052415Z_de2eed0c`, `20261101T052525Z_b79f5090`, `20261101T052635Z_2c0e17bf`, `20261101T052746Z_10797ffa`, `20261101T052856Z_b056a02c`, `20261101T053006Z_e82b546f`. Evidence is on the owner's Mac, in the ignored `runs/` and `data/derived/d1/`; `ledgers/runs.jsonl` records each run.

### Results
All measured, in the VM.

| Measure | Result |
|---|---|
| Launches with identical versions | 12/12 (10 counted, 2 trials); 7 pins, none null |
| Lock refusal | exit 1 with a changed `px4` pin; exit 0 with the real lock |
| Missions completed | 10/10; 95% Wilson interval 0.722 to 1.000 |
| Closest approach per waypoint, from the logged estimate | median 0.041 m, worst 0.202 m, tolerance 0.5 m |
| Closest approach per waypoint, from Gazebo ground truth | 0.026 to 0.164 m |
| Estimate against ground truth | median 0.09 to 0.12 m per run, worst 0.40 m |
| Episodes valid | 10/10 by `ironclad-validate` |
| Frozen parameters read back from PX4 | 21 of 21 match, in all 10 runs |
| Transmitted setpoints over the limits | 0; fastest horizontal speed flown 2.11 m/s, limit 2.5 |
| Tick spacing after the first tick | p50 50.0 ms, p95 50.5, p99 50.8, max 53.9 |
| Decision to publish return | p50 183 µs, p95 450 µs, max 334 ms (the first tick) |
| Observation age at decision | p50 10.0 ms, p95 32.3, max 347 ms (the first tick); a lower bound, per ADR-0005 |
| Flight log span | 47.2 to 47.5 s per run |
| `px4_msgs` against PX4's `msg/` | 235 files identical, 0 different |
| `make px4_fmu-v6x_default` | builds, 1,824,680 bytes, sha256 `a8e6b8d4…3008`; flash 99.70% used; compile only |

Ground truth passes through each waypoint in the commanded directions, so the frame conversion holds on real simulated motion as well as in `tests/test_offboard.py`.

### Failure analysis
- **Trial 1, 0/5 waypoints (run `20261101T051322Z_10bc58fd`).** PX4 refused to arm: "No connection to the GCS". `gz_x500` raises the default of `NAV_DLL_ACT` to 2 after the `PX4_PARAM_` overrides run. Setting 0 through the override is lost, because 0 was still the default then. `run_mission.sh` now sets it after the airframe runs and reads back every value. Any other parameter could fail the same way, so the read-back file in each run is the evidence for configured values, not the override list. Trial 1 exported as a failed episode.
- **Trial 2 passed (run `20261101T051742Z_49b6cc47`), and showed a bad metric.** Closest approach read about 0.47 m because the judge moved on at the first sample inside tolerance. It now keeps a waypoint current until the aircraft leaves its tolerance. This changed no pass or fail among the counted runs. It would miss a repeated waypoint that the aircraft never leaves; this route has none.
- **A one-tick stall of about 334 ms** at the first tick in 3 of 10 counted runs, before arming. The gate held that one setpoint back as stale and logged why, which is correct. The likely cause is the first publish, which is not confirmed.
- **Unexplained: the aircraft lands about 0.9 m from the end of the route.** It enters Land within 0.25 m, then moves about 1.1 m south in the upper part of the descent, in every run. It ends 0.82 to 0.99 m from the route's end by ground truth, so this is real motion and not estimator error. There is no wind in this world, and no setpoint from this project is sent during Land. The cause is not known. ET-D1-2 does not cover landing position, but the D3 landing zone should not ignore it, so WO-004 takes it.

### Deviations from the work order and ADR-0007
- The work order names `banshee.offboard.mission --runs 10 --out runs/`. Runs go through `banshee.sitl.campaign`, because each run needs a fresh simulator started from the host.
- `offboard_stream_before_switch_s` is frozen at 1.0. The mission streams for 1.5 s, which is above that minimum.
- Two settings are not in the frozen list: `COM_RC_IN_MODE=4` and `COM_RCL_EXCEPT=4`, for a simulator with no RC. They are not values for the aircraft, and WO-004 must also test with simulated manual control, as ADR-0007 says.
- ADR-0007 asks for a build from a clean start twice. The stack was built from clean once, plus one partial rerun. **Not run:** a second clean build.
- **Not run:** QGroundControl connecting to SITL. No exit test depends on it.
- Each run's `git.json` says `dirty: true`, because `ledgers/runs.jsonl`, which the runs write, was untracked. It was the only untracked or changed path before and after the campaign.

### Cost and latency
$0. All local. One campaign took 11 minutes, about 70 s per run including simulator start and teardown.

### Sealed access
None.

### Exit tests
| Exit test | Threshold | Result | Evidence | Pass? |
|---|---|---|---|---|
| ET-D1-1 | 2/2 launches identical; zero null pins | 12/12; zero null | `versions.json` per run | yes |
| ET-D1-2 | 10/10 reach every waypoint within 0.5 m, by independent code | 10/10; worst 0.202 m | `banshee.outcome.waypoints` per run | yes |
| ET-D1-3 | 100% contract valid | 10/10 | `ironclad-validate` | yes |

### Limits
- The judge reads PX4's estimate, because that is what the log holds, while the episode's assessment method is `independent_sim_state`, the closest value the contract offers. The ground-truth check supports the result but is not part of the pass decision, and the episode notes say so.
- The route planner runs inside the same tick as the gate, so setpoint freshness is met by construction here. A stale or lost stream is untested until WO-004.
- The gate holds a setpoint back, and the mission takes no other action on a hold or land verdict. PX4's offboard loss is meant to act next, and that is also untested until WO-004.
- The 6X build leaves 0.3% of flash free, so adding anything to that firmware means removing something else.
- Capture times use the smallest offset seen in a run, so measured ages are lower bounds. D2 needs a real measurement.
- Physics in Gazebo on an arm64 VM says nothing about the real aircraft's behaviour.

### Next bounded work order
WO-004: the fault matrix and ET-D1-4, ET-D1-5, plus the landing offset above.

### Retro note
The first trial cost little because it was bounded and logged. Reading the parameters back found a silent no-op that the override list had hidden. Checking the judge's numbers against ground truth, not only pass or fail, is what exposed the metric error early enough to fix before the counted runs.

## Review and final runs, 2026-10-31
The full review required by `AGENTS.md §13.9` ran on a clean clone: an independent agent, read-only, with `make check` green there and numbers recomputed from raw evidence. It found no blockers. Its findings were checked against the data, and the fixes below went in. Then the 10 missions were flown again on the final code. **These 10 are the runs of record for the exit tests.** The first 10 also passed, and stay in the record.

### What the review changed
| Finding | Checked | Outcome |
|---|---|---|
| The campaign counted a win without looking at the VM's exit code | read in the code; the first 10 all logged `mission exit 0`, so their count stands | success now needs a clean run |
| The episode said `independent_sim_state`, while the judge read PX4's estimate | true, and already disclosed, but the field itself was wrong | success now also needs Gazebo ground truth, in route order, so the field is true. `pyulog` is now the `sitl` extra, needed only to run missions |
| The closest-approach check on ground truth ignored order, and a square looks alike with x and y swapped | true | the check is now ordered, with a test for reversed and swapped tracks |
| The episode's simulator version was the `gz-harmonic` package version | true | now `gz_sim` 8.15.0 |
| Observations were marked valid even with an invalid estimator | true; no flown step had one | now invalid, with no value |
| An export error would stop the campaign and leave a run "started" | read in the code | now a failed run |
| `gz sim` had no time limit of its own | none left over in the VM, but a killed caller would skip the trap | a watchdog now stops all three at 295 s |
| Odometry frames were assumed to be NED | mid-route velocity matches position change in sign and size (east 2.05 against 1.94 m/s) | a sample in another frame is now dropped, so the gate holds |
| The landing offset has a likely cause | **true**: in all first 10 runs the aircraft entered Land at about 1.4 m/s south, on the final leg's heading, against a request near 0.3 m/s | a settle phase now brakes before Land. The offset fell from 0.83–1.00 m to 0.31–0.43 m, which supports the cause. About 0.3 m south remains and is not explained |

**Correction to "Results, 2026-10-31".** The end offset there, 0.82 to 0.99 m, should read 0.83 to 1.00 m: it read one axis. "The cause is not known" is replaced by the row above. That section's 10 episodes keep the old simulator version and a judge based on the estimate alone, so **use the final 10 episodes, not those**.

### Accepted, not changed here
All go to WO-004, unless marked:
- Setpoint age is always 0 in the mission, because the planner runs in the gate's tick, so the 200 ms bound is never exercised in flight.
- No test covers the mission node's wiring. `enu_to_ned` and `ned_to_enu` are the same function, so calling the wrong one would pass. Ground truth does catch a wrong axis.
- A non-zero yaw rate has never flown, because guidance requests 0. The sign is tested only as a pure function.
- Mode switch and arm commands skip the freshness check.
- When the mission hits its time limit it exits with no land command. In simulation PX4's offboard loss should then act, which is untested.
- Not for WO-004, and unchanged: `valid_until_t_ns` is the gate's bound and is filled in for steps that were not sent, since the contract requires a time. `restore_mode` is `initial_state_only`, the only value the contract allows, although `initial-state.json` holds only the first position and the world name, so an episode cannot be restored from it.
- The ULog stays under `runs/` and not inside the episode. The work order asks for it to be retained, and it is, at about 55 MB per run.

### Final results
Commit `dd2e610603a5b0bc29aaf1aa565c49ae1dea791d`. All measured, in the VM. Run IDs: `20261101T054322Z_3b0d572c`, `20261101T054434Z_908f01fc`, `20261101T054545Z_463db2fd`, `20261101T054657Z_94dcdf21`, `20261101T054808Z_40ad1133`, `20261101T054920Z_c4759c8d`, `20261101T055032Z_d3cf33d9`, `20261101T055143Z_f412d3f2`, `20261101T055255Z_8dd65595`, `20261101T055406Z_81c79653`.

| Measure | Result |
|---|---|
| Missions completed, on estimate and ground truth and a clean run | 10/10; 95% Wilson interval 0.722 to 1.000 |
| Closest approach per waypoint, in route order, from the logged estimate | median 0.052 m, worst 0.210 m, tolerance 0.5 m |
| Closest approach per waypoint, in route order, from Gazebo ground truth | 0.035 to 0.267 m, median 0.110 m |
| Episodes valid | 10/10 by `ironclad-validate` |
| Launches with identical versions, all runs on this machine | 22/22; 7 pins, none null |
| Lock check | exit 0 with the real lock; exit 1 and refusal with a changed `px4` pin (`runs/lock-and-msgs-evidence/lock-check.log`) |
| `px4_msgs` against PX4's `msg/`, by `compare_msgs.sh` | 235 identical, 0 different (same folder) |
| Frozen parameters read back from PX4 | 21 of 21 match, in all 10 runs |
| Transmitted setpoints over the limits | 0; fastest horizontal speed flown 2.11 m/s, limit 2.5 |
| Highest point by ground truth | 5.21 m |
| Tick spacing after the first tick | p50 50.0 ms, p95 50.5, p99 50.8, max 57.6 |
| Decision to publish return | p50 166 µs, p95 450 µs, max 334 ms (the first tick) |
| Observation age at decision | p50 10.5 ms, p95 44.5, max 341 ms (the first tick); a lower bound, per ADR-0005 |
| Settle phase | 0.80 to 0.85 s |
| Landing offset from the route's end, by ground truth | 0.31 to 0.43 m |

The first-tick stall appeared in 2 of these 10 runs. As before, it was before arming, and the gate held that one setpoint back. Running `git.json` shows `dirty: true` for the same reason as before: the runs append to `ledgers/runs.jsonl`.

### Exit tests, runs of record
| Exit test | Threshold | Result | Pass? |
|---|---|---|---|
| ET-D1-1 | 2/2 launches identical; zero null pins | 22/22; zero null | yes |
| ET-D1-2 | 10/10 reach every waypoint within 0.5 m, by independent code | 10/10; worst 0.210 m by estimate, 0.267 m by ground truth | yes |
| ET-D1-3 | 100% contract valid | 10/10 | yes |

The 6X compile check, the limits and the "not run" items in "Results, 2026-10-31" still apply, except that the judge's limit on ground truth is now closed. The compile ran at the same locked PX4 commit, and `compile_target.sh` did not change.
