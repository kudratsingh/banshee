# WO-019 | Close the stale-status offboard-command window in the mode-override fix
**Phase:** D3 (accepted before phase D3 is marked ready; not a D2 prerequisite, by the owner's instruction of 2026-11-01)
**Exit tests advanced:** none
**Size:** S (stub; expand when it becomes next)
**Prerequisites:** WO-016 accepted.
**Authorization:** AGENTS §2.1. Simulation only.
**Files:** `src/banshee/offboard/mission.py`, `src/banshee/offboard/response.py`, `tests/test_faults.py`, `evals/D1-fault-matrix.json`, `reports/WO-019-stale-status-offboard-window.md`.

Serves `PROGRAM §5.1`.

## Objective
The node must not send an offboard command based on a status older than an operator's mode change.

## Scope
Written when expanded. Minimum: a test that puts the operator's switch between PX4's last status and the node's next command, which R-07 does not do (`reports/WO-016-preflight-mode-override.md` section 4). If a command crossing a status update cannot be fully prevented from the node, report the remaining window as measured, and do not call it closed.

## Out of scope
Hardware, and changes to arming logic beyond this window.

## Verification
Commands written when expanded.

## Stop conditions
A case that armed in WO-016's recording stops arming, or any regression mission fails: report, do not loosen the check.

## Report
`reports/WO-019-stale-status-offboard-window.md`
