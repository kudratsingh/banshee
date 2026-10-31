# WO-006 — Program-wide rename of this repository and package to banshee

**Status:** passed
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-006 · **Phase:** D0 · **Protocol version:** none; no `evals/` file applies
**Program link:** PROGRAM §5.1, §11, §14 → banshee D0

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
The repository and package are `banshee` on `main`, and the shared files `vishwaroop` copies match in both repositories. This is repository housekeeping, checked by CPU-tier tooling. No simulator, hardware or flight was involved.

## 2. Frozen method
The verification and exit criteria in `work_orders/WO-006-program-rename-banshee.md`, unchanged. The criterion: checks green on the merged commit, and the `contracts/v1/SHA256SUMS.json` and `PROGRAM.md` hashes equal in both repositories.

## 3. Reproduction
- Merged commit: `292d3685e006fa1ac98ee3ebd156ce4749e74f7e`, the merge of pull request 1 at head `3a66e3c`.
- Machine: Python 3.13.5 on macOS (Darwin 25.5.0, arm64), pins from `requirements-dev.txt`.
- Commands: those in the work order's Verification section, on a fresh clone checked out at the merged commit, with `PYTHONPATH` set to that clone's `src`. The append-only check used base `ef55cc4`, the `main` before the merge.
- `vishwaroop` was read only, with `GIT_OPTIONAL_LOCKS=0` and `git show` and `git archive` at commit `405efa5`. Nothing there was changed.

## 4. Results
All measured on 2026-10-31.

| Check | Result |
|---|---|
| CI run 41247160419 on the merged commit | success |
| `make check` | passed, 109 tests |
| `tools/check_hashes.py --verify-kit-manifest` | exit 0 |
| `tools/check_immutable.py --base ef55cc4` | exit 0 |
| `contracts/v1/validate.py` on `drone_sim` | exit 0 |
| `contracts/v1/audit_splits.py` on all three fixtures | exit 0 |
| `grep` for the old underscore package name, outside `.git` and tool caches | 0 hits |
| Negative test: `drone_sim` with the retired `producer` value | rejected, exit 1 |
| `git grep` for the old identifiers, case-insensitive | 27 hits, reviewed; see section 5 |

Shared files, `banshee` at the merged commit against `vishwaroop` at `405efa5`:

| Item | sha256 | Equal? |
|---|---|---|
| `PROGRAM.md` | `58f4c930ca08aaa2fd630826905e9ef9892968e7ceda8e2d920863f5142d02a9` | yes |
| `config/program-lock.json` | `6c6e8cf7ddfb8434754b223d12e1d12a23023be7da2a41e6f118f964c0f77e17` | yes |
| `contracts/v1/SHA256SUMS.json` | `9c0b9347be3758b359c7c7e9fdf7eb7798086167fb1162112fcc9d22bd5a61c3` | yes |
| `config/contract-lock.json` | `f8c3cc1f24919af858a6d77038f3e2127f64d6206610e02f7d9b6b59cbe595ff` | yes |
| `AGENTS.md` core (bytes before `## 13.`) | `8f174fdc05d6184675491181d91a9a8921f7678b22006378f696ec27847659b6` | yes |
| `docs/adr/ADR-0003-PROGRAM-project-names.md` | `5061a80b96b4bd192e1e07fda70ad3eedb905c9e2bfd7434cb65026462008d2e` | yes |
| `contracts/v1/` tree, `diff -r` | no tracked difference | yes |

The owner reported the same cross-repository result independently in the merge approval (`ledgers/approvals.jsonl`).

## 5. Failure analysis
- **One hit is outside the work order's wording.** The 27 old-identifier hits are descriptive prose or listed in `VERIFICATION.md`, except one: `ledgers/approvals.jsonl` line 4 quotes the owner's sentence naming the old repository names. A ledger is append-only and that quotation is its evidence, so it stays. No code or configuration uses an old name.
- **The negative test's exit code differs from the earlier record.** `VERIFICATION.md` records exit 2 and this run gave exit 1, because the work order's one-line check raises an uncaught exception. Both are the non-zero rejection the work order requires.
- **Corrections during the work.** The owner overruled `schema_version` 2.0.0, which is back at 1.0.0, and the wording of `AGENTS.md` line 3. A review agent's false `accepted` event was removed on the owner's decision and logged in `ledgers/corrections.jsonl`.

## 6. Cost and latency
$0. No paid service was used.

## 7. Sealed access
None.

## 8. Exit tests and acceptance
No exit test closes here.

| Gate | Threshold | Result | Evidence | Pass? |
|---|---|---|---|---|
| Checks on the merged commit | green | green | CI run 41247160419; section 4 | yes |
| Shared hashes in both repositories | equal | equal | section 4 | yes |
| Owner approval of the merge | explicit | given 2026-10-31 | `ledgers/approvals.jsonl` | yes |

## 9. Limits
A hash match shows the bytes are the same, nothing more. This report does not cover `vishwaroop`'s own checks, branch state or merge. The simulator tier was **not run**.

## 10. Next bounded work order
WO-001, once WO-008 and WO-009 are also accepted. To roll back, revert the merge commit in a new pull request, and make the matching change in `vishwaroop`.

## 11. Retro note
- Sized S; it took one day and most of the commits on the branch, because the shared-file specification changed twice while it was being applied.
- Ask the owner before following a general rule that conflicts with a stated decision, as the contract version did here.
- Run review agents on a clone from the start, never on the working copy.

## Errata (append-only)
