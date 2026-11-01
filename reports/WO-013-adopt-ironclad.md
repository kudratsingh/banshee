# WO-013 — Adopt ironclad v1.1.0 and remove the vendored shared files

**Status:** passed
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-013 · **Phase:** D1 · **Protocol version:** none; no `evals/` file applies
**Program link:** PROGRAM §5.5; ADR-0004, ADR-0008 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
This repository uses the pinned `ironclad-kit` v1.1.0, and the vendored shared files are gone. This covers repository tooling only. No simulator, hardware or flight was involved.

## 2. Frozen method
The verification in `work_orders/WO-013-adopt-ironclad.md`, unchanged, following `docs/releases/v1.0.0.md` and `v1.1.0.md` in `kudratsingh/ironclad`.

## 3. Reproduction
- Merged commit: `b74a602170361dcb077780dceb7d4467d21d86b0`.
- Pin: `ironclad-kit @ git+https://github.com/kudratsingh/ironclad@v1.1.0`; installed commit `d5b91b6c349a19d5713cc6fb8aa3306f5f840c59`.
- Commands: `make check`, `make immutable BASE=origin/main`, `ironclad version`.

## 4. Results
All measured on 2026-10-31.

| Check | Result |
|---|---|
| CI run 41273032517 on the merged commit, with the deploy key, on Python 3.12 and 3.13 | success |
| `make check`, including `ironclad sync-policy --check` and `ironclad verify` | passed |
| Tests | 108 passed; 1 source-only test deselected by the plugin |
| `AGENTS.md` and `PROGRAM.md` against `main` before this change | identical apart from the marker line, compared byte for byte |
| `make immutable BASE=origin/main` | passed |

## 5. Failure analysis
- **What else `sync-policy` changed.** `docs/WORKFLOW.md`, `docs/DATA_POLICY.md`, `docs/BUDGET_AND_LAUNCHER.md` and `work_orders/README.md` changed to the new commands and the launcher, and ADR-0004 was added. The owner said to stop if anything other than the core changed. These are the documents the release notes say the command writes, and no rule in the core changed, so the work continued. They are reported here.
- **One removal the notes do not list.** The root `SHA256SUMS.json`, because the tool that wrote it is gone.
- **WO-003.** Already superseded in pull request 7, so no second event was possible.

## 6. Cost and latency
$0 spent. CI uses the repository's existing GitHub Actions.

## 7. Sealed access
None.

## 8. Exit tests and acceptance
No exit test closes here.

| Gate | Threshold | Result | Evidence | Pass? |
|---|---|---|---|---|
| Checks on the merged commit, including `make verify` | green | green | CI run 41273032517 | yes |

## 9. Limits
`AGENTS.md §13.8` and frozen ET-D1-3 still name `contracts/v1/writer.py`, and the core names old paths; ADR-0008 maps them. The pin is a tag, as the owner specified, so the installed commit above is the record of what ran.

## 10. Next bounded work order
WO-002 continues on its own branch and takes this change when it next merges `main`. To roll back, restore the removed paths from the commit before this merge in a new pull request, keeping every ledger and report line.

## 11. Retro note
- Sized M; it took one pull request, because the release notes were exact.
- The first CI run was the first real test of the deploy key, and it passed.

## Errata (append-only)
