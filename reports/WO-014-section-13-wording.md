# WO-014 — Correct AGENTS.md sections 13.8 and 13.9

**Status:** passed
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-014 · **Phase:** D1 · **Protocol version:** none; no `evals/` file applies
**Program link:** PROGRAM §5.1 → banshee D1

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 1. Claim and scope
`§13.8` names the `ironclad` writer, and `§13.9` requires the independent review before the first armed flight, D3 readiness, on the owner's approval. Policy wording only.

## 2. Frozen method
The verification in the work order, unchanged.

## 3. Reproduction
Merged commit `85f8c9c8d2218080b7b63266a85da354ef3300cb`. Commands: `make check`, `make immutable BASE=origin/main`, `git diff origin/main -- AGENTS.md`.

## 4. Results
Measured on 2026-10-31: CI run 41273672151 succeeded on the merged commit; `make check` and the append-only check passed; the `AGENTS.md` diff touched two lines, both in section 13.

## 5. Failure analysis
None. The frozen ET-D1-3 text still names the old writer path, mapped in ADR-0008.

## 6. Cost and latency
$0.

## 7. Sealed access
None.

## 8. Exit tests and acceptance
No exit test closes here.

| Gate | Threshold | Result | Evidence | Pass? |
|---|---|---|---|---|
| Checks on the merged commit | green | green | CI run 41273672151 | yes |

## 9. Limits
Wording only; no behaviour is tested. `PROGRAM.md` still calls D3 optional, which is for `ironclad`.

## 10. Next bounded work order
WO-002 continues on its own branch. To roll back, revert the merge in a new pull request.

## 11. Retro note
Sized S, as it took one pull request.

## Errata (append-only)
