# WO-004 | D1 fault matrix in simulation and the freshness gate in the command loop
**Phase:** D1
**Exit tests advanced:** ET-D1-4, ET-D1-5
**Size:** M
**Prerequisites:** WO-002 accepted (SITL, offboard bridge, export exist); freshness bounds frozen in `evals/D1-exit-tests.json` (`frozen` events for ET-D1-5).
**Authorization:** AGENTS §2.1 only. Simulation only.
**Files:** `src/omni_drone/faults/`, `src/omni_drone/freshness.py` (bounds loading only; logic exists), `tests/`, `reports/WO-004-d1-fault-matrix-and-freshness-gate.md`.

## Objective
Execute every case in the D1 fault matrix (`docs/TEST_PROTOCOL.md §1`) against the real command path in SITL, with the freshness/estimator-validity gate deciding the response, and report configured versus tested behaviour for each case.

## Scope
Fault-injection harness (stale setpoint while heartbeat continues; lost command stream; stale sensor; missing depth; localization reset/loss; delayed planner; low energy; operator takeover; network interruption; injected frame-sign error caught by the sign tests); one log and one contract export per case; a table of expected vs observed behaviour; PX4 failsafe parameters recorded with the stack lock; the gate's decisions logged with reasons.

## Out of scope
Hardware, real link cuts (D2), VIO, learned components.

## Verification
```bash
make check
python -m omni_drone.faults.run_matrix --matrix evals/D1-fault-matrix.json --out runs/
python -m pytest tests/test_freshness.py -q
```
Expected: every case executed and logged; deviations from the specified response reported, not hidden; freshness tests green with the frozen bounds.

## Exit criteria
ET-D1-4 and ET-D1-5 pass → phase D1 `passed` once ET-D1-1…5 are all recorded.

## Stop conditions
A fault case whose specified response cannot be implemented on the pinned stack (report and propose an ADR; do not silently change the spec); any physical endpoint present.

## Report
`reports/WO-004-d1-fault-matrix-and-freshness-gate.md`
