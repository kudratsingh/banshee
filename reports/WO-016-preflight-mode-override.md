# WO-016 — The node yields to a mode chosen while disarmed

**Status:** passed
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-016 · **Phase:** D1 (a safety defect found in WO-004), before anything in D2
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Every result here is from simulation.

## 1. Claim and scope
Before flight, the node no longer takes the aircraft out of a mode the operator chose. It asks for offboard only from Hold, and it yields on any other state, on leaving offboard once in it, or on being armed outside offboard. This was one recording of the matrix at commit `0016b7c`, then 10 regression missions, as the owner instructed. ET-D1-4 and ET-D1-5 stay passed; this does not reopen them.

## 2. The defect and the fix
WO-004's node sent the offboard command whatever mode it found, repeating until PX4 accepted, then armed. An operator who selected Position while the node streamed was overridden and the aircraft flew.

| R-07, simulation (measured) | Run | What happened |
|---|---|---|
| Old logic, debug pass on uncommitted code | `20261101T224134Z_5db327be` | Position selected, node forced Offboard, armed, flew. Three checks deviated: nav 2 within 60 s, never armed, final latch |
| Fix, debug pass on uncommitted code | `20261101T224056Z_4114c67c` | Hold, Position at 11.92 s, never offboard, never armed, latch `operator` |
| Fix, recording of record at `0016b7c` | `20261101T231516Z_053eca03` | Hold, Position at 12.10 s, never offboard, never armed, no arm command sent, latch `operator`. All four checks match |

So R-07 fails on the old logic and passes on the fix. The old-logic run needed a local revert, so it is not reproducible from a commit; its logs are in `runs/r07-debug/`.

## 3. Results of this recording
`evals/D1-fault-matrix.json`, sha256 `4940861a9f1c030992e025917dffe6345832fc12eede04edccd3d65535b128bf`: 48 cases, 47 from WO-004 plus R-07.

| Check | Result | Label |
|---|---|---|
| Executed, with one log and one valid contract export each | 48/48; no invalid exports | measured |
| Mode sequence, compared with WO-004's fourth recording | identical in all 47 earlier cases | measured |
| Whether armed, whether triggered, final latch | unchanged in all 47 | measured |
| Deviations | the same 7 as the fourth recording: L-02, R-04, G-01, G-02, V-01, V-02, V-03. R-07 adds none | measured |
| Regression missions | 10/10 succeeded, 5/5 waypoints by the independent judge | measured |
| Estimator age while armed, regression missions | median 10.5 ms, p99 19.8 ms, worst 24.0 ms, n = 9,357 | measured |

The stop condition, a case that armed in WO-004 ceasing to arm, did not occur.

Radii and speeds moved by small amounts, as they do between recordings. R-06 moved the most, its maximum radius going from 1.895 m to 0.402 m. WO-004 reports its drift by two measures for this reason. The fix does not act on R-06 once armed, so I read this as run-to-run variation, though one recording cannot show that.

The estimator figures are well below WO-004's fourth regression set, whose worst was 77.4 ms on the same missions. I did not find out why. The 100 ms bound did not change. Lower ages in this one set say nothing about the 92.2 ms landing figure, which stays open for D2.

## 4. Limits
- **Hold to Hold cannot be seen.** An operator who selects Hold while in Hold changes nothing the node can read.
- **Stale status.** If the operator switches between PX4's last status and the node's next command, the node can still send one offboard command. No case tests that window, and R-07 switches well before the node's first command.
- **A mode switch away from Hold at boot** means the node yields and the mission does not start. That is the safe direction, but it needs checking on the real switch, so it is listed for D2.
- **`arm_attempt_after_s`** is a fault-case path that sends arm commands while waiting for the estimator, without this check. Only the cases that set it can reach it, and no normal mission does.
- **Not unit-tested:** the settle phase, as before. `arming_step` is.

## 5. What else happened
- **An aborted start.** I launched the first recording in parallel with the commit, `make check` then failed on a long docstring line, and the recording was running uncommitted code. I stopped it, killed its leftover VM processes by PID, fixed the line, committed, and restarted from the commit in a new directory. `runs/fault-matrix-wo016/` keeps the aborted start's log, and no result here comes from it.
- **Debug runs.** `runs/r07-debug/` holds the two runs in section 2, on uncommitted code. They are not results of record.
- **R-07 expected values** were corrected once before the recording: my first key name was not one the analyzer reads.
- **`evals/D1-fault-matrix.json`** was changed after D1 passed to add R-07, on the owner's instruction. Its status text says so. The other cases did not change.

## 6. Verification
`make check` passes. The recording and regression ran at `0016b7c`, on the bounded runner. Their 58 runs are in `ledgers/runs.jsonl`. All 58 record commit `0016b7c`. 57 of them carry `dirty: true`, because the runner appends to that ledger while recording; the first ran before any append. `git status` at the end showed that ledger as the only changed file.

## 7. Retro
Launching a long run alongside a commit cost a restart. A dependent step waits for the commit to return.
