"""Decide from logged state alone whether a route was flown. Imports nothing from the planner.

A waypoint counts as reached if a logged, estimator-valid position while armed lies within the
frozen tolerance, in route order. The mission completes if every waypoint is reached and the
aircraft ends disarmed. Positions in ENU m. This judges PX4's state estimate; a simulator ground
truth is not in the log, and the report says so.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ARMED = 2


def tolerance_from_evals(path: Path) -> float:
    """The frozen waypoint tolerance (m), read from the ET-D1-2 threshold text."""
    threshold = json.loads(path.read_text(encoding="utf-8"))["exit_tests"]["ET-D1-2"]["threshold"]
    match = re.search(r"within ([0-9.]+) m", threshold)
    if match is None:
        raise ValueError(f"no tolerance in ET-D1-2 threshold: {threshold!r}")
    return float(match.group(1))


def judge(
    steps: Iterable[dict[str, Any]], waypoints: list[list[float]], tolerance_m: float
) -> dict[str, Any]:
    """Return the outcome and, per waypoint, the closest approach while it was the next one."""
    index = 0
    inside = False
    closest = [math.inf for _ in waypoints]
    was_armed = False
    last_arming: int | None = None
    count = 0
    for step in steps:
        count += 1
        last_arming = step["arming_state"]
        if last_arming == ARMED:
            was_armed = True
        if last_arming != ARMED or not step["estimator_valid"] or index >= len(waypoints):
            continue
        position = step["position_enu_m"]
        # A waypoint stays current until the aircraft leaves its tolerance, so the closest approach
        # is the real one and not the first sample inside the tolerance.
        if inside and math.dist(position, waypoints[index]) > tolerance_m:
            index += 1
            inside = False
            if index >= len(waypoints):
                continue
        gap = math.dist(position, waypoints[index])
        closest[index] = min(closest[index], gap)
        inside = inside or gap <= tolerance_m
    reached_count = index + int(inside)
    reached = reached_count == len(waypoints)
    landed = was_armed and last_arming is not None and last_arming != ARMED
    return {
        "method": "logged state only; estimator-valid positions while armed, in route order",
        "tolerance_m": tolerance_m,
        "steps": count,
        "waypoints_total": len(waypoints),
        "waypoints_reached": reached_count,
        "closest_approach_m": [None if math.isinf(c) else round(c, 4) for c in closest],
        "landed_disarmed": landed,
        "success": reached and landed,
    }


def read_steps(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--route", type=Path, default=Path("evals/D1-route.json"))
    parser.add_argument("--tolerance-file", type=Path, required=True)
    args = parser.parse_args(argv)
    route = json.loads(args.route.read_text(encoding="utf-8"))
    result = judge(
        read_steps(args.run / "steps.jsonl"),
        route["waypoints_enu_m"],
        tolerance_from_evals(args.tolerance_file),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
