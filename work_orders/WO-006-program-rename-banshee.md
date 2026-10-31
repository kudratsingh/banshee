# WO-006 | Program-wide rename of this repository and package to banshee
**Phase:** D0
**Exit tests advanced:** none; this is program housekeeping ahead of WO-001.
**Size:** S
**Prerequisites:** none. Owner decision dated 2026-10-31, recorded in `ledgers/approvals.jsonl`.
**Authorization:** needs §2.3 approval for: contract semantic change (recorded in `ledgers/approvals.jsonl`). This work order does not authorize a remote, a purchase or any hardware action.
**Files:** `src/banshee/` (moved from the old package directory), `pyproject.toml`, `tests/`, `config/`, `contracts/v1/`, `PROGRAM.md`, `AGENTS.md`, `README.md`, `START_HERE.md`, `CHANGES.md`, `REQUIREMENTS_CHECKLIST.md`, `VERIFICATION.md`, `SHA256SUMS.json`, `docs/`, `prompts/`, `work_orders/`, `ledgers/approvals.jsonl`.

Serves `PROGRAM §5.1, §11, §14`.

## Objective
Apply the owner's name decision in this repository under ADR-0003, and author the shared files the `vishwaroop` repository copies byte for byte.

## Scope
- Rename the package to `banshee` and update packaging, tests, `config/phases.json`, the README, `START_HERE.md`, prompts and work orders.
- Change the contract `producer` enum and fixtures with `schema_version` kept at 1.0.0, the `PROGRAM.md` version and rows, and the shared `AGENTS.md` core (policy version 1.1, a Names paragraph and the repository names in its header), all through ADR-0003. This repository is the single source of these shared files.
- Regenerate the contract manifest, contract and program locks, and the repository manifest.

## Out of scope
- Creating or changing the `vishwaroop` repository, which has its own session and work order.
- Merging to `main` before the shared hashes are confirmed in both repositories.
- Any remote (handled in WO-007), purchase, hardware action or stage work (WO-001 onward).
- Starter-kit defects the rename did not cause (WO-008).
- Changing the contract's own name or its `urn:omni-world:...` schema ids (ADR-0003).

## Deliverables
ADR-0003 with its hash table; the renamed package; `PROGRAM.md` version 1.1; `AGENTS.md` policy version 1.1; regenerated manifests and locks; an approval record; a post-rename section in `VERIFICATION.md`.

## Steps
1. Import the starter kit on `main` and record a green baseline `make check`.
2. Apply the rename on branch `wo/WO-006-program-rename`.
3. Regenerate manifests and locks, then run the verification below.
4. Hand the shared bytes and hashes in ADR-0003 to the `vishwaroop` session. Merge once both repositories match.
5. Owner action: replace the Claude Project copy of `PROGRAM.md` with version 1.1. Agents cannot do this from the repository.

## Verification
```bash
make check
make immutable BASE=main
python tools/check_hashes.py --verify-kit-manifest
python contracts/v1/validate.py contracts/v1/examples/drone_sim/episode.json
python contracts/v1/audit_splits.py contracts/v1/examples/arm_sim/episode.json contracts/v1/examples/drone_sim/episode.json contracts/v1/examples/imagined_arm/episode.json
```
Expected: every command exits 0, and `grep -rn "omni""_drone" . --exclude-dir=.git` finds nothing. The repository `SHA256SUMS.json` was regenerated because files moved. It is a point-in-time record: `make board` and any append to `work_orders/STATUS.jsonl` invalidate it, so verify it on a clean checkout of the commit under test.

```bash
# Negative test: must exit non-zero, because the retired producer value is rejected
python -c "import json, jsonschema; e = json.load(open('contracts/v1/examples/drone_sim/episode.json')); e['producer'] = 'omni' + '_drone'; jsonschema.validate(e, json.load(open('contracts/v1/episode.schema.json')))"
# Old identifiers: every hit must be descriptive prose or listed in VERIFICATION.md
git grep -nEi 'omni[-_]?drone|world[-_]?model'
```

## Exit criteria
No exit test closes here. This WO is accepted when the checks are green on the merged commit and the `contracts/v1/SHA256SUMS.json` and `PROGRAM.md` hashes are confirmed equal in both repositories.

## Stop conditions
Any change beyond names; a shared-byte mismatch with `vishwaroop` that cannot be resolved by copying; any need for a remote, purchase or hardware action.

## Report
`VERIFICATION.md`, section "Post-rename verification". A report under `reports/` is written at acceptance, now that WO-008 has removed the test that blocked it.
