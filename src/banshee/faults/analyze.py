"""What a fault case did, read from its ULog and step log, set against what was specified.

The ULog holds PX4's own mode timeline and Gazebo ground truth, so this still works if the mission
node was killed. Nothing here decides a pass: each check is a match or a deviation, and ET-D1-4 asks
for every deviation to be reported. ``pyulog`` comes from the ``sitl`` extra.
"""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from itertools import pairwise
from pathlib import Path
from typing import Any

from ..outcome.waypoints import judge, read_steps

ARMED = 2
Track = list[tuple[float, float, float, float, float]]


def read_ulog(path: Path) -> dict[str, dict[str, Any]]:
    from pyulog import ULog

    names = [
        "vehicle_status",
        "vehicle_local_position_groundtruth",
        "vehicle_local_position",
        "battery_status",
        "timesync_status",
    ]
    return {d.name: d.data for d in ULog(str(path), names).data_list}


def to_boot_us(data: dict[str, dict[str, Any]], dds_us: int) -> int:
    """A time from DDS, which the agent's time sync shifts, in the ULog's boot clock."""
    offsets = sorted(int(v) for v in data["timesync_status"]["estimated_offset"])
    return dds_us + offsets[len(offsets) // 2]


def timeline(status: dict[str, Any], t0_us: int) -> list[dict[str, Any]]:
    """Each change of PX4's mode or arming state, in seconds from the trigger."""
    changes: list[dict[str, Any]] = []
    last: tuple[int, int] | None = None
    for t, nav, arming in zip(
        status["timestamp"], status["nav_state"], status["arming_state"], strict=True
    ):
        state = (int(nav), int(arming))
        if state != last:
            changes.append(
                {"t_s": round((int(t) - t0_us) / 1e6, 3), "nav": state[0], "arming": state[1]}
            )
            last = state
    return changes


def motion(track: Track, t0_us: int, observe_s: float = math.inf) -> dict[str, Any]:
    """Travel in the observation window. ``track`` rows: t_us, east, north, up, horizontal speed."""
    end_us = t0_us + observe_s * 1e6
    after = [row for row in track if t0_us <= row[0] <= end_us]
    if not after:
        return {}
    first = after[0]
    stopped = next((row for row in after if row[4] < 0.1), None)
    return {
        "speed_at_trigger_m_s": round(first[4], 3),
        "peak_speed_after_m_s": round(max(row[4] for row in after), 3),
        "stop_time_s": round((stopped[0] - t0_us) / 1e6, 3) if stopped else None,
        "stop_distance_m": round(math.dist(first[1:3], stopped[1:3]), 3) if stopped else None,
        "horizontal_travel_m": round(max(math.dist(first[1:3], row[1:3]) for row in after), 3),
        "vertical_travel_m": round(max(abs(row[3] - first[3]) for row in after), 3),
        "end_enu_m": [round(v, 2) for v in after[-1][1:4]],
    }


def yaw_change(steps: Sequence[dict[str, Any]]) -> float | None:
    """Total unwrapped yaw change after the trigger, in rad, positive counter-clockwise."""
    yaws = [s["yaw_enu_rad"] for s in steps if s.get("since_trigger_s") is not None]
    if len(yaws) < 2:
        return None
    total = 0.0
    for a, b in pairwise(yaws):
        total += math.atan2(math.sin(b - a), math.cos(b - a))
    return total


def measure(
    data: dict[str, dict[str, Any]],
    steps: list[dict[str, Any]],
    t0_us: int | None,
    observe_s: float = math.inf,
) -> dict[str, Any]:
    """The tested behaviour of one run."""
    origin_us = t0_us if t0_us is not None else int(data["vehicle_status"]["timestamp"][0])
    truth = data["vehicle_local_position_groundtruth"]
    track: Track = [
        (float(t), float(e), float(n), -float(d), math.hypot(float(vn), float(ve)))
        for t, n, e, d, vn, ve in zip(
            truth["timestamp"], truth["x"], truth["y"], truth["z"], truth["vx"], truth["vy"],
            strict=True,
        )
    ]  # fmt: skip
    eph = data["vehicle_local_position"]["eph"]
    position = data["vehicle_local_position"]
    eph_values = (
        [float(v) for t, v in zip(position["timestamp"], eph, strict=True) if int(t) >= t0_us]
        if t0_us is not None
        else []
    )
    eph_after = round(max(eph_values), 3) if eph_values else None
    result: dict[str, Any] = {
        "triggered": t0_us is not None,
        "timeline": timeline(data["vehicle_status"], origin_us),
        "max_radius_m": round(max(math.hypot(r[1], r[2]) for r in track), 3),
        "max_up_m": round(max(r[3] for r in track), 3),
        "peak_speed_m_s": round(max(r[4] for r in track), 3),
        "eph_median_m": round(sorted(float(v) for v in eph)[len(eph) // 2], 3),
        "eph_max_m": round(max(float(v) for v in eph), 3),
        "eph_max_after_trigger_m": eph_after,
        "ever_armed": any(int(a) == ARMED for a in data["vehicle_status"]["arming_state"]),
        "yaw_change_rad": yaw_change(steps),
        "gate_modes_after_trigger": sorted(
            {s["gate_mode"] for s in steps if s.get("since_trigger_s") is not None}
        ),
        "gate_reasons_after_trigger": sorted(
            {
                r[:32]
                for s in steps
                if s.get("since_trigger_s") is not None
                for r in s["gate_reasons"]
            }
        ),
        "final_latch": steps[-1]["latch"] if steps else None,
        "transmitted_after_trigger": sum(
            1 for s in steps if s.get("since_trigger_s") is not None and s["transmitted"]
        ),
        "peak_transmitted_horizontal_m_s": round(
            max(
                (math.hypot(*s["transmitted"][:2]) for s in steps if s["transmitted"]), default=0.0
            ),
            3,
        ),
    }
    if "battery_status" in data:
        result["battery_min"] = round(min(float(v) for v in data["battery_status"]["remaining"]), 3)
    last = data["vehicle_status"]
    result["armed_at_end"] = int(last["arming_state"][-1]) == ARMED
    if t0_us is not None:
        result.update(motion(track, t0_us, observe_s))
    return result


def check(
    expect: dict[str, Any],
    tested: dict[str, Any],
    steps: list[dict[str, Any]],
    observe_s: float = math.inf,
) -> list[dict[str, Any]]:
    """Each specified item against what happened. An empty ``expect`` measures only.

    Modes are read inside the observation window, because the node's own exit ends the case.
    """
    results: list[dict[str, Any]] = []

    def add(name: str, wanted: Any, got: Any, match: bool) -> None:
        results.append({"check": name, "specified": wanted, "tested": got, "match": bool(match)})

    after = [c for c in tested["timeline"] if 0.0 <= c["t_s"] <= observe_s]
    for item in expect.get("nav", []):
        hit = next((c for c in after if c["nav"] == item["state"]), None)
        within = item["within_s"]
        add(
            f"nav {item['state']} within {within} s",
            within,
            hit["t_s"] if hit else None,
            hit is not None and hit["t_s"] <= within,
        )
    for state in expect.get("nav_never", []):
        add(
            f"never nav {state}",
            "absent",
            state in {c["nav"] for c in after},
            not any(c["nav"] == state for c in after),
        )
    if "never_armed" in expect:
        add(
            "never armed",
            expect["never_armed"],
            not tested["ever_armed"],
            tested["ever_armed"] != expect["never_armed"],
        )
    if "armed_at_end" in expect:
        add(
            "armed at end",
            expect["armed_at_end"],
            tested["armed_at_end"],
            tested["armed_at_end"] == expect["armed_at_end"],
        )
    if "gate_mode" in expect:
        modes = tested["gate_modes_after_trigger"]
        add("gate mode", expect["gate_mode"], modes, expect["gate_mode"] in modes)
    if "final_latch" in expect:
        add(
            "final latch",
            expect["final_latch"],
            tested["final_latch"],
            tested["final_latch"] == expect["final_latch"],
        )
    for key in (
        "peak_transmitted_horizontal_m_s",
        "peak_speed_m_s",
        "max_up_m",
        "max_radius_m",
        "horizontal_travel_m",
        "vertical_travel_m",
    ):
        limit = expect.get(f"max_{key}")
        if limit is not None:
            got = tested.get(key)
            add(f"{key} at most", limit, got, got is not None and got <= limit)
    if "min_max_radius_m" in expect:
        add(
            "reaches radius",
            expect["min_max_radius_m"],
            tested["max_radius_m"],
            tested["max_radius_m"] >= expect["min_max_radius_m"],
        )
    if "yaw_ccw" in expect:
        got = tested["yaw_change_rad"]
        add(
            "yaw counter-clockwise",
            expect["yaw_ccw"],
            got,
            got is not None and (got > 0) == expect["yaw_ccw"] and abs(got) > 0.2,
        )
    if "route_success" in expect:
        waypoints = expect["route_waypoints_enu_m"]
        outcome = judge(steps, waypoints, 0.5)
        reached = outcome["waypoints_reached"] == len(waypoints)
        add(
            "independent judge reaches route",
            expect["route_success"],
            reached,
            reached == expect["route_success"],
        )
    return results


def analyze_dir(run: Path, case: dict[str, Any]) -> dict[str, Any]:
    """Read one copied run folder and return the case's record."""
    ulogs = sorted((run / "ulog").glob("*.ulg"))
    steps_path = run / "steps.jsonl"
    steps = read_steps(steps_path) if steps_path.exists() else []
    trigger_path = run / "trigger.json"
    t0 = (
        json.loads(trigger_path.read_text(encoding="utf-8"))["px4_us"]
        if trigger_path.exists()
        else None
    )
    if not ulogs:
        return {"case": case["id"], "executed": False, "why": "no ULog", "deviations": ["no ULog"]}
    data = read_ulog(ulogs[-1])
    t0_boot = None if t0 is None else to_boot_us(data, t0)
    observe_s = float(case.get("observe_s", 20.0))
    tested = measure(data, steps, t0_boot, observe_s)
    results = check(case.get("expect", {}), tested, steps, observe_s)
    if case.get("needs_trigger", True) and t0 is None:
        results.append(
            {"check": "fault injected", "specified": True, "tested": False, "match": False}
        )
    return {
        "case": case["id"],
        "executed": True,
        "label": case.get("label", "measured"),
        "configured": case.get("configured", ""),
        "tested": tested,
        "checks": results,
        "deviations": [r["check"] for r in results if not r["match"]],
    }
