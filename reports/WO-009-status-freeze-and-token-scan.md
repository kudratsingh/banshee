# WO-009 — Protect accepted work orders and widen the secret scan

**Status:** passed
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-009 · **Phase:** D0 · **Protocol version:** none; no `evals/` file applies
**Program link:** PROGRAM §10 → banshee D0

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
On `main`, the status tool cannot reset a work order that already has a record, and the secret scan catches Hugging Face and RunPod tokens, including in files with no extension. This covers repository tooling only.

## 2. Frozen method
The verification and exit criteria in `work_orders/WO-009-status-freeze-and-token-scan.md`, unchanged.

## 3. Reproduction
- Merged commit: `292d3685e006fa1ac98ee3ebd156ce4749e74f7e`. The work is in `a163954`, `f114bcf`, `0b48570`, `5dc8ef2`, `f166343` and `26f0ce2`.
- Machine: Python 3.13.5 on macOS (Darwin 25.5.0, arm64), pins from `requirements-dev.txt`.
- Commands: those in the work order's Verification section, on a fresh clone at the merged commit, with each state-changing command in a scratch copy made by `git archive`.

## 4. Results
All measured on 2026-10-31. The tokens were **fixtures**: a prefix followed by 36 repeated letters, written only to scratch copies.

| Check | Result |
|---|---|
| CI run 41247160419 on the merged commit | success |
| `make check` | passed, 109 tests |
| `tools/status_board.py --append --wo WO-007 --event created`, scratch copy | refused, exit 2 |
| `tools/scan_secrets.py --root <copy>`, `hf_` token in a `.md` file | exit 1 |
| Same, `rpa_` token in a `.md` file | exit 1 |
| Same, `hf_` token in a file with no extension | exit 1 |
| Same, `rpa_` token in a file with no extension | exit 1 |
| Same, unmodified copy | exit 0 |

The earlier checks in `VERIFICATION.md`, including the hand-appended status line and the symlink replacement, were not rerun on the merged commit as separate commands; their tests in `tests/test_tools.py` ran as part of `make check`.

## 5. Failure analysis
- `0b48570` was committed with lint red, because the commit script did not stop on failure. `5dc8ef2` fixed it in a new commit, with no amend, and later scripts used `set -e` and `set -o pipefail`.
- My first `.gitignore` patterns left names like `secret_prod.env` trackable, and the owner ordered the broad rule back. That rule then matched this work order's own file name, so the file was renamed in `26f0ce2` and a test now fails if any tracked file is ignored.

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
The scanner matches known patterns; a pass does not show that the repository holds no secret. A local `.env` now counts as a scanned file, so a real token in one fails `make secrets` on that machine. The sibling kit's copy of these fixes is not covered here.

## 10. Next bounded work order
WO-001, once WO-006 and WO-008 are also accepted. To roll back, revert the commits above in a new pull request.

## 11. Retro note
- Sized S; it took six commits, two of them repairs. Stop any commit script on the first failure.
- Test the repository's own files against a new ignore rule as soon as the rule is written.

## Errata (append-only)
