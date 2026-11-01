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
- Before flight, the node enters offboard first, repeating the mode command until PX4 accepts. It arms only from offboard, and sends neither after the first arm (`arming_step`). If the vehicle disarms later, the node stops. A takeover before flight was not tested at the time of this decision; R-07 tests one (below).
- **Added 2026-11-01, WO-016: before flight, the node asks for offboard only from Hold,** PX4's state when nobody has chosen a mode. Any other state, leaving offboard once in it, or being armed outside offboard means the operator or PX4 has chosen, so the latch becomes `operator` and the node sends nothing more. WO-004 did not have this rule: its node took the aircraft from Position to Offboard, then armed it.
- Limits of that rule. An operator who selects Hold while already in Hold cannot be seen. A node acting on a status older than the operator's switch can still send one offboard command, and no case tests that window. A mode switch already away from Hold at boot means the node yields and the mission does not start, which fails safe but has only been seen in simulation.

## Evidence
`reports/WO-004-d1-fault-matrix-and-freshness-gate.md`, `reports/WO-016-preflight-mode-override.md`, `tests/test_faults.py`. Simulation only.
