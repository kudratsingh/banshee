"""Run fault cases from the host: one run directory, one fresh bounded VM run, one analysis each.

Every case is executed and logged, and a deviation is a result, not an error. Simulation only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ironclad.core.runs import finish_run, new_run_dir

from ..sitl.bounded import COMPLETED, free_space_problems, run_bounded, vm_free_bytes
from .analyze import analyze_dir

VM = "banshee-sitl"
MIN_FREE_BYTES = 20_000_000_000


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
    lock = json.loads((repo / "config/stack-lock.resolved.json").read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        if wanted and case["id"] not in wanted:
            continue
        record = run_case(repo, args.matrix, case, lock)
        brief = {
            k: record.get(k) for k in ("case", "run_id", "executed", "deviations", "vm_returncode")
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
