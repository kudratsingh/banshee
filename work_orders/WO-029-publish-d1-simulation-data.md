# WO-029 | Publish the D1 simulation data for vishwaroop, with a frozen split and a nominal variation set
**Phase:** D2 (not started); simulation only
**Exit tests advanced:** none
**Size:** M
**Prerequisites:** WO-028 accepted.
**Authorization:** the owner's work order of 2026-11-06 (`ledgers/approvals.jsonl`). Local SITL only; no hardware, no spending. Private publication within the owner's projects.
**Files:** `src/banshee/publish/`, `src/banshee/sitl/variation.py`, `src/banshee/sitl/campaign.py`, `src/banshee/sitl/vm/run_mission.sh`, `tests/test_publish.py`, `evals/D1-split-plan.json`, `evals/D1-variation-set.json`, `evals/d1-line-v1.json`, `evals/d1-climb-v1.json`, `reports/WO-029-publish-d1-simulation-data.md`, `ledgers/`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Publish every completed D1 episode (both stacks, failed flights included) and the raw ULogs, and a 99-attempt nominal variation set, as completed immutable exports with a frozen family-level split.

## Scope
Freeze the split plan, routes, winds and seeds first. Families are route × wind × fault family, assigned by `src/banshee/publish/splits.py`. Exports go to `data/exports/`, each with MANIFEST.json, verified hashes and COMPLETE last.

## Out of scope
Writing into vishwaroop. Public release. Hardware.

## Verification
```bash
make check
```
Each export's hashes verified before COMPLETE; the contract's split audit with the family as a hold-out axis.

## Stop conditions
A family not in the frozen plan, a hash mismatch, or a contract validation failure: no COMPLETE, and report.

## Report
`reports/WO-029-publish-d1-simulation-data.md`
