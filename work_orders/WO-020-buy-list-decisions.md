# WO-020 | Record the owner's buy-list decisions and the C2 correction
**Phase:** D2 (not started)
**Exit tests advanced:** none
**Size:** S
**Prerequisites:** WO-018 accepted; the owner's decisions of 2026-11-01.
**Authorization:** AGENTS §2. The agent records and plans; the owner places the orders.
**Files:** `ledgers/approvals.jsonl`, `docs/BUY_LIST-2026-11-01.md`, `docs/BOM_WORKSHEET.md`, `docs/OPERATING_ENVELOPE.md`, `docs/SOURCES-D0.md`, `reports/WO-020-buy-list-decisions.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Put each decision on record, correct C2, and update the list and its totals.

## Scope
One ledger record per decision. Sellers, prices and totals. The FCC correction for line 5 in the envelope.

## Out of scope
Placing orders, sending email, connecting hardware, starting D2, choosing the OAK-D Pro field of view.

## Verification
```bash
make check
```

## Stop conditions
Nothing proceeds to hardware until parts arrive and the owner approves connecting them.

## Report
`reports/WO-020-buy-list-decisions.md`
