# WO-008 | Fix three starter-kit tooling defects found during the rename review
**Phase:** D0
**Exit tests advanced:** none; these block WO-001.
**Size:** S
**Prerequisites:** none. On the owner's instruction of 2026-10-31 (`ledgers/approvals.jsonl`), this is done now, in a separate commit on the WO-006 branch.
**Authorization:** AGENTS §2.1, plus the owner's instruction to delete one test (`ledgers/approvals.jsonl`).
**Files:** `.gitignore`, `tools/status_board.py`, `tests/test_tools.py`, `tests/test_project_consistency.py`, `CHANGES.md`, `VERIFICATION.md`, `work_orders/`, `docs/STATUS_BOARD.md`, `SHA256SUMS.json`.

Serves `PROGRAM §10`. The defects came with the starter kit; the rename did not cause them. The sibling kit ships the same `.gitignore`, `tools/status_board.py` and tests, so its owner may want the same fixes.

## Objective
Make the documented first-session steps work as written.

## Scope
1. `.gitignore`: `*secret*` matches `tools/scan_secrets.py`. A fresh `git add -A` silently drops it, and `ruff` skips it inside a git checkout. Add `!tools/scan_secrets.py`; WO-009 settled the final patterns.
2. `tools/status_board.py`: `--phase` and `--et` appends are always refused, because the record carries `"wo": null` and takes the work-order branch. Drop unset fields before `append()`, make `current_states` test keys by `.get()` truthiness, refuse a record naming more than one id, and add CLI-level tests.
3. `tests/test_project_consistency.py::test_no_fixture_claims_in_reports` fails on any file in `reports/`, so it blocks every real report. Delete it, on the owner's instruction.

## Out of scope
Anything in `contracts/v1/`, `PROGRAM.md` or the `AGENTS.md` core; any other behaviour change; any other weakening of a check.

## Deliverables
The three fixes in a commit separate from the rename, with tests, each logged in `CHANGES.md`. A follow-up commit closes a regression and a pattern gap that the review of that commit found.

## Steps
Apply the three fixes in one commit on the WO-006 branch. Run `make check` before committing. Regenerate `SHA256SUMS.json` last.

## Verification
```bash
make check
python tools/status_board.py --append --phase D0 --event ready   # in a scratch copy: must be accepted
git check-ignore tools/scan_secrets.py                           # must exit 1
```
Also: in a scratch copy, `git init && git add -A` must track every file in `SHA256SUMS.json`, and a real report in `reports/` must pass `make check`.

## Exit criteria
No exit test closes here. Accepted when all the verifications pass on the merged commit.

## Stop conditions
A fix would touch shared bytes, or would weaken a check other than the test named above.

## Report
`reports/WO-008-starter-kit-tooling-fixes.md`, written at acceptance, once this work order has merged. Until then the fixes are logged in `CHANGES.md`.
