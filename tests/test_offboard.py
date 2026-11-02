"""Frames, gate, guidance, outcome, export and lock checks. Fabricated data; no simulator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from ironclad.contracts.v1.validate import ContractError

from banshee.export.episode import export_run
from banshee.outcome.truth_check import closest_per_waypoint, enu_from_ned, truth_outcome
from banshee.outcome.waypoints import judge, tolerance_from_evals
from banshee.sitl.launch import differences
from banshee_onboard.freshness import FreshnessBounds, GateInputs
from banshee_onboard.gate import CommandLimits, load_frozen
from banshee_onboard.guidance import load_route

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


def test_frozen_bounds_and_route_load_and_agree() -> None:
    bounds, limits = load_frozen(ROOT / "evals/D1-exit-tests.json")
    assert bounds == BOUNDS
    route = load_route(ROOT / "evals/D1-route.json")
    assert route.speed_m_s <= limits.max_horizontal_m_s
    assert tolerance_from_evals(ROOT / "evals/D1-exit-tests.json") == 0.5
    assert route.arrival_radius_m < 0.5


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
