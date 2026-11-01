# WO-015 | Record the owner's decisions after D1: ADR-0010, D3 standoffs, VM bounds
**Phase:** D3 (standoffs); D1 (records)
**Exit tests advanced:** none. The standoffs are an input to ET-D3-4.
**Size:** S
**Prerequisites:** phase D1 `passed`; the owner's message of 2026-11-01 (`ledgers/approvals.jsonl`).
**Authorization:** AGENTS §2.1, with the owner's decisions. No purchase, no hardware.
**Files:** `evals/D3-standoffs.json`, `docs/OPERATING_ENVELOPE.md`, `docs/adr/ADR-0010-vision-cases-carried-to-d4.md`, `ledgers/approvals.jsonl`, `reports/WO-015-owner-decisions-after-d1.md`, `CHANGES.md`, status files.

Serves `PROGRAM §5.1`.

## Objective
Record three owner decisions where the repository can act on them.

## Scope
1. ADR-0010 becomes accepted.
2. Freeze the D3 standoffs, 8.6 m at 2.5 m/s and 3.35 m at 1.0 m/s, in `evals/`, and update the envelope, including the statement that the 150 m exclusion radius covers position-lost cases on its own.
3. Record the VM disk cap and the free-space check as done, after reading both back.

## Out of scope
The mode-override fix (WO-016), the purchase request and the D2 freeze (WO-017), D3's exit tests.

## Verification
```bash
make check
sha256sum evals/D3-standoffs.json
```

## Stop conditions
An owner statement the evidence does not support is recorded with the numbers, and raised, not reworded.

## Report
`reports/WO-015-owner-decisions-after-d1.md`
