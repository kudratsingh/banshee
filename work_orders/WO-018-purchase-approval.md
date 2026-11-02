# WO-018 | Record the owner's purchase approval and write the buy list
**Phase:** D2 (not started)
**Exit tests advanced:** none
**Size:** S
**Prerequisites:** WO-017 accepted; the owner's approval of 2026-11-01.
**Authorization:** AGENTS §2. The agent records and plans; the owner places the orders.
**Files:** `ledgers/approvals.jsonl`, `docs/BUY_LIST-2026-11-01.md`, `docs/PURCHASE_REQUEST-2026-11-01.md`, `docs/BOM_WORKSHEET.md`, `docs/OPERATING_ENVELOPE.md`, `reports/WO-018-purchase-approval.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Put the approval on record, and turn it into a list the owner can order from.

## Scope
The owner's words, per line. Sellers and prices under the sourcing rule. The C2 citation. WO-019 for the stale-status window.

## Out of scope
Placing orders, sending email, connecting hardware, starting D2.

## Verification
```bash
make check
```

## Stop conditions
Nothing proceeds to hardware until parts arrive and the owner approves connecting them.

## Report
`reports/WO-018-purchase-approval.md`
