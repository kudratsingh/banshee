"""Setpoint-freshness and estimator-validity gate (pure logic, no I/O, no ROS).

The gate answers one question before any offboard setpoint is sent: *is it safe to keep flying on
the planner's commands right now, and if not, what should the aircraft do instead?* It decides from
three independent facts — how old the newest setpoint is, how old the newest sensor input is, and
whether the state estimator is valid and recent — and never from the ROS 2 offboard heartbeat, which
PX4 treats separately from the setpoint stream (docs/SOURCES.md [S6]).

Recommended modes (the caller — the command gate — maps them to PX4 actions):

- ``continue``  everything fresh and valid: forward the setpoint.
- ``hold``      position estimate valid but planner/sensors stale: hold position, stop forwarding.
- ``land``      localization lost or stale: land (no position hold without a valid estimate).
- ``operator``  an operator takeover is active: forward nothing; the operator has the aircraft.

There is deliberately no universal "hover on any fault": the response depends on which estimates
remain valid (docs/TEST_PROTOCOL.md section 2). All times are integer nanoseconds in one monotonic
clock.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Mode = Literal["continue", "hold", "land", "operator"]


class BoundsError(ValueError):
    """Bounds must be positive integers (nanoseconds)."""


@dataclass(frozen=True)
class FreshnessBounds:
    """Frozen per stage in evals/<stage>-exit-tests.json; D1 defaults in TEST_PROTOCOL.md."""

    max_setpoint_age_ns: int
    max_sensor_age_ns: int
    max_estimator_age_ns: int

    def __post_init__(self) -> None:
        for name in ("max_setpoint_age_ns", "max_sensor_age_ns", "max_estimator_age_ns"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise BoundsError(f"{name} must be a positive integer number of nanoseconds")


@dataclass(frozen=True)
class GateInputs:
    """Everything the gate looks at. ``None`` means never received, which is stale by definition."""

    now_ns: int
    last_setpoint_ns: int | None
    last_sensor_ns: int | None
    estimator_valid: bool
    last_estimator_ns: int | None
    operator_takeover: bool = False
    heartbeat_ok: bool = True  # recorded for the log; never used to decide freshness


@dataclass(frozen=True)
class Verdict:
    """The gate's decision with every reason, for the structured log and the fault-matrix report."""

    forward_setpoint: bool
    mode: Mode
    reasons: tuple[str, ...]
    setpoint_age_ns: int | None
    sensor_age_ns: int | None
    estimator_age_ns: int | None


def _age(now_ns: int, stamp_ns: int | None) -> int | None:
    if stamp_ns is None:
        return None
    if stamp_ns > now_ns:
        # A timestamp from the future means a clock-domain error; treat as stale and say so.
        return None
    return now_ns - stamp_ns


def assess(inputs: GateInputs, bounds: FreshnessBounds) -> Verdict:
    """Decide whether to forward the current setpoint and which mode to recommend otherwise."""
    reasons: list[str] = []
    setpoint_age = _age(inputs.now_ns, inputs.last_setpoint_ns)
    sensor_age = _age(inputs.now_ns, inputs.last_sensor_ns)
    estimator_age = _age(inputs.now_ns, inputs.last_estimator_ns)

    if inputs.operator_takeover:
        return Verdict(
            False,
            "operator",
            ("operator takeover active",),
            setpoint_age,
            sensor_age,
            estimator_age,
        )

    estimator_ok = (
        inputs.estimator_valid
        and estimator_age is not None
        and estimator_age <= bounds.max_estimator_age_ns
    )
    if not inputs.estimator_valid:
        reasons.append("estimator reports invalid")
    elif estimator_age is None:
        reasons.append("estimator timestamp missing or from the future")
    elif estimator_age > bounds.max_estimator_age_ns:
        reasons.append(f"estimator stale: {estimator_age} ns > {bounds.max_estimator_age_ns} ns")

    if not estimator_ok:
        # Without a valid position estimate the aircraft cannot hold position; land.
        return Verdict(False, "land", tuple(reasons), setpoint_age, sensor_age, estimator_age)

    if setpoint_age is None:
        reasons.append("no setpoint received or setpoint timestamp invalid")
    elif setpoint_age > bounds.max_setpoint_age_ns:
        reasons.append(f"setpoint stale: {setpoint_age} ns > {bounds.max_setpoint_age_ns} ns")
    if sensor_age is None:
        reasons.append("no sensor input received or sensor timestamp invalid")
    elif sensor_age > bounds.max_sensor_age_ns:
        reasons.append(f"sensor stale: {sensor_age} ns > {bounds.max_sensor_age_ns} ns")

    if reasons:
        return Verdict(False, "hold", tuple(reasons), setpoint_age, sensor_age, estimator_age)
    return Verdict(True, "continue", (), setpoint_age, sensor_age, estimator_age)
