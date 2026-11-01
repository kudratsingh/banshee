"""One case's faults, as read by the mission node. Pure; times are seconds after the trigger."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..offboard.guidance import Route

FOREVER_S = math.inf


@dataclass(frozen=True)
class Window:
    """Active from ``start_s`` for ``for_s``, repeating every ``every_s`` if that is set."""

    for_s: float = 0.0
    start_s: float = 0.0
    every_s: float | None = None

    def active(self, t_s: float | None) -> bool:
        if t_s is None or self.for_s <= 0.0 or t_s < self.start_s:
            return False
        elapsed = t_s - self.start_s
        if self.every_s is not None:
            elapsed %= self.every_s
        return elapsed < self.for_s


def _window(raw: Any) -> Window:
    if raw is None:
        return Window()
    if raw == "forever":
        return Window(FOREVER_S)
    if isinstance(raw, int | float):
        return Window(float(raw))
    for_s = FOREVER_S if raw["for_s"] == "forever" else float(raw["for_s"])
    return Window(for_s, float(raw.get("start_s", 0.0)), raw.get("every_s"))


@dataclass(frozen=True)
class Injection:
    """Everything off by default, which is the nominal mission."""

    case_id: str = ""
    route: Route | None = None
    after_waypoint: int = 0
    delay_s: float = 0.0
    observe_s: float = 0.0
    freeze_planner: Window = field(default_factory=Window)
    freeze_sensor: Window = field(default_factory=Window)
    freeze_estimator: Window = field(default_factory=Window)
    stop_publishing: Window = field(default_factory=Window)
    gate_response: bool = True
    swap_axes: bool = False
    flip_east: bool = False
    scale: float = 1.0
    yaw_rate_rad_s: float = 0.0
    position_jump_m: tuple[float, float, float] | None = None
    arm_attempt_after_s: float | None = None
    stream_before_switch_s: float | None = None

    @property
    def is_case(self) -> bool:
        return bool(self.case_id)

    def at_boundary(self, action: tuple[float, ...]) -> tuple[float, ...]:
        """The ENU action after an injected frame fault: what the node actually transmits."""
        east, north = action[0], action[1]
        if self.swap_axes:
            east, north = north, east
        if self.flip_east:
            east = -east
        return (east, north, *action[2:])


def from_case(case: dict[str, Any]) -> Injection:
    """Build the node's view of a case from the matrix."""
    fly = case.get("fly", {})
    node = case.get("node", {})
    route = None
    if "waypoints_enu_m" in fly:
        route = Route(
            case["id"],
            tuple((float(p[0]), float(p[1]), float(p[2])) for p in fly["waypoints_enu_m"]),
            float(fly.get("arrival_radius_m", 0.25)),
            float(fly.get("speed_m_s", 2.0)),
            float(fly.get("gain_per_s", 1.0)),
        )
    jump = node.get("position_jump_m")
    return Injection(
        case_id=case["id"],
        route=route,
        after_waypoint=int(fly.get("after_waypoint", 0)),
        delay_s=float(fly.get("delay_s", 0.0)),
        observe_s=float(case.get("observe_s", 20.0)),
        freeze_planner=_window(node.get("freeze_planner")),
        freeze_sensor=_window(node.get("freeze_sensor")),
        freeze_estimator=_window(node.get("freeze_estimator")),
        stop_publishing=_window(node.get("stop_publishing")),
        gate_response=bool(node.get("gate_response", True)),
        swap_axes=bool(node.get("swap_axes", False)),
        flip_east=bool(node.get("flip_east", False)),
        arm_attempt_after_s=node.get("arm_attempt_after_s"),
        stream_before_switch_s=node.get("stream_before_switch_s"),
        scale=float(node.get("scale", 1.0)),
        yaw_rate_rad_s=float(node.get("yaw_rate_rad_s", 0.0)),
        position_jump_m=(float(jump[0]), float(jump[1]), float(jump[2])) if jump else None,
    )


def load_case(matrix: Path, case_id: str) -> dict[str, Any]:
    cases = json.loads(matrix.read_text(encoding="utf-8"))["cases"]
    for case in cases:
        if case["id"] == case_id:
            return dict(case)
    raise KeyError(f"no case {case_id} in {matrix}")
