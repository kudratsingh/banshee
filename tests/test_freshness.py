"""The freshness gate: estimator validity first, heartbeat never, no universal hover."""

from __future__ import annotations

import pytest

from banshee.freshness import BoundsError, FreshnessBounds, GateInputs, assess

MS = 1_000_000
BOUNDS = FreshnessBounds(
    max_setpoint_age_ns=200 * MS, max_sensor_age_ns=150 * MS, max_estimator_age_ns=100 * MS
)


def inputs(**overrides: object) -> GateInputs:
    base = {
        "now_ns": 10_000 * MS,
        "last_setpoint_ns": 9_950 * MS,
        "last_sensor_ns": 9_960 * MS,
        "estimator_valid": True,
        "last_estimator_ns": 9_970 * MS,
        "operator_takeover": False,
        "heartbeat_ok": True,
    }
    base.update(overrides)
    return GateInputs(**base)  # type: ignore[arg-type]


def test_all_fresh_forwards() -> None:
    verdict = assess(inputs(), BOUNDS)
    assert verdict.forward_setpoint is True
    assert verdict.mode == "continue"
    assert verdict.reasons == ()


def test_stale_setpoint_holds_when_estimator_valid() -> None:
    verdict = assess(inputs(last_setpoint_ns=9_700 * MS), BOUNDS)
    assert verdict.forward_setpoint is False
    assert verdict.mode == "hold"
    assert any("setpoint stale" in r for r in verdict.reasons)


def test_heartbeat_does_not_make_setpoint_fresh() -> None:
    verdict = assess(inputs(last_setpoint_ns=None, heartbeat_ok=True), BOUNDS)
    assert verdict.mode == "hold"
    assert any("no setpoint" in r for r in verdict.reasons)


def test_stale_sensor_holds() -> None:
    verdict = assess(inputs(last_sensor_ns=9_800 * MS), BOUNDS)
    assert verdict.mode == "hold"
    assert any("sensor stale" in r for r in verdict.reasons)


def test_invalid_estimator_lands_even_if_everything_else_fresh() -> None:
    verdict = assess(inputs(estimator_valid=False), BOUNDS)
    assert verdict.mode == "land"
    assert verdict.forward_setpoint is False


def test_stale_estimator_lands() -> None:
    verdict = assess(inputs(last_estimator_ns=9_800 * MS), BOUNDS)
    assert verdict.mode == "land"
    assert any("estimator stale" in r for r in verdict.reasons)


def test_future_timestamp_is_treated_as_invalid() -> None:
    verdict = assess(inputs(last_estimator_ns=10_500 * MS), BOUNDS)
    assert verdict.mode == "land"
    assert verdict.estimator_age_ns is None


def test_operator_takeover_wins() -> None:
    verdict = assess(inputs(operator_takeover=True, estimator_valid=False), BOUNDS)
    assert verdict.mode == "operator"
    assert verdict.forward_setpoint is False


def test_bounds_must_be_positive_integers() -> None:
    with pytest.raises(BoundsError):
        FreshnessBounds(0, 1, 1)
    with pytest.raises(BoundsError):
        FreshnessBounds(1, -5, 1)
    with pytest.raises(BoundsError):
        FreshnessBounds(1, 1, 1.5)  # type: ignore[arg-type]


def test_ages_are_reported_for_the_log() -> None:
    verdict = assess(inputs(), BOUNDS)
    assert verdict.setpoint_age_ns == 50 * MS
    assert verdict.sensor_age_ns == 40 * MS
    assert verdict.estimator_age_ns == 30 * MS
