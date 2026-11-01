"""Frame conversion at the PX4 boundary (ADR-0005). Internal: ENU world, FLU body. PX4: NED, FRD.

All functions are pure. Positions in m, velocities in m/s, angles in rad, yaw rates in rad/s.
"""

from __future__ import annotations

import math

Vec3 = tuple[float, float, float]


def ned_to_enu(v: Vec3) -> Vec3:
    """A position or velocity vector from NED to ENU: east, north, up."""
    return (v[1], v[0], -v[2])


def enu_to_ned(v: Vec3) -> Vec3:
    """A position or velocity vector from ENU to NED: north, east, down."""
    return (v[1], v[0], -v[2])


def yaw_ned_from_quaternion(w: float, x: float, y: float, z: float) -> float:
    """Yaw of a body-FRD-to-NED quaternion: heading from north, positive clockwise from above."""
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


def yaw_enu_from_ned(yaw_ned: float) -> float:
    """NED heading to ENU yaw, from east and positive counter-clockwise, in (-pi, pi]."""
    return math.atan2(math.cos(yaw_ned), math.sin(yaw_ned))


def yaw_rate_flu_to_frd(rate_flu: float) -> float:
    """A yaw rate about FLU up to a yaw rate about FRD down."""
    return -rate_flu
