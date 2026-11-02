"""The command gate: the only path from a requested velocity to a transmitted one.

It clamps a request to the limits and asks ``freshness.assess`` whether to forward it. Heartbeat
continuity never counts as setpoint freshness. Velocities in ENU m/s, yaw rate in FLU rad/s, times
in monotonic ns. It refuses nothing silently: every decision carries its reasons.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from .freshness import FreshnessBounds, GateInputs, Mode, assess

Action = tuple[float, float, float, float]


@dataclass(frozen=True)
class CommandLimits:
    """Speed limits: horizontal magnitude, climb, commanded descent (m/s); yaw rate (rad/s)."""

    max_horizontal_m_s: float
    max_climb_m_s: float
    max_descent_m_s: float
    max_yaw_rate_rad_s: float = 0.5


@dataclass(frozen=True)
class GateDecision:
    """``filtered`` is the clamped request; it is transmitted only if ``forward``."""

    forward: bool
    filtered: Action
    mode: Mode
    reasons: tuple[str, ...]


def clamp(requested: Action, limits: CommandLimits) -> Action:
    """Limit an action: non-finite values become 0, and horizontal keeps its direction."""
    vx, vy, vz, rate = (value if math.isfinite(value) else 0.0 for value in requested)
    speed = math.hypot(vx, vy)
    if speed > limits.max_horizontal_m_s:
        scale = limits.max_horizontal_m_s / speed
        vx, vy = vx * scale, vy * scale
    vz = max(-limits.max_descent_m_s, min(limits.max_climb_m_s, vz))
    rate = max(-limits.max_yaw_rate_rad_s, min(limits.max_yaw_rate_rad_s, rate))
    return (vx, vy, vz, rate)


def decide(
    requested: Action, inputs: GateInputs, bounds: FreshnessBounds, limits: CommandLimits
) -> GateDecision:
    """Clamp ``requested`` and decide from freshness and estimator validity alone."""
    verdict = assess(inputs, bounds)
    return GateDecision(
        verdict.forward_setpoint, clamp(requested, limits), verdict.mode, verdict.reasons
    )


def load_frozen(path: Path) -> tuple[FreshnessBounds, CommandLimits]:
    """Read the frozen bounds and the simulation limits from ``evals/D1-exit-tests.json``."""
    data = json.loads(path.read_text(encoding="utf-8"))
    fresh = data["freshness_bounds"]
    sim = data["sim_limits"]
    return (
        FreshnessBounds(
            fresh["max_setpoint_age_ns"], fresh["max_sensor_age_ns"], fresh["max_estimator_age_ns"]
        ),
        CommandLimits(
            sim["max_horizontal_speed_m_s"], sim["max_climb_m_s"], sim["max_commanded_descent_m_s"]
        ),
    )
