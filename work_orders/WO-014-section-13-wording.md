# WO-014 | Correct AGENTS.md sections 13.8 and 13.9
**Phase:** D1
**Exit tests advanced:** none; this is project policy housekeeping.
**Size:** S
**Prerequisites:** WO-013 merged; the owner's approval of 2026-10-31 (`ledgers/approvals.jsonl`).
**Authorization:** AGENTS §2.1, with the owner's approval of this wording.
**Files:** `AGENTS.md` (section 13 only), `docs/adr/ADR-0007-d0-airframe-and-stack-proposal.md`, `docs/adr/ADR-0008-adopt-ironclad.md`, `docs/BOM_WORKSHEET.md`, `ledgers/approvals.jsonl`, `docs/STATUS_BOARD.md`, `work_orders/`, `reports/`.

Serves `PROGRAM §5.1`. The owner's decisions moved the first armed flight to D3, and WO-013 moved the writer into `ironclad`.

## Objective
Make section 13 match those two changes.

## Scope
1. `§13.8`: exports go through `ironclad.contracts.v1.writer`.
2. `§13.9`: the independent review comes before the first armed flight, D3 readiness.
3. Record the owner's defaults: Pixhawk 6X for now, with the choice made at purchase; who checks the FCC, FAA and Jetson items.

## Out of scope
The shared core before `## 13.`, any other rule, and the frozen ET-D1-3 text.

## Verification
```bash
make check
make immutable BASE=origin/main
git diff origin/main -- AGENTS.md
```
Expected: every command exits 0, and the diff touches only the two lines in section 13.

## Exit criteria
No exit test closes here. Accepted when CI is green on the merged commit.

## Stop conditions
The change would touch the shared core.

## Report
`reports/WO-014-section-13-wording.md`.
