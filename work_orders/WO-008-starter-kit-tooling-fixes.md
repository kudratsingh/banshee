# WO-008 | Fix three starter-kit tooling defects found during the rename review
**Phase:** D0
**Exit tests advanced:** none; these block WO-001.
**Size:** S
**Prerequisites:** WO-006 `accepted` (status ledger), so these fixes build on the renamed tree.
**Authorization:** AGENTS §2.1 only
**Files:** `.gitignore`, `tools/status_board.py`, `tests/`, `SHA256SUMS.json`.

Serves `PROGRAM §10`. The defects came with the starter kit; the rename did not cause them. The sibling kit ships the same `.gitignore`, `tools/status_board.py` and tests, so its owner may want the same fixes.

## Objective
Make the documented first-session steps work as written.

## Scope
1. `.gitignore`: `*secret*` matches `tools/scan_secrets.py`. A fresh `git add -A` silently drops it, and `ruff` skips it inside a git checkout. Add `!tools/scan_secrets.py` after that pattern.
2. `tools/status_board.py`: `--phase` and `--et` appends are always refused, because the record carries `"wo": null` and takes the work-order branch. Omit unset fields, and add a CLI-level test.
3. `tests/test_project_consistency.py::test_no_fixture_claims_in_reports` fails on any file in `reports/`, so it blocks every real report. Change it so real reports pass while keeping a guard against unbacked claims.

## Out of scope
Anything in `contracts/v1/`, `PROGRAM.md` or the `AGENTS.md` core; any other behaviour change; any weakening of a check beyond item 3's stated justification.

## Deliverables
The three fixes, each with a regression test or command, in their own commits.

## Steps
Fix one defect per commit. Run `make check` before each commit. Regenerate `SHA256SUMS.json` last.

## Verification
```bash
make check
python tools/status_board.py --append --phase D0 --event ready   # in a scratch copy: must be accepted
git check-ignore tools/scan_secrets.py                           # must exit 1
```
Also: in a scratch copy, `git init && git add -A` must track every file in `SHA256SUMS.json`, and a real report in `reports/` must pass `make check`.

## Exit criteria
No exit test closes here. Accepted when all three verifications pass on the merged commit.

## Stop conditions
A fix would touch shared bytes, or would weaken a check beyond the stated justification.

## Report
`reports/WO-008-starter-kit-tooling-fixes.md`, which this work order makes possible.
