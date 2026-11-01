"""Frames, gate, guidance, outcome, export and lock checks. Fabricated data; no simulator."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest
from ironclad.contracts.v1.validate import ContractError

from banshee.export.episode import export_run
from banshee.freshness import FreshnessBounds, GateInputs
from banshee.offboard.frames import (
    enu_to_ned,
    ned_to_enu,
    yaw_enu_from_ned,
    yaw_ned_from_quaternion,
    yaw_rate_flu_to_frd,
)
from banshee.offboard.gate import CommandLimits, clamp, decide, load_frozen
from banshee.offboard.guidance import RouteFollower, load_route, velocity_toward
from banshee.outcome.truth_check import closest_per_waypoint, enu_from_ned, truth_outcome
from banshee.outcome.waypoints import judge, tolerance_from_evals
from banshee.sitl.launch import differences

ROOT = Path(__file__).resolve().parents[1]
BOUNDS = FreshnessBounds(200_000_000, 150_000_000, 100_000_000)
LIMITS = CommandLimits(2.5, 1.0, 0.5)
NOW = 10_000_000_000


def _inputs(**overrides: Any) -> GateInputs:
    values: dict[str, Any] = {
        "now_ns": NOW,
        "last_setpoint_ns": NOW,
        "last_sensor_ns": NOW,
        "estimator_valid": True,
        "last_estimator_ns": NOW,
    }
    values.update(overrides)
    return GateInputs(**values)


@pytest.mark.parametrize(
    ("enu", "ned"),
    [
        ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),  # east is NED y
        ((0.0, 1.0, 0.0), (1.0, 0.0, 0.0)),  # north is NED x
        ((0.0, 0.0, 1.0), (0.0, 0.0, -1.0)),  # up is negative down
    ],
)
def test_each_axis_and_sign_at_the_px4_boundary(enu: Any, ned: Any) -> None:
    assert enu_to_ned(enu) == ned
    assert ned_to_enu(ned) == enu


def test_yaw_conversions_keep_direction() -> None:
    assert yaw_rate_flu_to_frd(0.3) == -0.3
    assert yaw_enu_from_ned(0.0) == pytest.approx(math.pi / 2)  # facing north
    assert yaw_enu_from_ned(math.pi / 2) == pytest.approx(0.0)  # facing east
    half = math.pi / 4
    assert yaw_ned_from_quaternion(math.cos(half), 0, 0, math.sin(half)) == pytest.approx(
        math.pi / 2
    )


def test_clamp_keeps_horizontal_direction_and_separate_vertical_limits() -> None:
    vx, vy, vz, rate = clamp((30.0, 40.0, 9.0, 9.0), LIMITS)
    assert math.hypot(vx, vy) == pytest.approx(2.5)
    assert vy / vx == pytest.approx(40.0 / 30.0)
    assert (vz, rate) == (1.0, 0.5)
    assert clamp((0.0, 0.0, -9.0, -9.0), LIMITS)[2:] == (-0.5, -0.5)


def test_clamp_turns_non_finite_values_into_zero() -> None:
    assert clamp((math.nan, math.inf, -math.inf, math.nan), LIMITS) == (0.0, 0.0, 0.0, 0.0)


def test_gate_forwards_only_when_fresh() -> None:
    assert decide((1.0, 0.0, 0.0, 0.0), _inputs(), BOUNDS, LIMITS).forward


@pytest.mark.parametrize(
    ("overrides", "mode"),
    [
        ({"last_setpoint_ns": NOW - 300_000_000}, "hold"),
        ({"last_sensor_ns": NOW - 300_000_000}, "hold"),
        ({"estimator_valid": False}, "land"),
        ({"last_estimator_ns": NOW - 300_000_000}, "land"),
        ({"operator_takeover": True}, "operator"),
    ],
)
def test_gate_holds_back_stale_or_invalid_input(overrides: dict[str, Any], mode: str) -> None:
    decision = decide((1.0, 0.0, 0.0, 0.0), _inputs(**overrides), BOUNDS, LIMITS)
    assert not decision.forward
    assert decision.mode == mode
    assert decision.reasons


def test_heartbeat_never_counts_as_freshness() -> None:
    stale = _inputs(last_setpoint_ns=NOW - 300_000_000, heartbeat_ok=True)
    assert not decide((1.0, 0.0, 0.0, 0.0), stale, BOUNDS, LIMITS).forward


def test_frozen_bounds_and_route_load_and_agree() -> None:
    bounds, limits = load_frozen(ROOT / "evals/D1-exit-tests.json")
    assert bounds == BOUNDS
    route = load_route(ROOT / "evals/D1-route.json")
    assert route.speed_m_s <= limits.max_horizontal_m_s
    assert tolerance_from_evals(ROOT / "evals/D1-exit-tests.json") == 0.5
    assert route.arrival_radius_m < 0.5


def test_follower_walks_the_route_in_order() -> None:
    route = load_route(ROOT / "evals/D1-route.json")
    follower = RouteFollower(route)
    assert follower.step((0.0, 0.0, 0.0)) is not None and follower.index == 0
    velocity = velocity_toward((0.0, 0.0, 5.0), (10.0, 0.0, 5.0), route)
    assert velocity == pytest.approx((route.speed_m_s, 0.0, 0.0))
    assert follower.step((0.0, 0.0, 5.0)) is not None and follower.index == 1
    for waypoint in route.waypoints:
        follower.step(waypoint)
    assert follower.step(route.waypoints[-1]) is None


def _step(position: list[float], arming: int = 2, valid: bool = True, t: int = 0) -> dict[str, Any]:
    return {
        "t_ns": 1000 + t * 50,
        "phase": "route",
        "position_enu_m": position,
        "velocity_enu_m_s": [0.0, 0.0, 0.0],
        "yaw_enu_rad": 0.0,
        "capture_t_ns": 900 + t * 50,
        "received_t_ns": 950 + t * 50,
        "estimator_valid": valid,
        "arming_state": arming,
        "requested": [0.0, 0.0, 0.0, 0.0],
        "filtered": [0.0, 0.0, 0.0, 0.0],
        "transmitted": [0.0, 0.0, 0.0, 0.0],
        "sent_t_ns": 1001 + t * 50,
        "valid_until_t_ns": 2000 + t * 50,
    }


WAYPOINTS = [[0.0, 0.0, 5.0], [10.0, 0.0, 5.0]]


def test_outcome_needs_every_waypoint_in_order_and_a_landing() -> None:
    steps = [_step([0.0, 0.0, 5.0]), _step([10.0, 0.0, 5.0]), _step([10.0, 0.0, 0.0], arming=1)]
    result = judge(steps, WAYPOINTS, 0.5)
    assert result["success"] and result["waypoints_reached"] == 2


@pytest.mark.parametrize(
    "steps",
    [
        pytest.param(
            [_step([10.0, 0.0, 5.0]), _step([0.0, 0.0, 5.0], arming=1)], id="out-of-order"
        ),
        pytest.param(
            [_step([0.0, 0.0, 5.0]), _step([10.0, 0.0, 5.0])],
            id="never-landed",
        ),
        pytest.param(
            [_step([0.0, 0.0, 5.0]), _step([10.6, 0.0, 5.0]), _step([10.6, 0.0, 0.0], arming=1)],
            id="outside-tolerance",
        ),
        pytest.param(
            [
                _step([0.0, 0.0, 5.0]),
                _step([10.0, 0.0, 5.0], valid=False),
                _step([9.0, 0.0, 0.0], arming=1),
            ],
            id="estimator-invalid",
        ),
    ],
)
def test_outcome_rejects_a_bad_flight(steps: list[dict[str, Any]]) -> None:
    assert not judge(steps, WAYPOINTS, 0.5)["success"]


def test_truth_check_converts_axes_and_finds_the_closest_point() -> None:
    assert enu_from_ned(1.0, 2.0, -3.0) == (2.0, 1.0, 3.0)
    track = [(0.0, 0.0, 0.0), (3.0, 4.0, 0.0)]
    assert closest_per_waypoint(track, [(3.0, 4.0, 1.0), (0.0, 0.0, 0.0)]) == [1.0, 0.0]


def test_truth_outcome_needs_route_order() -> None:
    forward = [(0.0, 0.0, 5.0), (5.0, 0.0, 5.0), (10.0, 0.0, 5.0)]
    assert truth_outcome(forward, WAYPOINTS, 0.5)["success"]
    assert not truth_outcome(list(reversed(forward)), WAYPOINTS, 0.5)["success"]
    # A swapped x and y misses the route, even though the two axes look alike on a square.
    swapped = [(0.0, 0.0, 5.0), (0.0, 10.0, 5.0)]
    assert not truth_outcome(swapped, WAYPOINTS, 0.5)["success"]


def test_export_marks_an_invalid_estimate_as_an_invalid_observation(tmp_path: Path) -> None:
    steps = [_step([0.0, 0.0, 5.0], t=0, valid=False), _step([1.0, 0.0, 5.0], t=1)]
    path = export_run(
        steps,
        run_id="invalid",
        created_at="2026-10-31T00:00:00+00:00",
        route={"route_id": "fixture-route", "waypoints_enu_m": WAYPOINTS},
        limits={
            "max_horizontal_speed_m_s": 2.5,
            "max_climb_m_s": 1.0,
            "max_commanded_descent_m_s": 0.5,
        },
        outcome=judge(steps, WAYPOINTS, 0.5),
        stack={"gz_sim": "8.15.0", "px4": "fixture"},
        target_dir=tmp_path / "episode",
        tolerance_m=0.5,
    )
    first = json.loads((path / "transitions.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert first["observations"][0]["valid"] is False
    assert first["observations"][0]["value"] is None
    manifest = json.loads((path / "episode.json").read_text(encoding="utf-8"))
    assert manifest["simulator"]["version"] == "8.15.0"


def test_outcome_does_not_import_the_planner() -> None:
    for name in ("waypoints.py", "truth_check.py"):
        source = (ROOT / "src/banshee/outcome" / name).read_text(encoding="utf-8")
        assert "banshee.offboard" not in source and "guidance" not in source


def test_export_writes_a_valid_episode_once(tmp_path: Path) -> None:
    steps = [
        _step([0.0, 0.0, 5.0], t=0),
        _step([10.0, 0.0, 5.0], t=1),
        _step([10.0, 0.0, 0.0], 1, t=2),
    ]
    outcome = judge(steps, WAYPOINTS, 0.5)
    kwargs: dict[str, Any] = {
        "run_id": "fixture",
        "created_at": "2026-10-31T00:00:00+00:00",
        "route": {"route_id": "fixture-route", "waypoints_enu_m": WAYPOINTS},
        "limits": {
            "max_horizontal_speed_m_s": 2.5,
            "max_climb_m_s": 1.0,
            "max_commanded_descent_m_s": 0.5,
        },
        "outcome": outcome,
        "stack": {"gazebo": "fixture", "px4": "fixture"},
        "target_dir": tmp_path / "episode",
        "tolerance_m": 0.5,
    }
    path = export_run(steps, **kwargs)
    assert (path / "episode.json").exists() and (path / "transitions.jsonl").exists()
    with pytest.raises(ContractError):
        export_run(steps, **kwargs)


def test_export_records_a_held_back_step_and_a_failed_flight(tmp_path: Path) -> None:
    held = {**_step([0.0, 0.0, 5.0], t=0), "transmitted": None, "sent_t_ns": None}
    steps = [held, _step([1.0, 0.0, 5.0], t=1)]
    outcome = judge(steps, WAYPOINTS, 0.5)
    assert not outcome["success"]
    path = export_run(
        steps,
        run_id="failed",
        created_at="2026-10-31T00:00:00+00:00",
        route={"route_id": "fixture-route", "waypoints_enu_m": WAYPOINTS},
        limits={
            "max_horizontal_speed_m_s": 2.5,
            "max_climb_m_s": 1.0,
            "max_commanded_descent_m_s": 0.5,
        },
        outcome=outcome,
        stack={"gazebo": "fixture", "px4": "fixture"},
        target_dir=tmp_path / "episode",
        tolerance_m=0.5,
    )
    manifest = json.loads((path / "episode.json").read_text(encoding="utf-8"))
    assert manifest["outcome"]["success"] is False and manifest["outcome"]["truncated"] is True
    first = json.loads((path / "transitions.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert first["action"]["transmitted"] is None


def test_lock_check_refuses_a_difference_or_a_null_pin() -> None:
    keys = ("os", "ros2", "gazebo", "gz_sim", "px4", "agent", "px4_msgs")
    lock = dict.fromkeys(keys, "a")
    assert differences(dict(lock), lock) == []
    assert any(p.startswith("px4:") for p in differences({**lock, "px4": "b"}, lock))
    assert any("null pin" in p for p in differences(lock, {**lock, "agent": ""}))
