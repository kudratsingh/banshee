"""The split rule: each family goes wholly to train or to held-out, decided by a salted hash.

Deterministic and frozen: the same families and salt always give the same split. Held-out must
contain at least ``min_variation`` nominal families from the variation set and ``min_fault`` fault
families; if the hash alone gives fewer, the lowest-scoring ones of that kind are moved in.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable

from .families import NOMINAL, Family

TRAIN = "train"
HELDOUT = "heldout"
# The contract's partitions are train, dev, sealed and regression. Held-out here is "dev": "sealed"
# needs storage outside the agent's reach (docs/DATA_POLICY.md section 5), and this agent made it.
PARTITION = {TRAIN: "train", HELDOUT: "dev"}


def score(family: Family, salt: str) -> float:
    digest = hashlib.sha256(f"{salt}|{family.id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def assign(
    families: Iterable[Family],
    variation: Iterable[Family],
    *,
    salt: str,
    heldout_fraction: float,
    min_variation: int,
    min_fault: int,
) -> dict[str, str]:
    """Family id -> "train" or "heldout"."""
    every = sorted(set(families) | set(variation))
    variation_ids = {f.id for f in variation}
    held = {f.id for f in every if score(f, salt) < heldout_fraction}
    for wanted, pool in (
        (min_variation, [f for f in every if f.id in variation_ids]),
        (min_fault, [f for f in every if f.fault_family != NOMINAL]),
    ):
        ranked = sorted(pool, key=lambda f: score(f, salt))
        if len(ranked) < wanted:
            raise ValueError("not enough families to meet the held-out minimum")
        for family in ranked:
            if sum(f.id in held for f in pool) >= wanted:
                break
            held.add(family.id)
    return {f.id: (HELDOUT if f.id in held else TRAIN) for f in every}
