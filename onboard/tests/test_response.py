"""Moved from tests/test_faults.py with the onboard package (WO-027); runs on Python 3.10."""

from __future__ import annotations

import math
from typing import Any

import pytest

from banshee_onboard.injection import Injection, Window
from banshee_onboard.response import (
    NAV_DESCEND,
    NAV_LAND,
    NAV_LOITER,
    NAV_OFFBOARD,
    NAV_UNKNOWN,
    arming_step,
    respond,
)


def _respond(latch: Any, mode: Any, nav: int, reached: bool = False, flying: bool = True) -> Any:
    return respond(latch, mode, nav, in_flight=flying, reached_target=reached)


def test_continue_sends_setpoint_and_heartbeat() -> None:
    r = _respond("none", "continue", NAV_OFFBOARD)
    assert (r.latch, r.command, r.send_setpoint, r.send_heartbeat) == ("none", "none", True, True)


@pytest.mark.parametrize(("mode", "latch"), [("hold", "hold"), ("land", "land")])
def test_a_stale_verdict_latches_and_commands_and_stops_the_stream(mode: Any, latch: str) -> None:
    r = _respond("none", mode, NAV_OFFBOARD)
    assert (r.latch, r.command) == (latch, latch)
    assert not r.send_setpoint and not r.send_heartbeat


def test_a_latch_does_not_return_when_the_verdict_recovers() -> None:
    r = _respond("hold", "continue", NAV_LOITER, reached=True)
    assert (r.latch, r.command, r.send_setpoint) == ("hold", "none", False)


def test_hold_escalates_to_land_and_never_back() -> None:
    assert _respond("hold", "land", NAV_LOITER, reached=True).command == "land"
    assert _respond("land", "hold", NAV_LAND, reached=True).latch == "land"


def test_a_mode_change_this_node_did_not_ask_for_is_the_operator() -> None:
    position = 2
    r = _respond("none", "continue", position)
    assert (r.latch, r.command, r.send_setpoint, r.send_heartbeat) == (
        "operator",
        "none",
        False,
        False,
    )
    assert _respond("hold", "continue", position, reached=True).latch == "operator"
    assert _respond("operator", "continue", NAV_OFFBOARD).latch == "operator"


def test_before_flight_a_stale_tick_does_not_latch() -> None:
    r = _respond("none", "hold", NAV_LOITER, flying=False)
    assert (r.latch, r.command, r.send_setpoint, r.send_heartbeat) == ("none", "none", False, True)


def test_windows() -> None:
    assert not Window().active(1.0)
    assert not Window(1.0).active(None)
    assert Window(1.0).active(0.5) and not Window(1.0).active(1.5)
    assert Window(math.inf).active(1e6)
    repeat = Window(0.15, every_s=1.0)
    assert repeat.active(2.1) and not repeat.active(2.5)
    assert Window(1.0, start_s=2.0).active(2.5) and not Window(1.0, start_s=2.0).active(1.0)


def test_the_default_injection_is_the_nominal_mission() -> None:
    fault = Injection()
    assert not fault.is_case and fault.gate_response and fault.scale == 1.0


@pytest.mark.parametrize("nav", [NAV_LAND, NAV_DESCEND])
def test_land_is_reached_in_land_or_descend(nav: int) -> None:
    assert _respond("land", "land", nav).command == "none"
    assert _respond("land", "land", nav).latch == "land"


def test_the_operator_keeps_control_from_a_land_latch_px4_is_flying_as_descend() -> None:
    """R-06, first recording: the node repeated Land and took Altitude mode back after 84 ms."""
    assert _respond("land", "land", NAV_DESCEND, reached=True).command == "none"
    altitude = 1
    r = _respond("land", "land", altitude, reached=True)
    assert (r.latch, r.command) == ("operator", "none")


@pytest.mark.parametrize("latch", ["hold", "land"])
def test_the_operator_keeps_control_before_the_target_is_reached(latch: Any) -> None:
    position = 2
    r = _respond(latch, latch, position)
    assert (r.latch, r.command) == ("operator", "none")


def test_a_pending_command_repeats_only_from_the_state_it_was_decided_in() -> None:
    assert _respond("land", "land", NAV_OFFBOARD).command == "land"
    assert _respond("land", "land", NAV_LOITER).latch == "operator"


def test_a_hold_escalates_to_land_from_loiter_and_then_yields() -> None:
    r = _respond("hold", "land", NAV_LOITER, reached=True)
    assert (r.latch, r.command, r.pending_from) == ("land", "land", NAV_LOITER)
    still = respond(
        "land",
        "land",
        NAV_LOITER,
        in_flight=True,
        reached_target=False,
        pending_from=r.pending_from,
    )
    assert still.command == "land"
    left = respond(
        "land", "land", 2, in_flight=True, reached_target=False, pending_from=r.pending_from
    )
    assert (left.latch, left.command) == ("operator", "none")


def test_a_hold_does_not_escalate_over_the_operator() -> None:
    r = _respond("hold", "land", 2, reached=True)
    assert (r.latch, r.command) == ("operator", "none")


def test_arming_needs_offboard_first_and_happens_once() -> None:
    assert arming_step(NAV_LOITER, was_armed=False, offboard_seen=False) == "mode"
    assert arming_step(NAV_OFFBOARD, was_armed=False, offboard_seen=False) == "arm"
    assert arming_step(NAV_OFFBOARD, was_armed=False, offboard_seen=True) == "arm"
    assert arming_step(NAV_OFFBOARD, was_armed=True, offboard_seen=True) == "none"


def test_before_flight_the_node_never_overrides_a_chosen_mode() -> None:
    position = 2
    # A mode chosen while disarmed, whether or not the node had reached offboard.
    assert arming_step(position, was_armed=False, offboard_seen=False) == "yield"
    assert arming_step(position, was_armed=False, offboard_seen=True) == "yield"
    # Back to Hold from offboard is also a choice, so the node must not ask for offboard again.
    assert arming_step(NAV_LOITER, was_armed=False, offboard_seen=True) == "yield"
    # Armed outside offboard: someone else is in charge.
    assert arming_step(NAV_LOITER, was_armed=True, offboard_seen=True) == "yield"
    assert arming_step(position, was_armed=True, offboard_seen=True) == "yield"
    # No status yet: nothing is known, so nothing is sent.
    assert arming_step(NAV_UNKNOWN, was_armed=False, offboard_seen=False) == "none"
