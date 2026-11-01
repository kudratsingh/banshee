"""What the mission node does with the gate's verdict. Pure logic; no ROS.

``docs/TEST_PROTOCOL.md §2``: hold when position is valid and only the planner or a sensor is
stale; land when localization is lost; always yield to the operator. A verdict latches, because
stopping the setpoints alone may not be a response while the heartbeat runs; WO-004 measures that.

The node commands only while the vehicle is still in the state it decided from. Any other state
means the operator or PX4 is in charge, so the command must not be sent again (ADR-0009).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..freshness import Mode

Latch = Literal["none", "hold", "land", "operator"]
Command = Literal["none", "hold", "land"]

NAV_LOITER = 4
NAV_DESCEND = 12
NAV_OFFBOARD = 14
NAV_LAND = 18
# PX4 flies Land as Descend when it has no position, so either one is the land response.
TARGET_NAV = {"hold": frozenset({NAV_LOITER}), "land": frozenset({NAV_LAND, NAV_DESCEND})}


@dataclass(frozen=True)
class Response:
    latch: Latch
    command: Command
    send_setpoint: bool
    send_heartbeat: bool
    pending_from: int = NAV_OFFBOARD


def arming_step(nav_state: int, was_armed: bool) -> Literal["none", "mode", "arm"]:
    """Before flight: offboard first, and arm only from offboard. Nothing after the first arm.

    Sent together, PX4 can accept the arm and refuse the mode, which leaves it armed in Hold. And
    arming again after a disarm would override the operator.
    """
    if was_armed:
        return "none"
    return "arm" if nav_state == NAV_OFFBOARD else "mode"


def respond(
    latch: Latch,
    mode: Mode,
    nav_state: int,
    *,
    in_flight: bool,
    reached_target: bool,
    pending_from: int = NAV_OFFBOARD,
) -> Response:
    """The next latch and what to send. ``in_flight``: armed under this node's offboard control.

    ``pending_from`` is the state the node was in when it decided. A mode change that this node did
    not ask for is the operator or PX4 taking over, so the node stops sending anything. A hold can
    escalate to a land; nothing goes back to offboard.
    """
    operator = Response("operator", "none", False, False, pending_from)
    if latch == "operator" or mode == "operator":
        return operator
    if not in_flight:
        send = latch == "none"
        return Response(latch, "none", mode == "continue" and send, send, pending_from)
    if latch == "none":
        if nav_state != NAV_OFFBOARD:
            return operator
        if mode == "continue":
            return Response("none", "none", True, True, pending_from)
        latch = "land" if mode == "land" else "hold"
        pending_from = nav_state
    else:
        if nav_state not in TARGET_NAV[latch] and (reached_target or nav_state != pending_from):
            return operator
        if latch == "hold" and mode == "land":
            latch = "land"
            reached_target = False
            pending_from = nav_state
    if nav_state in TARGET_NAV[latch]:
        return Response(latch, "none", False, False, pending_from)
    return Response(latch, latch, False, False, pending_from)
