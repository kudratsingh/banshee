"""The gate's response, injection windows and fault analysis. Fabricated data; no simulator."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest

from banshee.faults.analyze import check, motion, timeline, to_boot_us, yaw_change
from banshee.faults.case_env import RC_ENV, env_lines, timeline_lines
from banshee.faults.injection import Injection, Window, from_case
from banshee.faults.rc_sim import CENTER, channels_at
from banshee.faults.run_matrix import export_case
from banshee.offboard.response import NAV_DESCEND, NAV_LAND, NAV_LOITER, NAV_OFFBOARD, respond

ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "evals/D1-fault-matrix.json").read_text(encoding="utf-8"))


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


def test_every_matrix_case_parses_and_names_its_specification() -> None:
    ids = [case["id"] for case in MATRIX["cases"]]
    assert len(ids) == len(set(ids))
    for case in MATRIX["cases"]:
        assert case["configured"] and case["title"] and "expect" in case
        assert from_case(case).case_id == case["id"]


def test_the_matrix_covers_every_case_the_exit_test_lists() -> None:
    titles = " ".join(case["title"].lower() for case in MATRIX["cases"])
    for needle in (
        "stale setpoint while the heartbeat",
        "lost command stream",
        "stale sensor",
        "missing depth",
        "localization reset",
        "localization loss",
        "delayed planner",
        "low energy",
        "operator takeover",
    ):
        assert needle in titles


def test_case_files_are_shell_safe_and_timed() -> None:
    assert "export A='b c'" in env_lines({"env": {"A": "b c"}})
    assert any(
        line.startswith("export PX4_PARAM_COM_RC_IN_MODE=0") for line in env_lines({"rc": True})
    )
    assert RC_ENV["PX4_PARAM_COM_RCL_EXCEPT"] == 0
    assert timeline_lines([[2, "b"], [0, "a"], [2.5, "c"]]) == [
        "a",
        "sleep 2.000",
        "b",
        "sleep 0.500",
        "c",
    ]


def test_rc_channels_follow_events_and_stop() -> None:
    events = [{"t_s": 1, "set": {"5": 2000}}, {"t_s": 3, "stop": True}]
    assert channels_at(CENTER, events, None) == CENTER
    assert channels_at(CENTER, events, 0.5) == CENTER
    after = channels_at(CENTER, events, 2.0)
    assert after is not None and after[4] == 2000
    assert channels_at(CENTER, events, 3.5) is None
    assert CENTER[4] == 1000


def test_dds_times_map_to_the_boot_clock() -> None:
    data = {"timesync_status": {"estimated_offset": [-100, -102, -101]}}
    assert to_boot_us(data, 1000) == 899


def test_timeline_keeps_only_changes_from_the_trigger() -> None:
    status = {
        "timestamp": [0, 1_000_000, 2_000_000],
        "nav_state": [14, 14, 4],
        "arming_state": [2, 2, 2],
    }
    assert timeline(status, 1_000_000) == [
        {"t_s": -1.0, "nav": 14, "arming": 2},
        {"t_s": 1.0, "nav": 4, "arming": 2},
    ]


def test_motion_measures_stop_distance() -> None:
    track = [(0.0, 0.0, 0.0, 5.0, 2.5), (1e6, 1.0, 0.0, 5.0, 1.0), (2e6, 1.5, 0.0, 6.0, 0.05)]
    measured = motion(track, 0)
    assert measured["stop_distance_m"] == 1.5 and measured["stop_time_s"] == 2.0
    assert measured["vertical_travel_m"] == 1.0


def test_yaw_change_unwraps_counter_clockwise() -> None:
    steps = [
        {"since_trigger_s": 0.0, "yaw_enu_rad": 3.0},
        {"since_trigger_s": 1.0, "yaw_enu_rad": -3.0},
    ]
    change = yaw_change(steps)
    assert change is not None and change == pytest.approx(2 * math.pi - 6.0)


def _tested(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "timeline": [{"t_s": -1.0, "nav": 14, "arming": 2}, {"t_s": 1.2, "nav": 4, "arming": 2}],
        "ever_armed": True,
        "armed_at_end": True,
        "gate_modes_after_trigger": ["hold"],
        "final_latch": "hold",
        "yaw_change_rad": None,
        "max_up_m": 5.0,
        "max_radius_m": 10.0,
        "peak_speed_m_s": 2.0,
        "horizontal_travel_m": 1.0,
    }
    values.update(overrides)
    return values


def test_a_met_specification_has_no_deviation() -> None:
    expect = {"nav": [{"state": 4, "within_s": 1.5}], "gate_mode": "hold", "final_latch": "hold"}
    assert all(r["match"] for r in check(expect, _tested(), []))


@pytest.mark.parametrize(
    ("expect", "tested"),
    [
        ({"nav": [{"state": 4, "within_s": 1.0}]}, {}),
        ({"nav": [{"state": 18, "within_s": 9.0}]}, {}),
        ({"nav_never": [4]}, {}),
        ({"never_armed": True}, {}),
        ({"armed_at_end": False}, {}),
        ({"gate_mode": "land"}, {}),
        ({"final_latch": "land"}, {}),
        ({"max_peak_speed_m_s": 1.0}, {}),
        ({"yaw_ccw": True}, {"yaw_change_rad": -1.0}),
        ({"yaw_ccw": True}, {"yaw_change_rad": 0.01}),
    ],
)
def test_a_missed_specification_is_a_deviation(
    expect: dict[str, Any], tested: dict[str, Any]
) -> None:
    assert not all(r["match"] for r in check(expect, _tested(**tested), []))


def test_an_empty_expectation_only_measures() -> None:
    assert check({}, _tested(), []) == []


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


def test_a_held_state_lost_at_once_is_a_deviation() -> None:
    after = {
        "timeline": [{"t_s": 2.1, "nav": 1, "arming": 2}, {"t_s": 2.2, "nav": 12, "arming": 2}],
    }
    expect = {"nav": [{"state": 1, "within_s": 4.0, "holds_s": 15.0}]}
    results = check(expect, _tested(**after), [], 25.0)
    assert [r["match"] for r in results] == [True, False]
    kept = {"timeline": [{"t_s": 2.1, "nav": 1, "arming": 2}, {"t_s": 9.0, "nav": 1, "arming": 1}]}
    results = check(expect, _tested(**kept), [], 25.0)
    assert [r["match"] for r in results] == [True, True]


def test_a_case_without_steps_has_no_episode_and_says_why(tmp_path: Path) -> None:
    case = {"id": "X-01", "title": "x", "fly": {}}
    result = export_case(tmp_path, tmp_path, case, {"run_id": "r", "executed": True})
    assert result == "not exported: no steps logged"


def test_the_logged_action_is_the_one_a_frame_fault_transmits() -> None:
    action = (1.0, 2.0, 0.5, 0.1)
    assert Injection().at_boundary(action) == action
    assert Injection(swap_axes=True).at_boundary(action) == (2.0, 1.0, 0.5, 0.1)
    assert Injection(flip_east=True).at_boundary(action) == (-1.0, 2.0, 0.5, 0.1)


def test_never_armed_needs_the_command_to_have_been_sent() -> None:
    expect = {"never_armed": True, "arm_attempted": True}
    silent = check(expect, _tested(ever_armed=False, arm_commands=0), [])
    assert [r["match"] for r in silent] == [False, True]
    asked = check(expect, _tested(ever_armed=False, arm_commands=2), [])
    assert all(r["match"] for r in asked)
