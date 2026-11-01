"""The version manifest and lock check (ET-D1-1). Refuses a stack that differs from the lock.

``--check-versions`` runs inside the VM, reads what is installed, compares it with
``config/stack-lock.resolved.json`` and prints the manifest. Any difference exits 1.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PINNED_KEYS = ("os", "ros2", "gazebo", "gz_sim", "px4", "agent", "px4_msgs")


def _capture(*command: str) -> str:
    out = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    return out.stdout.strip()


def read_manifest(work: Path) -> dict[str, str]:
    """What is installed in the VM, read from the tools themselves."""
    return {
        "os": _capture("lsb_release", "-ds"),
        "ros2": _capture("dpkg-query", "-W", "-f=${Version}", "ros-jazzy-ros-base"),
        "gazebo": _capture("dpkg-query", "-W", "-f=${Version}", "gz-harmonic"),
        "gz_sim": _capture("gz", "sim", "--versions").splitlines()[0],
        "px4": _capture("git", "-C", str(work / "PX4-Autopilot"), "rev-parse", "HEAD"),
        "agent": _capture("git", "-C", str(work / "Micro-XRCE-DDS-Agent"), "rev-parse", "HEAD"),
        "px4_msgs": _capture("git", "-C", str(work / "ws/src/px4_msgs"), "rev-parse", "HEAD"),
    }


def differences(manifest: dict[str, str], lock: dict[str, str]) -> list[str]:
    """One message per pinned key that is null, missing or different."""
    problems = []
    for key in PINNED_KEYS:
        if not lock.get(key):
            problems.append(f"{key}: null pin in the lock")
        elif manifest.get(key) != lock[key]:
            problems.append(f"{key}: installed {manifest.get(key)!r}, locked {lock[key]!r}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-versions", action="store_true", required=True)
    parser.add_argument("--lock", type=Path, default=Path("config/stack-lock.resolved.json"))
    parser.add_argument("--work", type=Path, default=Path(os.path.expanduser("~/sitl")))
    args = parser.parse_args(argv)
    manifest = read_manifest(args.work)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    lock = json.loads(args.lock.read_text(encoding="utf-8"))["pins"]
    problems = differences(manifest, lock)
    for problem in problems:
        print(f"refused: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
