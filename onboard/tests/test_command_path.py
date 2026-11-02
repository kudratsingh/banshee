"""Moved from tests/test_offboard.py with the onboard package (WO-027); runs on Python 3.10."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest

from banshee_onboard.frames import (
    enu_to_ned,
    ned_to_enu,
    yaw_enu_from_ned,
    yaw_ned_from_quaternion,
    yaw_rate_flu_to_frd,
)
from banshee_onboard.freshness import FreshnessBounds, GateInputs
from banshee_onboard.gate import CommandLimits, clamp, decide
from banshee_onboard.guidance import RouteFollower, load_route, velocity_toward

ROOT = Path(__file__).resolve().parents[2]


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
