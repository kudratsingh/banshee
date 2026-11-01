"""Go-to guidance along a declared route: a requested velocity, in ENU, from the state estimate."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from .frames import Vec3


@dataclass(frozen=True)
class Route:
    """Waypoints in the ENU local frame (m), arrival radius (m), speed (m/s) and gain (1/s)."""

    route_id: str
    waypoints: tuple[Vec3, ...]
    arrival_radius_m: float
    speed_m_s: float
    gain_per_s: float


def load_route(path: Path) -> Route:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Route(
        data["route_id"],
        tuple((float(p[0]), float(p[1]), float(p[2])) for p in data["waypoints_enu_m"]),
        float(data["arrival_radius_m"]),
        float(data["speed_m_s"]),
        float(data["gain_per_s"]),
    )


def distance(a: Vec3, b: Vec3) -> float:
    return math.dist(a, b)


def velocity_toward(position: Vec3, target: Vec3, route: Route) -> Vec3:
    """Proportional velocity toward ``target``, capped at the route speed."""
    delta = (target[0] - position[0], target[1] - position[1], target[2] - position[2])
    gain = route.gain_per_s
    velocity = (delta[0] * gain, delta[1] * gain, delta[2] * gain)
    speed = math.hypot(*velocity)
    if speed > route.speed_m_s:
        scale = route.speed_m_s / speed
        return (velocity[0] * scale, velocity[1] * scale, velocity[2] * scale)
    return velocity


class RouteFollower:
    """Tracks the current waypoint. ``step`` returns the requested velocity, or None when done."""

    def __init__(self, route: Route) -> None:
        self.route = route
        self.index = 0

    def step(self, position: Vec3) -> Vec3 | None:
        while self.index < len(self.route.waypoints):
            target = self.route.waypoints[self.index]
            if distance(position, target) > self.route.arrival_radius_m:
                return velocity_toward(position, target, self.route)
            self.index += 1
        return None
