# ADR-0009 — The gate's response latches, and yields to the operator

**Date:** 2026-11-01 · **Status:** accepted · **Work order:** WO-004 · **Program link:** PROGRAM §5.1

## Context
`docs/TEST_PROTOCOL.md §2` asks for hold when position is valid and only the planner or a sensor is stale, land when localization is lost, and always allowing operator takeover. WO-004's controls measured that stopping setpoints is not a response on its own: with the heartbeat running, PX4 flew the last setpoint for 29.7 m, until the fence (H-04).

In the first recording, the node also repeated Land over an operator's Altitude switch, and took the aircraft back after 84 ms (R-06), because PX4 flew Land as Descend and the node never counted it as reached.

## Decision
`src/banshee/offboard/response.py` is a pure function with these rules.
- A stale verdict latches `hold`, and localization loss latches `land`. A hold can escalate to a land. Nothing returns to offboard.
- A latch sends a mode command and stops setpoints and heartbeat.
- Land and Descend both count as the land response.
- **The node commands only while the vehicle is in the state it decided from.** Any other state means the operator or PX4 has taken over, so the latch becomes `operator` and the node sends nothing again.

## Consequences
- A takeover needs no acknowledgement from the node, and the node cannot override it.
- A PX4 failsafe also ends the node's commands, so PX4's choice stands. For example, if the node decides Land and PX4 moves to Hold first, the aircraft follows PX4's sequence.
- This covers the node only. Commands from PX4 failsafes can still override an operator, and `COM_FAIL_ACT_T` applies there.
- Before flight, the node still repeats its mode and arm commands in the `stream` phase. Takeover there was not tested.

## Evidence
`reports/WO-004-d1-fault-matrix-and-freshness-gate.md`, `tests/test_faults.py`. Simulation only.
