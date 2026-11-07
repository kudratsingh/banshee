"""Freeze the split plan: every family in the D1 episodes and the variation set, and its split.

Run once, before publishing either set: ``python -m banshee.publish.plan``. It refuses to overwrite
an existing plan.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .families import NOMINAL, Family, describe, wind_id
from .splits import PARTITION, assign, score

PLAN = Path("evals/D1-split-plan.json")
SALT = "banshee-d1-split-v1"
HELDOUT_FRACTION = 0.25
MIN_VARIATION = 2
MIN_FAULT = 2


def variation_families(variation_plan: dict[str, Any]) -> list[Family]:
    routes = [r["route_id"] for r in variation_plan["routes"]]
    winds = [w["world"] for w in variation_plan["winds"]]
    return [Family(r, wind_id(w), NOMINAL) for r in routes for w in winds]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    repo = args.repo
    if (repo / PLAN).exists():
        print(f"refused: {PLAN} exists and is frozen")
        return 1
    variation_plan = json.loads((repo / "evals/D1-variation-set.json").read_text("utf-8"))
    variation = variation_families(variation_plan)
    found = [describe(d, repo / "runs") for d in sorted((repo / "data/derived").glob("d1*/*/"))]
    families = {e.family for e in found}
    split = assign(
        families,
        variation,
        salt=SALT,
        heldout_fraction=HELDOUT_FRACTION,
        min_variation=MIN_VARIATION,
        min_fault=MIN_FAULT,
    )
    code = (repo / "src/banshee/publish/splits.py").read_bytes()
    table = [
        {
            "family_id": f.id,
            "route_id": f.route_id,
            "wind_id": f.wind_id,
            "fault_family": f.fault_family,
            "split": split[f.id],
            "partition": PARTITION[split[f.id]],
            "score": round(score(f, SALT), 6),
            "in_variation_set": f in variation,
            "d1_episodes_at_freeze": sum(e.family == f for e in found),
        }
        for f in sorted(families | set(variation))
    ]
    plan = {
        "status": "frozen 2026-11-06, before publishing either set and before the variation run",
        "authorization": "owner's work order of 2026-11-06 (ledgers/approvals.jsonl), WO-029",
        "family": "route x wind x fault family; one family is never in two partitions",
        "rule": {
            "code": "src/banshee/publish/splits.py",
            "code_sha256": hashlib.sha256(code).hexdigest(),
            "salt": SALT,
            "heldout_fraction": HELDOUT_FRACTION,
            "min_heldout_variation_families": MIN_VARIATION,
            "min_heldout_fault_families": MIN_FAULT,
        },
        "partitions": {"train": "train", "heldout": "dev, not sealed: see splits.py"},
        "families": table,
    }
    (repo / PLAN).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    held = [row for row in table if row["split"] == "heldout"]
    print(f"{len(table)} families, {len(held)} held out")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
