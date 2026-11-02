# WO-022 | Recompute the envelope for the X650 and update the D2 exit tests
**Phase:** D2 (accepted before D2 starts, by the owner's instruction of 2026-11-01)
**Exit tests advanced:** none; it changes the frozen statements of ET-D2-1, ET-D2-2, ET-D2-4 and ET-D2-5 before any result exists
**Size:** M
**Prerequisites:** WO-021 accepted.
**Authorization:** the owner's decision of 2026-11-01. Simulation only; no hardware. Full independent review, because it touches milestone exit tests.
**Files:** `src/banshee/sitl/x650_proxy.py`, `tests/test_x650_proxy.py`, `src/banshee/export/episode.py`, `src/banshee/faults/run_matrix.py`, `evals/X650-proxy-cases.json`, `evals/X650-proxy-control-cases.json`, `evals/X650-position-lost-cases.json`, `docs/SOURCES-D0.md`, `ledgers/runs.jsonl`, `evals/D3-standoffs-x650.json`, `evals/D2-exit-tests.json`, `config/phases.json`, `docs/PHASES.md`, `docs/OPERATING_ENVELOPE.md`, `docs/adr/ADR-0007-d0-airframe-and-stack-proposal.md`, `reports/WO-022-x650-envelope-and-d2-tests.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Recompute the standoffs, the fence overrun and the exclusion radius for the X650 at about 4–5 kg with 15-inch carbon props, freeze the values, and update the D2 exit tests that name hardware.

## Scope
Measure the braking, overrun and drift cases on a simulated proxy of the X650, three recordings each. D1's X500 evidence stays as the record of that model. Estimated terms are recomputed and labelled.

## Out of scope
A real X650, re-running D1, and the stack change on the Jetson, which waits on the owner's decision in `docs/BUY_LIST-REPRICED-2026-11-01.md`.

## Verification
```bash
make check
```
The proxy recordings, and the independent review.

## Stop conditions
A recomputed value that breaks the owner's 150 m rule is reported with options, not adjusted to fit.

## Report
`reports/WO-022-x650-envelope-and-d2-tests.md`
