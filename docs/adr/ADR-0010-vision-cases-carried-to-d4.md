# ADR-0010 — Carry the vision-only fault cases to D4

**Date:** 2026-11-01 · **Status:** proposed · **Work order:** WO-004 · **Program link:** PROGRAM §5.1

## Context
WO-004's stop condition: a fault case whose specified response cannot be implemented on the pinned stack is reported, with an ADR proposed, and the specification is not silently changed.

V-01 to V-04 fly `gz_x500_vision` with `EKF2_GPS_CTRL` 0. In all four recordings of `evals/D1-fault-matrix.json` nothing armed in that world. In the fourth, the node sent 25 arm commands per case and PX4 logged "Arming denied: Resolve system health failures first", with "heading estimate not stable" and "Global position estimate required" among the preflight failures. So no fault was injected in V-01 to V-03, and the refusal expected in V-04 does not discriminate. V-05 is not part of this: it flies plain `gz_x500` with `SYS_HAS_GPS` 0, and shows the refusal it specifies. Whether the cause is the `gz_x500_vision` set-up or the stack was not established. See `reports/WO-004-d1-fault-matrix-and-freshness-gate.md §4`.

These cases came from WO-001's proposals. They are not in ET-D1-4's list or `docs/TEST_PROTOCOL.md §1`, and VIO is outside WO-004's scope.

## Decision
Proposed: keep V-01 to V-04 in the matrix, reported as not shown. Carry them to D4, where vision is in scope, with the vision set-up as the first task of that work order. The vision-only rows of `docs/OPERATING_ENVELOPE.md` stay estimated until then. The specification does not change.

## Alternatives considered
| Option | Why not (or why not yet) |
|---|---|
| Debug the vision world now | VIO is out of WO-004's scope, and no D1 exit test depends on it |
| Drop the cases | Would hide that the origin-error behaviour has never been shown |
| Hold D1 open until they fly | Holds D1 for a capability the program schedules for D4 |

## Consequences
- D1 closes without vision-only flight being shown, because the exit test does not list it. If the owner rejects this proposal, V-01 to V-03 reopen in a new work order. The 0.5 m `COM_POS_FS_EPH` setting and the origin-error behaviour stay **not run**.
- D4's work order inherits these four cases and their specified responses.
- Anything before D4 that relies on the vision-only rows relies on estimates.

## Reversibility
Cheap. The owner can reject this and have the cases debugged in a new work order. The cases and their logs stay in the record either way.
