"""Cross-check a run against simulator ground truth from its ULog. Not part of the pass decision.

The judge in ``waypoints.py`` reads the logged estimate. This reads PX4 SITL's
``vehicle_local_position_groundtruth``, which comes from Gazebo, so it also tests the frame
conversion on real motion. ``pyulog`` is not a project dependency; it goes in its own environment.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Sequence
from pathlib import Path
from typing import Any

Point = Sequence[float]


def enu_from_ned(north: float, east: float, down: float) -> tuple[float, float, float]:
    return (east, north, -down)


def closest_per_waypoint(track: Sequence[Point], waypoints: Sequence[Point]) -> list[float]:
    """The closest distance from the whole track to each waypoint (m), in any order."""
    return [min(math.dist(p, w) for p in track) for w in waypoints]


def read_truth_track(ulog_path: Path) -> list[tuple[float, float, float]]:
    from pyulog import ULog

    ulog = ULog(str(ulog_path), ["vehicle_local_position_groundtruth"])
    data = ulog.data_list[0].data
    return [
        enu_from_ned(float(n), float(e), float(d))
        for n, e, d in zip(data["x"], data["y"], data["z"], strict=True)
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ulog", type=Path, required=True)
    parser.add_argument("--route", type=Path, default=Path("evals/D1-route.json"))
    args = parser.parse_args(argv)
    waypoints = json.loads(args.route.read_text(encoding="utf-8"))["waypoints_enu_m"]
    track = read_truth_track(args.ulog)
    result: dict[str, Any] = {
        "closest_approach_m": [round(c, 3) for c in closest_per_waypoint(track, waypoints)],
        "start_enu_m": [round(v, 2) for v in track[0]],
        "end_enu_m": [round(v, 2) for v in track[-1]],
        "max_up_m": round(max(p[2] for p in track), 2),
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
