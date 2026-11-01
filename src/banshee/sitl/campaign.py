"""Run nominal missions from the host: one run directory, one bounded VM run, one judged episode.

Each run gets a new directory and ledger lines, a fresh simulator in the VM, a bounded log, and an
independent outcome. ``export_root`` receives one contract episode per run. A failed run stays in
the record. Simulation only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path

from ironclad.core.runs import finish_run, new_run_dir

from ..export.episode import export_run
from ..outcome.waypoints import judge, read_steps, tolerance_from_evals
from .bounded import COMPLETED, free_space_problems, run_bounded, vm_free_bytes

VM = "banshee-sitl"
MIN_FREE_BYTES = 20_000_000_000


def run_once(repo: Path, abs_repo: Path, export_root: Path) -> dict[str, object]:
    """One mission. Returns its summary; a failed mission is a result, not an exception."""
    route = json.loads((repo / "evals/D1-route.json").read_text(encoding="utf-8"))
    evals = json.loads((repo / "evals/D1-exit-tests.json").read_text(encoding="utf-8"))
    lock = json.loads((repo / "config/stack-lock.resolved.json").read_text(encoding="utf-8"))
    run_dir = new_run_dir(
        repo,
        purpose="d1_nominal_mission",
        config={"route": route, "sim_limits": evals["sim_limits"]},
        seeds={},
        env_lock=lock,
    )
    run_id = run_dir.name
    vm_out = f"/tmp/banshee-runs/{run_id}"  # noqa: S108 - inside the VM
    result = run_bounded(
        [
            "limactl", "shell", VM, "--", "bash",
            str(abs_repo / "src/banshee/sitl/vm/run_mission.sh"), str(abs_repo), vm_out,
        ],
        run_dir / "vm.log",
        max_log_bytes=5_000_000,
        timeout_s=300,
    )  # fmt: skip
    subprocess.run(
        ["limactl", "copy", "-r", f"{VM}:{vm_out}", str(run_dir / "tmp")],
        check=False,
        capture_output=True,
        timeout=120,
    )
    copied = run_dir / "tmp" / run_id
    steps_path = copied / "steps.jsonl"
    summary: dict[str, object] = {"run_id": run_id, "vm_outcome": result.outcome}
    if not steps_path.exists():
        finish_run(repo, run_dir, status="failed", note=f"no steps logged; {result.outcome}")
        summary["success"] = False
        return summary
    steps = read_steps(steps_path)
    tolerance = tolerance_from_evals(repo / "evals/D1-exit-tests.json")
    outcome = judge(steps, route["waypoints_enu_m"], tolerance)
    stack = json.loads((copied / "versions.json").read_text(encoding="utf-8"))
    episode = export_run(
        steps,
        run_id=run_id,
        created_at=datetime.now(UTC).isoformat(),
        route=route,
        limits=evals["sim_limits"],
        outcome=outcome,
        stack=stack,
        target_dir=export_root / run_id,
        tolerance_m=tolerance,
    )
    forwards = [s for s in steps if s["transmitted"] is not None]
    gaps = [b["t_ns"] - a["t_ns"] for a, b in pairwise(steps)]
    summary.update(
        success=outcome["success"],
        waypoints=f"{outcome['waypoints_reached']}/{outcome['waypoints_total']}",
        closest_approach_m=outcome["closest_approach_m"],
        steps=len(steps),
        transmitted=len(forwards),
        max_tick_gap_ms=round(max(gaps) / 1e6, 1) if gaps else None,
        episode=str(episode),
        versions=stack,
    )
    status = "completed" if result.outcome == COMPLETED and outcome["success"] else "failed"
    finish_run(repo, run_dir, status=status, note=str(summary["waypoints"]))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, required=True)
    parser.add_argument("--export-root", type=Path, default=Path("data/derived/d1"))
    args = parser.parse_args(argv)
    repo = Path(".")
    args.export_root.mkdir(parents=True, exist_ok=True)
    problems = free_space_problems(
        {"host": _host_free(repo), f"VM {VM}": vm_free_bytes(VM)}, MIN_FREE_BYTES
    )
    if problems:
        print("refused: " + "; ".join(problems))
        return 3
    wins = 0
    for index in range(args.runs):
        summary = run_once(repo, repo.resolve(), args.export_root)
        wins += bool(summary["success"])
        print(json.dumps({"index": index, **summary}, default=str), flush=True)
    print(f"{wins}/{args.runs} succeeded")
    return 0 if wins == args.runs else 1


def _host_free(path: Path) -> int:
    import shutil

    return shutil.disk_usage(path).free


if __name__ == "__main__":
    raise SystemExit(main())
