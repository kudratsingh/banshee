# WO-008 — Fix three starter-kit tooling defects found during the rename review

**Status:** passed
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-008 · **Phase:** D0 · **Protocol version:** none; no `evals/` file applies
**Program link:** PROGRAM §10 → banshee D0

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
The documented first-session steps work as written on `main`: phase and exit-test status appends are accepted, `git add -A` keeps the secret scanner, and a real report no longer fails the tests. This covers repository tooling only.

## 2. Frozen method
The verification and exit criteria in `work_orders/WO-008-starter-kit-tooling-fixes.md`, unchanged.

## 3. Reproduction
- Merged commit: `292d3685e006fa1ac98ee3ebd156ce4749e74f7e`. The fixes are in `95f7a34` and `e412aea`.
- Machine: Python 3.13.5 on macOS (Darwin 25.5.0, arm64), pins from `requirements-dev.txt`.
- Commands: those in the work order's Verification section, on a fresh clone at the merged commit, with each state-changing command in a scratch copy made by `git archive`.

## 4. Results
All measured on 2026-10-31.

| Check | Result |
|---|---|
| CI run 41247160419 on the merged commit | success |
| `make check` | passed, 109 tests |
| `tools/status_board.py --append --phase D0 --event ready`, scratch copy | accepted, exit 0 |
| `git check-ignore tools/scan_secrets.py` | exit 1, not ignored |
| `git init && git add -A`, scratch copy, against `SHA256SUMS.json` | 116 files listed, 0 untracked |
| A file in `reports/`, scratch copy: `make test secrets links` | passed |
| Full `make check` with this report and the other two acceptance reports in `reports/` | passed |

## 5. Failure analysis
The review of the first commit found that combining `--phase` and `--et` could mark a phase as passed without recording the exit test. `e412aea` closed that by refusing a record that names more than one id, with a regression test.

## 6. Cost and latency
$0. No paid service was used.

## 7. Sealed access
None.

## 8. Exit tests and acceptance
No exit test closes here.

| Gate | Threshold | Result | Evidence | Pass? |
|---|---|---|---|---|
| The work order's verifications on the merged commit | all pass | all pass | section 4 | yes |

## 9. Limits
Deleting `test_no_fixture_claims_in_reports` removed a check, on the owner's instruction (`ledgers/approvals.jsonl`), because it failed on any file in `reports/`. Nothing now scans reports for fixture claims automatically; `AGENTS.md §7.2` still applies by discipline. The sibling kit's copy of these fixes is not covered here.

## 10. Next bounded work order
WO-001, once WO-006 and WO-009 are also accepted. To roll back, revert the commits above in a new pull request.

## 11. Retro note
- Sized S and took two commits. The defect in the first commit was caught only by an independent review, so keep one for tooling that writes to ledgers.
- WO-009 changed the `.gitignore` patterns again the same day, so check the owner's rule before narrowing one.

## Errata (append-only)
