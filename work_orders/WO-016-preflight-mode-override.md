# WO-016 | Stop the node overriding a mode chosen while disarmed
**Phase:** D1 (a safety defect found in WO-004), before anything in D2
**Exit tests advanced:** none. ET-D1-4 and ET-D1-5 stay passed; this recording checks they still hold.
**Size:** S
**Prerequisites:** phase D1 `passed`; the owner's instruction of 2026-11-01 (`ledgers/approvals.jsonl`).
**Authorization:** AGENTS §2.1. Simulation only. One recording, by the owner's instruction.
**Files:** `src/banshee/offboard/response.py`, `src/banshee/offboard/mission.py`, `src/banshee/faults/injection.py`, `src/banshee/faults/rc_sim.py`, `tests/test_faults.py`, `evals/D1-fault-matrix.json`, `docs/adr/ADR-0009-gate-response-latch.md`, `reports/WO-016-preflight-mode-override.md`.

## Objective
Before flight, the node must not take the aircraft out of a mode the operator chose.

## Scope
The node asks for offboard only from Hold, and yields on any other state, or on leaving offboard once in it, or on being armed outside offboard. New case R-07 shows it. One recording of the matrix, then 10 regression missions.

## Out of scope
Hardware, D2, other items carried from WO-004.

## Verification
```bash
make check
python -m banshee.faults.run_matrix --matrix evals/D1-fault-matrix.json --summary S
python -m banshee.sitl.campaign --runs 10
```
Expected: R-07 passes and fails without the fix; every other case behaves as in WO-004's fourth recording; 10/10 regression.

## Stop conditions
A case that armed in WO-004 stops arming, or any regression mission fails: report, do not loosen the check.

## Report
`reports/WO-016-preflight-mode-override.md`
