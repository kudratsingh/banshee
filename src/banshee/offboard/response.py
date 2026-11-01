"""What the mission node does with the gate's verdict. Pure logic; no ROS.

``docs/TEST_PROTOCOL.md §2``: hold when position is valid and only the planner or a sensor is
stale; land when localization is lost; always yield to the operator. A verdict latches, because
stopping the setpoints alone may not be a response while the heartbeat runs; WO-004 measures that.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..freshness import Mode

Latch = Literal["none", "hold", "land", "operator"]
Command = Literal["none", "hold", "land"]

NAV_LOITER = 4
NAV_OFFBOARD = 14
NAV_LAND = 18
TARGET_NAV = {"hold": NAV_LOITER, "land": NAV_LAND}


@dataclass(frozen=True)
class Response:
    latch: Latch
    command: Command
    send_setpoint: bool
    send_heartbeat: bool


def respond(
    latch: Latch, mode: Mode, nav_state: int, *, in_flight: bool, reached_target: bool
) -> Response:
    """The next latch and what to send. ``in_flight``: armed under this node's offboard control.

    A mode change that this node did not ask for is the operator or PX4 taking over, so the node
    stops sending anything. A hold can escalate to a land; nothing goes back to offboard.
    """
    if latch == "operator" or mode == "operator":
        return Response("operator", "none", False, False)
    if not in_flight:
        return Response(latch, "none", mode == "continue" and latch == "none", latch == "none")
    if latch == "none":
        if nav_state != NAV_OFFBOARD:
            return Response("operator", "none", False, False)
        if mode == "continue":
            return Response("none", "none", True, True)
        latch = "land" if mode == "land" else "hold"
    elif latch == "hold" and mode == "land":
        latch = "land"
        reached_target = False
    if reached_target and nav_state != TARGET_NAV[latch]:
        return Response("operator", "none", False, False)
    command: Command = "none" if nav_state == TARGET_NAV[latch] else latch
    return Response(latch, command, False, False)
