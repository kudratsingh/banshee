"""Which simulator stack a host-side run uses: Jazzy (the D1 record) or Humble (WO-025).

``BANSHEE_STACK`` selects it, and is ``jazzy`` when unset, so existing runs are unchanged.
Each stack has its own VM and its own lock, so the Jazzy VM stays as the record.
"""

from __future__ import annotations

import os
from pathlib import Path

STACKS = {
    "jazzy": ("banshee-sitl", "config/stack-lock.resolved.json"),
    "humble": ("banshee-sitl-humble", "config/stack-lock.humble.resolved.json"),
}


def current() -> str:
    name = os.environ.get("BANSHEE_STACK", "jazzy")
    if name not in STACKS:
        raise SystemExit(f"BANSHEE_STACK must be one of {sorted(STACKS)}, not {name!r}")
    return name


def vm_name() -> str:
    return STACKS[current()][0]


def resolved_lock(repo: Path) -> Path:
    return repo / STACKS[current()][1]
