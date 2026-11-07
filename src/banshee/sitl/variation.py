"""Run the frozen nominal variation set: routes x winds x attempts, in the frozen order and seeds.

Resumable: an attempt already in the summary file is skipped. A failed or incomplete attempt is a
result and stays in the record. Simulation only, on the Jazzy VM, where the wind worlds are.

    python -m banshee.sitl.variation --summary runs/variation-d1-v1/attempts.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bounded import free_space_problems, vm_free_bytes
from .campaign import MIN_FREE_BYTES, VM, _host_free, run_once

PLAN = Path("evals/D1-variation-set.json")
EXPORT_ROOT = Path("data/derived/variation-d1-v1")
SUITE = "d1-variation-v1"


def done(summary: Path) -> set[int]:
    if not summary.exists():
        return set()
    return {json.loads(line)["index"] for line in summary.read_text("utf-8").splitlines() if line}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args(argv)
    repo = Path(".")
    plan = json.loads((repo / PLAN).read_text(encoding="utf-8"))
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    (repo / EXPORT_ROOT).mkdir(parents=True, exist_ok=True)
    skip = done(args.summary)
    todo = [a for a in plan["attempts"] if a["index"] not in skip][: args.limit]
    for attempt in todo:
        problems = free_space_problems(
            {"host": _host_free(repo), f"VM {VM}": vm_free_bytes(VM)}, MIN_FREE_BYTES
        )
        if problems:
            print("stopped: " + "; ".join(problems))
            return 3
        summary = run_once(
            repo,
            repo.resolve(),
            repo / EXPORT_ROOT,
            route_path=attempt["route"],
            world=attempt["world"],
            seed=attempt["seed"],
            suite_id=SUITE,
        )
        record = {**attempt, **{k: summary.get(k) for k in ("run_id", "vm_outcome", "success")}}
        record["episode"] = summary.get("episode")
        record["export_error"] = summary.get("export_error")
        with args.summary.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
        print(
            json.dumps(
                {k: record[k] for k in ("index", "route_id", "wind_id", "run_id", "success")}
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
