# VERIFICATION.md — banshee (Omni Drone), imported from the omni-drone starter kit

## Post-rename verification (2026-10-31, branch `wo/WO-006-program-rename`)

**These are the current hashes.** The packaging record further down is kept as history and shows the values before the rename.

Environment: Python 3.13.5 on macOS 26.5 (Darwin 25.5.0, arm64), with the pins in `requirements-dev.txt`. The baseline `make check` on the unmodified import, also measured here, passed before any edit.

### Identity
- `contracts/v1/SHA256SUMS.json` sha256: `9c0b9347be3758b359c7c7e9fdf7eb7798086167fb1162112fcc9d22bd5a61c3` (pinned in `config/contract-lock.json`)
- `PROGRAM.md` version 1.1 sha256: `58f4c930ca08aaa2fd630826905e9ef9892968e7ceda8e2d920863f5142d02a9` (pinned in `config/program-lock.json`)
- `AGENTS.md` shared core (bytes before the `## 13.` heading) sha256: `8f174fdc05d6184675491181d91a9a8921f7678b22006378f696ec27847659b6`

### Measured
| Check | Result |
|---|---|
| `make check` (lint, types, tests, hash locks, secrets, links) | passed; 87 tests |
| `make immutable BASE=main` | passed on a scratch commit of this tree in a throwaway clone |
| `tools/check_hashes.py --verify-kit-manifest` | passed |
| `contracts/v1/validate.py` on all three fixtures | exit 0 |
| `contracts/v1/audit_splits.py` on all three fixtures | exit 0 |
| Negative test: `drone_sim` with the retired drone `producer` value | rejected, exit 2 |
| `grep -rn` for the old underscore package name, outside `.git` | no hits |

### Cross-repository check
**Real repository, measured read-only on 2026-10-31 at 09:11 UTC. Not confirmed yet.** `PROGRAM.md` and `config/program-lock.json` match. The contract manifest, `config/contract-lock.json`, ADR-0003 and the `AGENTS.md` core do not: the `vishwaroop` working tree held an earlier uncommitted draft of them (contract manifest `9c0b9347...`, `AGENTS.md` core `9b442240...`), and it has to copy the final bytes from this commit. Compare against the hash table in ADR-0003.

**Scratch copy.** All the shared files in ADR-0003 were copied into a scratch copy of `world-model-starter-kit.zip`, with a minimal package rename for that run only. `make check` passed there (82 tests) and every copied file matched this repository. This shows the bytes work in the sibling's test suite; it does not confirm the real repository.

### Remote (WO-007)
- `kudratsingh/banshee` is private, with default branch `main`, as read back from GitHub. It was created on the owner's request of 2026-10-31.
- `main` was pushed at `ef55cc4`. CI run 41187438262 passed on that commit: `cpu-tier (3.12)` and `cpu-tier (3.13)` succeeded and the manual simulator job was skipped.
- GitHub accepted protection on `main`, read back from the API: pull requests required with 0 approvals, both `cpu-tier` checks required, administrators included, force-push and deletion disallowed.
- This rename branch is committed locally and not pushed. It stays local until the owner approves the push and pull request separately. CI on this rename is **not run**.

### Old names left on purpose
- `Omni_Drone_World_Model_Starter_Kits_2026-10-30.zip` in `CHANGES.md` and `world-model-starter-kit.zip` in this file, real file names.
- `omni-drone` in this file's title and in the rename notes in `CHANGES.md`, which record where the repository came from.
- `omni-world` in `contracts/v1/RELEASE.json` and the schema `$id` URNs, the contract's own name, and in ADR-0003 and WO-006, which say it stays.
- "Omni Drone", "World Model & Planner", "world model" and "world-model" as descriptive prose, which the owner's decision keeps valid.

### Record notes
- The rename edits were applied to the uncommitted working tree at 08:53:22Z, before the approval, `ready` and `in_progress` records were appended at 08:55:03Z. `docs/WORKFLOW.md §1` puts those records first. The owner's decision itself predates the edits.
- During review, a read-only review agent appended a false `accepted` event for WO-006 to the working copy of `work_orders/STATUS.jsonl`. It was never committed. The owner chose to remove it and log it; the full line and the account are in `ledgers/corrections.jsonl`.

### Not run
No simulator and no hardware. The owner's Claude Project copy of `PROGRAM.md` has not been updated to version 1.1; only the owner can do that.

## Packaging record (before the rename)

Packaging run: 2026-10-31 07:51 UTC. Everything below was executed on the assembled kit before zipping; nothing is copied from the reference bundle's reports.

## Environment (packaging machine)

- Python 3.13.18 on Linux 6.18.44-fc-v185 (x86_64)
- jsonschema 4.26.0
- pytest 9.1.1
- ruff 0.16.9
- mypy 2.3.1
- No simulator, GPU, robotics stack, network service, hardware, or other repository was used.

## Identity

- `contracts/v1/SHA256SUMS.json` sha256: `28a2bab148bd83a32bab547ddcc1318d081e2401ce0a8c627138de64a7ec116c` (pinned in `config/contract-lock.json`; identical in both kits)
- `PROGRAM.md` sha256: `a7f0b3f1d6f8bb5bc09ee00f44c7f657a3040a3453909f83b602379cfbfbe483` (pinned in `config/program-lock.json`; identical in both kits)
- `AGENTS.md` shared core (sections 1–12, before the project addendum) sha256: `11c7b92e9793342bd17d4ced447dbe3376d01e39b17b5d35ccd2f81cece0c444` (identical in both kits)
- Tests collected: 87 (CPU tier: contract conformance + core record helpers + tools + project consistency + project modules)

## Commands and outcomes

| Check | Command | Exit code | Result |
|---|---|---:|---|
| ruff format --check | `ruff format --check src tools tests contracts/v1` | 0 | 26 files already formatted |
| ruff check | `ruff check src tools tests contracts/v1` | 0 | All checks passed! |
| mypy | `mypy src tools contracts/v1/validate.py contracts/v1/audit_splits.py contracts/v1/writer.py` | 0 | Success: no issues found in 19 source files |
| pytest | `-m pytest -p no:cacheprovider` | 0 | 87 passed in 1.05s |
| check_hashes | `tools/check_hashes.py` | 0 | hash locks OK: contract release, program document |
| scan_secrets | `tools/scan_secrets.py` | 0 | secrets/absolute-path scan OK |
| check_links | `tools/check_links.py` | 0 | markdown links OK |
| budget_preflight | `tools/budget_preflight.py --budget config/budget.json --plan config/cpu-smoke-plan.json` | 0 | "status": "local_plan_within_configured_limits", |
| validate fixtures | `contracts/v1/validate.py contracts/v1/examples/arm_sim/episode.json` | 0 | "status": "contract_valid", |
| audit fixtures | `contracts/v1/audit_splits.py contracts/v1/examples/arm_sim/episode.json contracts/v1/examples/drone_sim/episode.json contracts/v1/examples/imagined_arm/episode.json` | 0 | "status": "declared_group_and_lineage_checks_passed", |

All commands above were run with the repository root as the working directory (`python` = the packaging interpreter).

## Not run (and therefore not claimed)

- No ManiSkill3, PX4, Gazebo, ROS 2, PyTorch or Isaac Lab installation or run; `config/stack-lock.pending.json` pins are unresolved.
- No milestone or stage exit test; every phase is `not_started` on the status board; `reports/` holds no milestone report.
- No GitHub CI run (`.github/workflows/ci.yml` is untested on GitHub; its steps are the same `make` targets executed here).
- No `tools/check_immutable.py` run against a real PR (its logic is covered by `tests/test_tools.py` on temporary git repositories).
- No paid service, hardware, flight, arm motion, remote repository, or other project was touched.

## Interpretation

A green CPU tier proves serialization, integrity and tooling behaviour on fabricated fixtures. It is not evidence about any simulator, model, robot or aircraft.

