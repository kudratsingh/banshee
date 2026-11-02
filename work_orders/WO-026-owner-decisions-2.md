# WO-026 | Record the owner's second set of decisions of 2026-11-02: ET-D2-4's check, line approvals, line 2's FCC record, and the D3 package and tests
**Phase:** D2 (not started)
**Exit tests advanced:** none; it adds a pass/fail check to ET-D2-4 and adds ET-D3-6 and ET-D3-7, before any D2 or D3 result
**Size:** S
**Prerequisites:** WO-023 accepted.
**Authorization:** the owner's decisions of 2026-11-02 (`ledgers/approvals.jsonl`). The owner places orders; the agent places none. Full independent review, because it touches milestone exit tests.
**Files:** `ledgers/approvals.jsonl`, `config/phases.json`, `docs/PHASES.md`, `evals/D2-exit-tests.json`, `docs/BUY_LIST-FINAL-2026-11-02.md`, `docs/D3_APPROVAL_PACKAGE.md`, `docs/OPERATING_ENVELOPE.md`, `docs/SOURCES-D0.md`, `reports/WO-026-owner-decisions-2.md`, `CHANGES.md`, `docs/STATUS_BOARD.md`, `work_orders/STATUS.jsonl`.

Serves `PROGRAM §5.1`.

## Objective
Put each decision on record; add the no-stale-setpoint check to ET-D2-4; record line 2's FCC clearance; draft the D3 approval package with the radio check and RTK options; add D3 exit tests that collect the data to raise the limits.

## Scope
As in the objective. The package split and the Humble repeats are WO-027 and WO-028.

## Out of scope
Purchases, order tracking, hardware, D2 and D3 themselves.

## Verification
```bash
make check
```
The independent review.

## Stop conditions
A decision that cannot be recorded without going beyond the owner's words: report it.

## Report
`reports/WO-026-owner-decisions-2.md`
