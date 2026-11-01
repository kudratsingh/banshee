# ADR-0008 — Adopt ironclad v1.1.0

**Date:** 2026-10-31 · **Status:** accepted · **Work order:** WO-013 · **Program link:** PROGRAM §5.5; ADR-0004

## Context
ADR-0004 makes shared material a versioned dependency, `ironclad`. The release notes in that repository ask each project to adopt it in a work order of its own and to record the adoption in an ADR.

## Decision
- **Pin:** `ironclad-kit @ git+https://github.com/kudratsingh/ironclad@v1.1.0`, as the owner specified. The package is never installed by name, because `ironclad` on PyPI is an unrelated project.
- **CI credential:** the read-only deploy key the owner created, as the secret `IRONCLAD_DEPLOY_KEY`. It is loaded by a step in our own workflow, with GitHub's published host key, so the secret goes to no third-party action.
- **Removed:** `contracts/`, `tools/`, `src/banshee/core/`, the four shared test files and the two old locks. Git history keeps them.
- **Also removed:** the root `SHA256SUMS.json`. The release notes do not list it. The tool that wrote it is gone, and nothing would keep it current or check it, so it would become a stale record. `ironclad verify` now does the work of the old hash checks.
- **Kept:** `src/banshee/freshness.py`, `src/banshee/interfaces.py` and `tests/test_freshness.py`, which are this project's.

Old paths that stay in frozen or policy text mean the following:

| Old path | Now |
|---|---|
| `contracts/v1/validate.py` | `ironclad-validate`, or `ironclad.contracts.v1.validate` |
| `contracts/v1/audit_splits.py` | `ironclad-audit-splits` |
| `contracts/v1/writer.py` | `ironclad.contracts.v1.writer` |
| `tools/status_board.py` | `ironclad-status` |
| `tools/check_immutable.py` | `ironclad-check-immutable` |
| `tools/scan_secrets.py` | `ironclad-scan-secrets` |
| `tools/budget_preflight.py` | `ironclad-budget-preflight` |
| `src/*/core/` | `ironclad.core` |

These remain in `AGENTS.md §13.8` and in the frozen ET-D1-3 and its threshold in `evals/D1-exit-tests.json`. This repository authors no policy text, and a frozen exit test is not edited.

## Alternatives considered
| Option | Why not |
|---|---|
| `webfactory/ssh-agent`, the release notes' example | it would hand the secret to a third-party action; the notes allow a step of our own |
| Pin by full commit | the owner specified the tag. `verify` accepts both. A tag can move, and the installed commit, `d5b91b6`, is on record here |
| Keep `SHA256SUMS.json` as history | git already keeps it, and a stale manifest in the tree reads as current |

## Consequences
- CI now depends on the deploy key and on `ironclad`'s availability.
- Shared fixes reach this repository only by moving the pin.
- The shared tests run through the plugin, against this repository.
- `docs/WORKFLOW.md §8` now describes a `cpu-tier` gate job. This repository's protection still requires `cpu-tier (3.12)` and `cpu-tier (3.13)`, which also works, so nothing changes here.

## Reversibility
A new pull request can restore the removed paths from the commit before this change, keeping every ledger and report line.
