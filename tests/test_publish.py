"""Families, the split rule, and the export's order: manifest, verify, rename, COMPLETE last."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from banshee.export.episode import export_run
from banshee.outcome.waypoints import judge
from banshee.publish.export import publish, sha256, verify
from banshee.publish.families import NOMINAL, Family, fault_family, route_id, wind_id
from banshee.publish.splits import HELDOUT, TRAIN, assign

WAYPOINTS = [[0.0, 0.0, 5.0], [10.0, 0.0, 5.0]]


def test_family_parts() -> None:
    assert fault_family("N-01-X500-3") == NOMINAL and fault_family("H-02-4KG") == "H"
    assert fault_family("PL-2p5-LD") == "PL" and fault_family(None) == NOMINAL
    assert wind_id(None) == "calm" and wind_id("windy_2p5") == "wind-2.5"
    with pytest.raises(ValueError):
        wind_id("stormy")
    assert route_id(None) == "d1-square-v1"
    assert route_id([[0, 0, 5]]) == route_id([[0.0, 0.0, 5.0]]) != route_id([[0, 0, 6]])


def _families() -> tuple[list[Family], list[Family]]:
    faults = [Family(f"r{i}", "calm", f"F{i}") for i in range(12)]
    variation = [Family(r, w, NOMINAL) for r in ("a", "b", "c") for w in ("calm", "wind-5.0")]
    return faults, variation


def test_split_is_deterministic_and_meets_the_minimums() -> None:
    faults, variation = _families()
    kwargs: dict[str, Any] = {"heldout_fraction": 0.0, "min_variation": 2, "min_fault": 3}
    one = assign(faults, variation, salt="s", **kwargs)
    assert one == assign(list(reversed(faults)), variation, salt="s", **kwargs)
    held = {k for k, v in one.items() if v == HELDOUT}
    assert sum(f.id in held for f in variation) == 2
    assert sum(f.id in held for f in faults) == 3
    assert set(one.values()) == {TRAIN, HELDOUT}


def test_a_minimum_that_cannot_be_met_is_refused() -> None:
    faults, variation = _families()
    with pytest.raises(ValueError):
        assign(faults, variation, salt="s", heldout_fraction=0.0, min_variation=7, min_fault=0)


def _step(position: list[float], t: int) -> dict[str, Any]:
    return {
        "t_ns": 1000 + t * 50,
        "phase": "route",
        "position_enu_m": position,
        "velocity_enu_m_s": [0.0, 0.0, 0.0],
        "yaw_enu_rad": 0.0,
        "capture_t_ns": 900 + t * 50,
        "received_t_ns": 950 + t * 50,
        "estimator_valid": True,
        "arming_state": 2,
        "requested": [0.0, 0.0, 0.0, 0.0],
        "filtered": [0.0, 0.0, 0.0, 0.0],
        "transmitted": [0.0, 0.0, 0.0, 0.0],
        "sent_t_ns": 1001 + t * 50,
        "valid_until_t_ns": 2000 + t * 50,
    }


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    steps = [_step([0.0, 0.0, 5.0], 0), _step([10.0, 0.0, 5.0], 1), _step([10.0, 0.0, 0.0], 2)]
    for run_id in ("run-a", "run-b"):
        export_run(
            steps,
            run_id=run_id,
            created_at="2026-11-06T00:00:00+00:00",
            route={"route_id": "d1-square-v1", "waypoints_enu_m": WAYPOINTS},
            limits={
                "max_horizontal_speed_m_s": 2.5,
                "max_climb_m_s": 1.0,
                "max_commanded_descent_m_s": 0.5,
            },
            outcome=judge(steps, WAYPOINTS, 0.5),
            stack={"os": "Ubuntu 24.04.5 LTS", "px4": "fixture"},
            target_dir=repo / "data/derived/d1" / run_id,
            tolerance_m=0.5,
        )
        run = repo / "runs" / run_id
        (run / "tmp" / run_id / "ulog").mkdir(parents=True)
        (run / "tmp" / run_id / "ulog" / "log.ulg").write_bytes(run_id.encode())
        (run / "config.snapshot.json").write_text(json.dumps({"world": "default"}))
    plan = {"families": [{"family_id": "d1-square-v1|calm|nominal", "split": HELDOUT}]}
    (repo / "evals").mkdir()
    (repo / "evals/D1-split-plan.json").write_text(json.dumps(plan))
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
         "--allow-empty", "-m", "fixture"],
        check=True,
    )  # fmt: skip
    return repo


def test_an_export_is_complete_verified_relabelled_and_read_only(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    final = publish(repo, "d1", "episodes", "2026-11-06T00:00:00+00:00")
    manifest = json.loads((final / "MANIFEST.json").read_text())
    assert (final / "COMPLETE").read_text().strip() == sha256(final / "MANIFEST.json")
    verify(final)
    assert manifest["contract"]["schema_version"] == "1.0.0"
    assert manifest["counts"]["by_stack_and_split"] == {"jazzy/heldout": 2}
    episode = json.loads((final / "episodes/run-a/episode.json").read_text())
    assert episode["split"]["partition"] == "dev"
    assert episode["split"]["scene_group_id"] == "d1-square-v1|calm|nominal"
    assert not (final / "MANIFEST.json").stat().st_mode & 0o222
    assert not list((repo / "data/exports").glob(".tmp-*"))
    with pytest.raises(FileExistsError):
        publish(repo, "d1", "episodes", "2026-11-06T00:00:00+00:00")


def test_a_ulog_export_lists_each_file_with_its_hash(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    final = publish(repo, "d1", "ulogs", "2026-11-06T00:00:00+00:00")
    rows = json.loads((final / "MANIFEST.json").read_text())["entries"]
    assert [r["run_id"] for r in rows] == ["run-a", "run-b"]
    assert rows[0]["ulogs"][0]["sha256"] == sha256(final / "ulogs/run-a/log.ulg")


def test_a_family_missing_from_the_plan_is_refused(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / "evals/D1-split-plan.json").write_text(json.dumps({"families": []}))
    with pytest.raises(ValueError):
        publish(repo, "d1", "episodes", "2026-11-06T00:00:00+00:00")
    assert not list((repo / "data/exports").glob("*"))
