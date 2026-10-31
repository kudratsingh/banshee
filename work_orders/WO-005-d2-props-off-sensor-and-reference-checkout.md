# WO-005 | D2 props-off sensor, localization and reference checkout
**Phase:** D2
**Exit tests advanced:** ET-D2-1, ET-D2-2, ET-D2-3, ET-D2-4
**Size:** L (milestone-level stub; expand when it becomes next)
**Prerequisites:** phase D1 `passed`; hardware purchased by the owner per the D0 decision (recorded in `ledgers/approvals.jsonl`); outside-in reference equipment available; `evals/D2-exit-tests.json` frozen.
**Authorization:** §2.3 owner approval required before connecting to the flight controller (even with propellers removed) and before any link-cut test; no arming.
**Files:** `src/banshee/reference/`, `src/banshee/sensors/`, `tests/`, `reports/WO-005-d2-props-off-sensor-and-reference-checkout.md`.

## Objective
With propellers removed, validate the intended camera/IMU setup hand-carried through the test volume (timestamps, frames, latency, resets, tracking loss), qualify the outside-in reference, and exercise the real connection-loss behaviour on the actual command path — before any armed flight.

## Scope
Written when expanded. Minimum: timestamp-offset and latency measurement; VIO tracking log with dropout/reset counts and drift vs reference; reference static survey, dynamic latency, coverage map, session-check procedure; three real link-cut trials with motors disarmed; contract exports of every session.

## Out of scope
Arming, flight, learned components.

## Verification
Commands written when expanded; results per `docs/PHASES.md` D2 thresholds.

## Stop conditions
Hardware not yet owned; approval for hardware connection missing; reference coverage inadequate (report inconclusive, do not pass ET-D2-2).

## Report
`reports/WO-005-d2-props-off-sensor-and-reference-checkout.md`
