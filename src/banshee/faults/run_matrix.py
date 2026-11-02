"""Run fault cases from the host: one run directory, one fresh bounded VM run, one analysis each.

Every case is executed and logged, and a deviation is a result, not an error. Simulation only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ironclad.contracts.v1.validate import ContractError
from ironclad.core.runs import finish_run, new_run_dir

from banshee.sitl import stack as sitl_stack

from ..export.episode import export_run
from ..outcome.waypoints import read_steps
from ..sitl.bounded import COMPLETED, free_space_problems, run_bounded, vm_free_bytes
from .analyze import analyze_dir

VM = sitl_stack.vm_name()
MIN_FREE_BYTES = 20_000_000_000
EXPORT_ROOT = Path("data/derived/d1-faults")
FAULT_NOTES = (
    "PX4 SITL with Gazebo, with a fault injected. A simulation pass is not flight readiness. "
    "Success means the specified response to the fault, not a flown route; a run where the route "
    "failed can be a success. Terminated means disarmed at the end, including by a kill switch."
)


def export_case(repo: Path, copied: Path, case: dict[str, Any], record: dict[str, Any]) -> str:
    """Write the case's contract episode. Returns its path, or why there is none."""
    steps_path = copied / "steps.jsonl"
    if not steps_path.exists():
        return "not exported: no steps logged"
    evals = json.loads((repo / "evals/D1-exit-tests.json").read_text(encoding="utf-8"))
    tested = record.get("tested", {})
    deviations = record.get("deviations", [])
    landed = bool(tested.get("ever_armed")) and not tested.get("armed_at_end", True)
    fly = case.get("fly", {})
    route = {"route_id": case["id"], "waypoints_enu_m": fly.get("waypoints_enu_m", [])}
    outcome = {
        "success": bool(record.get("executed")) and not deviations,
        "landed_disarmed": landed,
        "case": case["id"],
        "checks": record.get("checks", []),
        "tested": tested,
    }
    run_id = record["run_id"]
    versions = copied / "versions.json"
    stack = json.loads(versions.read_text(encoding="utf-8")) if versions.exists() else {}
    try:
        path = export_run(
            read_steps(steps_path),
            run_id=f"{case['id']}-{run_id}",
            created_at=datetime.now(UTC).isoformat(),
            route=route,
            limits=evals["sim_limits"],
            outcome=outcome,
            stack=stack,
            target_dir=repo / EXPORT_ROOT / run_id,
            tolerance_m=0.0,
            suite_id="d1-faults",
            instruction=case["title"],
            reason=f"{case['id']}: " + ("; ".join(deviations) or "as specified"),
            protocol_version="evals/D1-fault-matrix.json",
            notes=FAULT_NOTES,
            airframe=str(case.get("env", {}).get("PX4_SIM_MODEL", "gz_x500")),
        )
    except (ContractError, ValueError, OSError) as error:
        return f"not exported: {error}"
    return str(path)


def run_case(
    repo: Path, matrix_path: Path, case: dict[str, Any], lock: dict[str, Any]
) -> dict[str, Any]:
    abs_repo = repo.resolve()
    run_dir = new_run_dir(
        repo,
        purpose="d1_fault_case",
        config={"case": case},
        seeds={},
        env_lock=lock,
    )
    vm_out = f"/tmp/banshee-runs/{run_dir.name}"  # noqa: S108 - inside the VM
    script = str(abs_repo / "src/banshee/sitl/vm/run_case.sh")
    result = run_bounded(
        [
            "limactl",
            "shell",
            VM,
            "--",
            "bash",
            script,
            str(abs_repo),
            vm_out,
            str(abs_repo / matrix_path),
            case["id"],
        ],
        run_dir / "vm.log",
        max_log_bytes=5_000_000,
        timeout_s=int(case.get("timeout_s", 120)) + 120,
    )
    subprocess.run(
        ["limactl", "copy", "-r", f"{VM}:{vm_out}", str(run_dir / "tmp")],
        check=False,
        capture_output=True,
        timeout=180,
    )
    copied = run_dir / "tmp" / run_dir.name
    record = analyze_dir(copied, case)
    record.update(run_id=run_dir.name, vm_outcome=result.outcome, vm_returncode=result.returncode)
    record["export"] = export_case(repo, copied, case, record)
    (run_dir / "analysis.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    clean = result.outcome == COMPLETED and result.returncode == 0 and record["executed"]
    finish_run(repo, run_dir, status="completed" if clean else "failed", note=case["id"])
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--only", default="")
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    if importlib.util.find_spec("pyulog") is None:
        print("refused: install the sitl extra, for pyulog")
        return 3
    repo = Path(".")
    free = {"host": shutil.disk_usage(repo).free, f"VM {VM}": vm_free_bytes(VM)}
    problems = free_space_problems(free, MIN_FREE_BYTES)
    if problems:
        print("refused: " + "; ".join(problems))
        return 3
    cases = json.loads(args.matrix.read_text(encoding="utf-8"))["cases"]
    wanted = {c for c in args.only.split(",") if c}
    lock = json.loads(sitl_stack.resolved_lock(repo).read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        if wanted and case["id"] not in wanted:
            continue
        record = run_case(repo, args.matrix, case, lock)
        brief = {
            k: record.get(k)
            for k in ("case", "run_id", "executed", "deviations", "vm_returncode", "export")
        }
        print(json.dumps(brief), flush=True)
        if args.summary is not None:
            with args.summary.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record) + "\n")
        failed += not record["executed"]
    print(f"not executed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
