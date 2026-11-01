# WO-013 | Adopt ironclad v1.1.0 and remove the vendored shared files
**Phase:** D1
**Exit tests advanced:** none; this is program housekeeping.
**Size:** M
**Prerequisites:** `ironclad` `v1.1.0` tagged; `IRONCLAD_DEPLOY_KEY` set by the owner in this repository (`ledgers/approvals.jsonl`).
**Authorization:** AGENTS §2.1, on the owner's instruction of 2026-10-31. The owner created the deploy key. No full review is needed: CI is enough, on the owner's instruction.
**Files:** `contracts/`, `tools/`, `src/banshee/core/`, `src/banshee/__init__.py`, `src/banshee/interfaces.py`, `tests/`, `config/contract-lock.json`, `config/program-lock.json`, `SHA256SUMS.json`, `pyproject.toml`, `requirements-dev.txt`, `Makefile`, `.github/workflows/ci.yml`, `.gitignore`, `.pre-commit-config.yaml`, the policy copies `ironclad sync-policy` writes, `CLAUDE.md`, `README.md`, `REQUIREMENTS_CHECKLIST.md`, `CHANGES.md`, `data/README.md`, `docs/ARCHITECTURE.md`, `docs/TEST_PROTOCOL.md`, `docs/adr/ADR-0008-adopt-ironclad.md`, `docs/STATUS_BOARD.md`, `work_orders/`, `ledgers/approvals.jsonl`, `reports/`.

Serves `PROGRAM §5.5`. This follows `docs/releases/v1.0.0.md` and `v1.1.0.md` in `kudratsingh/ironclad`. WO-002 continues on its own branch and shares no change with this one.

## Objective
Move this repository onto the pinned `ironclad` release, so shared files have one source.

## Scope
1. Pin `ironclad-kit @ git+https://github.com/kudratsingh/ironclad@v1.1.0` in `requirements-dev.txt` and `pyproject.toml`.
2. Load the read-only deploy key in CI, in a step of our own, so the secret goes to no third-party action. The pin stays `https`.
3. Make the `Makefile` a wrapper for the installed commands.
4. Run `ironclad sync-policy --root .` and read the diff. The core must stay at policy 1.1.
5. Remove the vendored copies the release lists, and fix references in documents that are not frozen.
6. Record the adoption in ADR-0008.

## Out of scope
- Changing any policy text, program ADR or frozen exit test. `AGENTS.md §13.8` and the frozen ET-D1-3 text still name the old path; ADR-0008 gives the equivalent.
- WO-002's work, or using the launcher.
- Accepted work orders and reports, which keep their old paths.

## Verification
```bash
make check
make immutable BASE=origin/main
ironclad version
```
Expected: every command exits 0, `ironclad version` prints `1.1.0`, and the core differs from `main` by the marker line alone. The first CI run is the first real test of the deploy key.

## Exit criteria
No exit test closes here. Accepted when CI is green on the merged commit, including the `make verify` step.

## Stop conditions
`sync-policy` changes the core or `PROGRAM.md` beyond the marker line; a shared test needs weakening to pass; CI cannot install with the deploy key.

## Report
`reports/WO-013-adopt-ironclad.md`.
