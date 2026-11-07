"""Which family an episode belongs to: route x wind x fault family.

A family is the unit of the split, so that one route, wind and fault family never spans two
partitions, across both stacks, both airframes and both exports.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

NOMINAL = "nominal"
DEFAULT_ROUTE_ID = "d1-square-v1"
# Gazebo world name -> wind id. "default" has no wind; "windy" is PX4's, at (5, 2) m/s.
WIND_IDS = {
    "default": "calm",
    "windy": "wind-5.4",
    "windy_5": "wind-5.0",
    "windy_4": "wind-4.0",
    "windy_3": "wind-3.0",
    "windy_2p5": "wind-2.5",
}


@dataclass(frozen=True, order=True)
class Family:
    route_id: str
    wind_id: str
    fault_family: str

    @property
    def id(self) -> str:
        return f"{self.route_id}|{self.wind_id}|{self.fault_family}"


def wind_id(world: str | None) -> str:
    """The wind id for a Gazebo world; an unknown world is refused, not guessed."""
    name = world or "default"
    if name not in WIND_IDS:
        raise ValueError(f"unknown world {name!r}")
    return WIND_IDS[name]


def route_id(waypoints: list[list[float]] | None) -> str:
    """A case's own waypoints name its route by their hash; no waypoints means the D1 route."""
    if not waypoints:
        return DEFAULT_ROUTE_ID
    canonical = json.dumps([[float(v) for v in point] for point in waypoints])
    return "wp-" + hashlib.sha256(canonical.encode()).hexdigest()[:10]


def fault_family(case_id: str | None) -> str:
    """N-01 and its controls are nominal; otherwise the letters before the first dash."""
    if not case_id or case_id.startswith("N-"):
        return NOMINAL
    return case_id.split("-")[0]


@dataclass(frozen=True)
class Described:
    episode_id: str
    run_id: str
    family: Family
    case_id: str | None
    stack: str
    airframe: str
    suite_id: str
    success: bool
    schema_version: str


def stack_name(stack: dict[str, Any]) -> str:
    os_name = str(stack.get("os", ""))
    if "22.04" in os_name:
        return "humble"
    if "24.04" in os_name:
        return "jazzy"
    raise ValueError(f"unknown stack {os_name!r}")


def describe(episode_dir: Path, runs_root: Path) -> Described:
    """Read an episode and its run record; anything missing is an error, never a guess."""
    episode = json.loads((episode_dir / "episode.json").read_text(encoding="utf-8"))
    config = json.loads((episode_dir / "configuration.json").read_text(encoding="utf-8"))
    run_id = episode_dir.name
    suite = episode["split"]["suite_id"]
    case_id: str | None = None
    if suite == "d1-faults":
        case_path = runs_root / run_id / "tmp" / run_id / "case.json"
        case = json.loads(case_path.read_text(encoding="utf-8"))
        case_id = case["id"]
        family = Family(
            route_id((case.get("fly") or {}).get("waypoints_enu_m")),
            wind_id((case.get("env") or {}).get("PX4_GZ_WORLD")),
            fault_family(case_id),
        )
    else:
        snapshot = json.loads((runs_root / run_id / "config.snapshot.json").read_text("utf-8"))
        family = Family(episode["task"]["id"], wind_id(snapshot.get("world")), NOMINAL)
    return Described(
        episode_id=episode["episode_id"],
        run_id=run_id,
        family=family,
        case_id=case_id,
        stack=stack_name(config["stack"]),
        airframe=config.get("airframe", "gz_x500"),
        suite_id=suite,
        success=bool(episode["outcome"].get("success")),
        schema_version=episode["schema_version"],
    )
