"""Export a mission run through ``ironclad.contracts.v1.writer``: one run, one write-once episode.

The state stream is position (m), velocity (m/s) and yaw (rad), in the ENU local frame. Actions are
ENU velocity with FLU yaw rate. Times are monotonic ns in the VM; capture times are mapped from
PX4's clock by the smallest offset seen (ADR-0005). Applied actions are not known, so they are null.
"""

from __future__ import annotations

import json
from itertools import pairwise
from pathlib import Path
from typing import Any

from ironclad.contracts.v1.writer import EpisodeBuilder

FRAME = "enu_local"
STATE_UNITS = ["m", "m", "m", "m/s", "m/s", "m/s", "rad"]
NOMINAL_NOTES = (
    "PX4 SITL with Gazebo. A simulation pass is not flight readiness. Success needs the route "
    "judged from PX4's estimate and Gazebo ground truth, and a clean run."
)


def _observation(step: dict[str, Any]) -> dict[str, Any]:
    valid = bool(step["estimator_valid"])
    value = [*step["position_enu_m"], *step["velocity_enu_m_s"], step["yaw_enu_rad"]]
    return {
        "stream": "state",
        "capture_t_ns": step["capture_t_ns"],
        "received_t_ns": step["received_t_ns"],
        "valid": valid,
        "value": value if valid else None,
        "artifact": None,
    }


def _record(
    episode_id: str, index: int, step: dict[str, Any], after: dict[str, Any]
) -> dict[str, Any]:
    transmitted = step["transmitted"]
    return {
        "schema_version": "1.0.0",
        "episode_id": episode_id,
        "step": index,
        "t_ns": step["t_ns"],
        "dt_ns": after["t_ns"] - step["t_ns"],
        "observations": [_observation(step)],
        "next_observations": [_observation(after)],
        "action": {
            "requested": step["requested"],
            "filtered": step["filtered"],
            "transmitted": transmitted,
            "applied": None,
            "decision_t_ns": step["t_ns"],
            "sent_t_ns": step["sent_t_ns"] if transmitted is not None else None,
            "applied_t_ns": None,
            "valid_until_t_ns": step["valid_until_t_ns"],
        },
        "context": {
            "mode": step["phase"],
            "estimator_valid": step["estimator_valid"],
            "intervention": None,
        },
    }


def _usable(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Steps whose observation arrived by decision time, with strictly increasing times."""
    usable: list[dict[str, Any]] = []
    for step in steps:
        if step["received_t_ns"] > step["t_ns"] or step["capture_t_ns"] > step["received_t_ns"]:
            continue
        if usable and step["t_ns"] <= usable[-1]["t_ns"]:
            continue
        usable.append(step)
    return usable


def export_run(
    steps: list[dict[str, Any]],
    *,
    run_id: str,
    created_at: str,
    route: dict[str, Any],
    limits: dict[str, Any],
    outcome: dict[str, Any],
    stack: dict[str, Any],
    target_dir: Path,
    tolerance_m: float,
    suite_id: str = "d1-nominal",
    instruction: str = "Take off, fly the route by offboard velocity, land.",
    reason: str | None = None,
    protocol_version: str = "evals/D1-exit-tests.json",
    notes: str = NOMINAL_NOTES,
) -> Path:
    """Build and validate one episode directory at ``target_dir``, which must not exist."""
    episode_id = f"banshee-d1-{run_id}"
    usable = _usable(steps)
    if len(usable) < 2:
        raise ValueError("a run needs at least two usable steps to export")
    speed = limits["max_horizontal_speed_m_s"]
    configuration = json.dumps({"airframe": "gz_x500", "stack": stack}, sort_keys=True).encode()
    builder = EpisodeBuilder(
        {
            "schema_version": "1.0.0",
            "episode_id": episode_id,
            "producer": "banshee",
            "created_at": created_at,
            "environment_kind": "physics_sim",
            "purpose": "evaluation",
            "task": {
                "id": route["route_id"],
                "version": "1",
                "instruction": instruction,
                "criteria_artifact": {"path": "rubric.json", "sha256": ""},
            },
            "configuration": {
                "embodiment_id": "gz_x500",
                "embodiment_artifact": {"path": "configuration.json", "sha256": ""},
                "controller_artifact": {"path": "configuration.json", "sha256": ""},
                "calibration_artifact": {"path": "configuration.json", "sha256": ""},
                "preprocessing_artifact": {"path": "configuration.json", "sha256": ""},
                "stack_artifact": {"path": "configuration.json", "sha256": ""},
            },
            "policy": {
                "origin": "scripted",
                "checkpoint_id": None,
                "training_run_id": None,
                "family_id": None,
                "weights_artifact": None,
                "config_artifact": None,
            },
            "provenance": {
                "parent_episode_ids": [],
                "source_episode_artifacts": [],
                "generator_model_artifact": None,
            },
            "split": {
                "partition": "dev",
                "suite_id": suite_id,
                "scene_group_id": route["route_id"],
                "session_group_id": run_id,
                "policy_run_group_id": None,
                "inherited_from_parent": False,
            },
            "timebase": {
                "unit": "nanoseconds",
                "clock_domain": "vm_monotonic",
                "alignment_artifact": {"path": "alignment.json", "sha256": ""},
            },
            "frames": [FRAME],
            "streams": [
                {
                    "name": "state",
                    "kind": "state",
                    "frame_id": FRAME,
                    "units": STATE_UNITS,
                    "shape": [7],
                    "dtype": "float64",
                    "role": "input",
                }
            ],
            "action_spec": {
                "representation": "world_velocity_yaw_rate",
                "labels": ["ve", "vn", "vu", "yaw_rate"],
                "units": ["m/s", "m/s", "m/s", "rad/s"],
                "frame_id": FRAME,
                "semantics": "Offboard velocity setpoint with expiry; simulation limits only.",
                "lower": [-speed, -speed, -limits["max_commanded_descent_m_s"], -0.5],
                "upper": [speed, speed, limits["max_climb_m_s"], 0.5],
            },
            "simulator": {
                "engine": "px4_sitl_gazebo",
                "version": str(stack.get("gz_sim", "unknown")),
                "initial_state_artifact": {"path": "initial-state.json", "sha256": ""},
                "asset_manifest_artifact": {"path": "assets.json", "sha256": ""},
                "restore_mode": "initial_state_only",
            },
            "validation": {"statuses": [], "evidence": []},
            "outcome": {
                "protocol_version": protocol_version,
                "rubric_version": "1",
                "assessment_method": "independent_sim_state",
                "success": outcome["success"],
                "terminated": bool(outcome["landed_disarmed"]),
                "truncated": not outcome["landed_disarmed"],
                "reason": reason
                or f"{outcome['waypoints_reached']}/{outcome['waypoints_total']} waypoints",
                "final_assessment_artifact": {"path": "outcome.json", "sha256": ""},
                "training_reward_artifact": None,
                "paired_trial_id": None,
                "reviewer_ids": [],
            },
            "notes": notes,
        }
    )
    rubric = {"route": route, "tolerance_m": tolerance_m}
    alignment = {"method": "PX4 sample time plus the smallest offset to VM receipt seen in the run"}
    initial = {"position_enu_m": usable[0]["position_enu_m"], "world": "default"}
    for name, payload in (
        ("rubric.json", json.dumps(rubric, sort_keys=True).encode()),
        ("configuration.json", configuration),
        ("alignment.json", json.dumps(alignment).encode()),
        ("initial-state.json", json.dumps(initial).encode()),
        ("assets.json", json.dumps({"model": "gz_x500", "px4": stack.get("px4")}).encode()),
        ("outcome.json", json.dumps(outcome, sort_keys=True).encode()),
    ):
        builder.add_file(name, payload)
    for index, (step, after) in enumerate(pairwise(usable)):
        builder.add_record(_record(episode_id, index, step, after))
    return builder.write(target_dir)
