# WO-017 | Purchase request for Option A, and freeze D2's exit tests
**Phase:** D2 (exit tests frozen; the phase is not started)
**Exit tests advanced:** none passed. ET-D2-1 to ET-D2-5 are frozen.
**Size:** S
**Prerequisites:** phase D1 `passed`; WO-016 accepted; the owner's instruction of 2026-11-01 (`ledgers/approvals.jsonl`).
**Authorization:** AGENTS §2.1. No purchase, cart, account or hardware action. Each line needs the owner's approval.
**Files:** `docs/PURCHASE_REQUEST-2026-11-01.md`, `docs/BOM_WORKSHEET.md`, `evals/D2-exit-tests.json`, `reports/WO-017-purchase-request-and-d2-freeze.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Give the owner one table to approve line by line, and fix what D2 must show before any D2 result exists.

## Scope
The re-priced Option A order, with price, source, date and Covered List status on each line, and no netting. The recommendation between Pixhawk 6X and ARKV6X. `evals/D2-exit-tests.json`, with frozen events for each exit test.

## Out of scope
Buying anything, starting D2, expanding WO-005, connecting to any hardware.

## Verification
```bash
make check
```
Totals are recomputed from the table by an independent reviewer, who also compares the freeze with `config/phases.json`, because this work order touches milestone exit tests.

## Stop conditions
This work order is the stopping point: after it, nothing proceeds until the owner approves lines.

## Report
`reports/WO-017-purchase-request-and-d2-freeze.md`
