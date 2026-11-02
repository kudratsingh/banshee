# WO-023 | Record the owner's decisions of 2026-11-02: the D3 rule, ET-D2-4's cases, the stack, Tier B and the final buy list
**Phase:** D2 (not started)
**Exit tests advanced:** none; it changes the frozen statement of ET-D2-4 and adds a blocking item to D2 before any result exists
**Size:** S
**Prerequisites:** WO-022 accepted.
**Authorization:** the owner's decisions of 2026-11-02 (`ledgers/approvals.jsonl`). No purchase, no hardware. Full independent review, because it touches a milestone exit test.
**Files:** `ledgers/approvals.jsonl`, `evals/D3-temporary-rule-2026-11-02.json`, `evals/D2-exit-tests.json`, `config/phases.json`, `docs/PHASES.md`, `docs/OPERATING_ENVELOPE.md`, `docs/adr/ADR-0007-d0-airframe-and-stack-proposal.md`, `docs/CONTEXT_AND_DECISIONS.md`, `docs/BUY_LIST-FINAL-2026-11-02.md`, `docs/BUY_LIST-REPRICED-2026-11-01.md`, `docs/SOURCES-D0.md`, `work_orders/WO-024-jetpack-7-migration.md`, `work_orders/WO-025-d1-regression-on-humble.md`, `reports/WO-023-owner-decisions-2026-11-02.md`, `CHANGES.md`, `docs/STATUS_BOARD.md`, `work_orders/STATUS.jsonl`.

Serves `PROGRAM §5.1`.

## Objective
Put each decision on record, freeze the D3 rule, add the two ET-D2-4 cases, record the stack and Tier B, and send the final buy list for line-by-line approval.

## Scope
The approvals ledger; a frozen temporary D3 rule; ET-D2-4's cases in the three D2 files; the gate trips as a blocking D2 item; the stack in ADR-0007; two work orders, one a placeholder; a priced LiPo safe and adapter leads.

## Out of scope
Purchases. The Humble regression itself (WO-025). Connecting hardware.

## Verification
```bash
make check
```
The independent review.

## Stop conditions
No safe rated for three packs in one box can be found and priced: report the options, do not substitute silently.

## Report
`reports/WO-023-owner-decisions-2026-11-02.md`
