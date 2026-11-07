"""Publish episodes, or their raw ULogs, as one completed, immutable export.

Order (docs/DATA_POLICY.md section 4): build in a temporary directory inside the export root, hash
every file into MANIFEST.json, verify the hashes, rename into place, verify again, write COMPLETE
last, then make the export read-only. A published episode is the original with its split block
relabelled from the frozen plan; it is validated against the contract after relabelling.

    python -m banshee.publish.export --set d1 --kind episodes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ironclad.contracts.v1.validate import validate_episode

from .families import Described, describe
from .splits import PARTITION

EXPORT_ROOT = Path("data/exports")
PLAN = Path("evals/D1-split-plan.json")
RIGHTS = "Owner-private. All rights reserved. For use within the owner's projects only."
SETS = {
    "d1": {"glob": "data/derived/d1*/*/", "id": "banshee-d1-sim"},
    "variation": {"glob": "data/derived/variation-d1-v1/*/", "id": "banshee-d1-variation-v1"},
}
TRANSFORMATION = {
    "name": "banshee.publish.export",
    "version": "1",
    "change": "episode.json split block: partition, and scene_group_id set to the family id, "
    "from the frozen plan; every other byte unchanged",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def clone(source: Path, target: Path) -> None:
    """Copy one file as an APFS clone where possible, so a large ULog costs no extra space."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if subprocess.run(["cp", "-c", str(source), str(target)], check=False).returncode != 0:
        shutil.copy2(source, target)


def file_table(root: Path) -> list[dict[str, Any]]:
    return [
        {"path": p.relative_to(root).as_posix(), "sha256": sha256(p), "bytes": p.stat().st_size}
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name not in ("MANIFEST.json", "COMPLETE")
    ]


def verify(root: Path) -> None:
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    listed = {f["path"]: f["sha256"] for f in manifest["files"]}
    found = {f["path"]: f["sha256"] for f in file_table(root)}
    if listed != found:
        missing = sorted(set(listed) ^ set(found))[:5]
        changed = sorted(p for p in listed if p in found and listed[p] != found[p])[:5]
        raise RuntimeError(f"hash check failed: missing or extra {missing}, changed {changed}")


def make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        mode = path.stat().st_mode
        path.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    root.chmod(root.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def relabel(episode_dir: Path, target: Path, split: str, family_id: str) -> str:
    """Clone an episode and relabel its split. Returns the source episode.json's sha256."""
    for source in sorted(episode_dir.iterdir()):
        clone(source, target / source.name)
    original = episode_dir / "episode.json"
    episode = json.loads(original.read_text(encoding="utf-8"))
    episode["split"]["partition"] = PARTITION[split]
    episode["split"]["scene_group_id"] = family_id
    (target / "episode.json").unlink()
    (target / "episode.json").write_text(
        json.dumps(episode, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    validate_episode(target / "episode.json")
    return sha256(original)


def entry(d: Described, split: str) -> dict[str, Any]:
    return {
        "episode_id": d.episode_id,
        "run_id": d.run_id,
        "stack": d.stack,
        "airframe": d.airframe,
        "suite_id": d.suite_id,
        "case_id": d.case_id,
        "family_id": d.family.id,
        "route_id": d.family.route_id,
        "wind_id": d.family.wind_id,
        "fault_family": d.family.fault_family,
        "split": split,
        "partition": PARTITION[split],
        "success": d.success,
    }


def publish(repo: Path, set_name: str, kind: str, created_at: str) -> Path:
    spec = SETS[set_name]
    export_id = f"{spec['id']}-{kind}"
    root = repo / EXPORT_ROOT
    final = root / export_id
    if final.exists():
        raise FileExistsError(f"{final} exists; completed exports are immutable")
    plan_bytes = (repo / PLAN).read_bytes()
    plan = json.loads(plan_bytes)
    split_of = {row["family_id"]: row["split"] for row in plan["families"]}
    dirs = sorted(repo.glob(spec["glob"]))
    described = [describe(d, repo / "runs") for d in dirs]
    unknown = sorted({d.family.id for d in described} - set(split_of))
    if unknown:
        raise ValueError(f"families not in the frozen plan: {unknown[:5]}")
    versions = {d.schema_version for d in described}
    if len(versions) != 1:
        raise ValueError(f"mixed contract schema versions {versions}")
    root.mkdir(parents=True, exist_ok=True)
    tmp = root / f".tmp-{export_id}-{os.getpid()}"
    tmp.mkdir()
    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for directory, d in zip(dirs, described, strict=True):
        split = split_of[d.family.id]
        row = entry(d, split)
        if kind == "episodes":
            row["path"] = f"episodes/{d.run_id}"
            row["source_episode_sha256"] = relabel(
                directory, tmp / "episodes" / d.run_id, split, d.family.id
            )
            rows.append(row)
        else:
            ulogs = sorted((repo / "runs" / d.run_id / "tmp" / d.run_id / "ulog").glob("*.ulg"))
            if not ulogs:
                missing.append(d.run_id)
                continue
            row["ulogs"] = []
            for ulog in ulogs:
                rel = f"ulogs/{d.run_id}/{ulog.name}"
                clone(ulog, tmp / rel)
                row["ulogs"].append({"path": rel, "sha256": sha256(tmp / rel)})
            rows.append(row)
    if kind == "episodes":
        from ironclad.contracts.v1.audit_splits import audit

        audit(
            [tmp / r["path"] / "episode.json" for r in rows],
            ("session_group_id", "policy_run_group_id", "scene_group_id"),
        )
    by = Counter((r["stack"], r["split"]) for r in rows)
    families = {(r["split"], r["family_id"]) for r in rows}
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    manifest = {
        "export_id": export_id,
        "kind": kind,
        "producer": "banshee",
        "created_at": created_at,
        "source_commit": head,
        "contract": {"name": "ironclad contracts v1", "schema_version": versions.pop()},
        "rights": RIGHTS,
        "simulation_only": True,
        "split_plan": {"path": PLAN.as_posix(), "sha256": hashlib.sha256(plan_bytes).hexdigest()},
        "transformation": TRANSFORMATION if kind == "episodes" else None,
        "counts": {
            "entries": len(rows),
            "by_stack_and_split": {f"{s}/{p}": n for (s, p), n in sorted(by.items())},
            "families_by_split": dict(Counter(s for s, _ in families)),
            "successful": sum(r["success"] for r in rows),
            "failed": sum(not r["success"] for r in rows),
            "episodes_without_ulog": missing,
        },
        "entries": rows,
        "files": file_table(tmp),
    }
    (tmp / "MANIFEST.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    verify(tmp)
    tmp.rename(final)
    verify(final)
    (final / "COMPLETE").write_text(sha256(final / "MANIFEST.json") + "\n", encoding="utf-8")
    make_read_only(final)
    return final


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", choices=sorted(SETS), required=True)
    parser.add_argument("--kind", choices=["episodes", "ulogs"], required=True)
    args = parser.parse_args(argv)
    final = publish(Path("."), args.set, args.kind, datetime.now(UTC).isoformat())
    print(final, (final / "COMPLETE").read_text(encoding="utf-8").strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
