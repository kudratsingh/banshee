# WO-021 | Record the X650 decision and the hold; re-price the list
**Phase:** D2 (not started)
**Exit tests advanced:** none
**Size:** S
**Prerequisites:** WO-020 accepted; the owner's decision of 2026-11-01.
**Authorization:** AGENTS §2. The agent records and plans; the owner approves line by line and places the orders.
**Files:** `ledgers/approvals.jsonl`, `docs/BUY_LIST-REPRICED-2026-11-01.md`, `docs/BUY_LIST-2026-11-01.md`, `docs/PURCHASE_REQUEST-2026-11-01.md`, `docs/BOM_WORKSHEET.md`, `docs/CONTEXT_AND_DECISIONS.md`, `docs/SOURCES-D0.md`, `docs/adr/ADR-0007-d0-airframe-and-stack-proposal.md`, `reports/WO-021-x650-hold-and-reprice.md`, `work_orders/WO-022-x650-envelope-and-d2-tests.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Put the hold on record at once, re-price the list for the X650 platform, check every new line against the FCC Covered List, and update ADR-0007.

## Scope
One table with seller, price, stock, date read and status per line, and a total. The X500 recorded as superseded. The fisheye question. WO-022 as a stub for the envelope and D2 tests.

## Out of scope
The envelope, standoffs and D2 exit tests (WO-022). Placing orders. Connecting hardware. Starting D2.

## Verification
```bash
make check
```

## Stop conditions
No purchase until the owner approves the re-priced list line by line.

## Report
`reports/WO-021-x650-hold-and-reprice.md`
