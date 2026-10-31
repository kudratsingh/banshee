# ADR-0003 — Project names: `banshee` and `vishwaroop`

**Date:** 2026-10-31 · **Status:** accepted · **Work order:** WO-006 in `banshee`; the next free work-order id in `vishwaroop` · **Program link:** PROGRAM §5, §11, §14

## Context
The owner decided the project names on 2026-10-31. The Omni Drone repository and Python package are `banshee`; the World Model & Planner repository and Python package are `vishwaroop`. Both starter kits still carry the old identifiers, including in three places that must stay byte-identical across the repositories: `PROGRAM.md`, the shared `AGENTS.md` core (sections 1–12), and `contracts/v1/`. The episode schema's `producer` enum and two fabricated example episodes are among them, so this is a contract change (`AGENTS.md §2.3, §11`) and needs a program-level ADR.

## Decision
1. **Names.** Repository paths, package imports, `config/phases.json#project` and contract `producer` values use `banshee` and `vishwaroop`. The descriptive names "Omni Drone", "World Model & Planner", "the drone project" and "the world-model project" stay valid in prose and docs. "Omni" keeps its recorded meaning of broad mission capability.
2. **Contract.** The `producer` enum becomes `arm`, `banshee`, `vishwaroop`, and the `drone_sim` and `imagined_arm` fixtures use the new values. `RELEASE.json` names the new consumers and the release label becomes `1.0.0+kit.2026-10-31.names`.
3. **`schema_version` stays `1.0.0`, and the path stays `contracts/v1/`.** Removing an enum value is breaking under `AGENTS.md §11.3`, which would normally mean a new major release with a migration. This change does not take that path because the owner directed an in-place change, and because nothing needs migrating: the only records under the old values are the fabricated fixtures changed here, and no real episode, export or pinned external consumer exists yet. After the first real episode is exported, §11.3 applies in full.
4. **The contract's own name stays.** `omni-world trajectory contract` and the `urn:omni-world:...` schema ids name the contract, not a repository or package. They are outside the owner's list and do not change.
5. **Documents.** `PROGRAM.md` becomes version 1.1 with dated rows in §11 and §14. The `AGENTS.md` core changes its repository names only, so no rule changes and the policy version stays 1.0.
6. **ADR numbers.** This program ADR takes ADR-0003 in both repositories. Planned project ADRs move up one: in `banshee`, the D0 airframe and stack ADR becomes ADR-0004 and the D1 frame and timebase ADR becomes ADR-0005; in `vishwaroop`, the M0 task-choice ADR becomes ADR-0004.

## Shared bytes
These files must match byte for byte in both repositories: `PROGRAM.md`, everything under `contracts/v1/`, `config/contract-lock.json`, `config/program-lock.json`, this ADR, and `AGENTS.md` up to but not including the `## 13.` heading.

To avoid two independently worded versions, the repository that applies this change second copies these bytes from the first and does not re-author them. It then confirms these values:

| Item | sha256 |
|---|---|
| `contracts/v1/SHA256SUMS.json` | `9c0b9347be3758b359c7c7e9fdf7eb7798086167fb1162112fcc9d22bd5a61c3` |
| `PROGRAM.md` (version 1.1) | `58f4c930ca08aaa2fd630826905e9ef9892968e7ceda8e2d920863f5142d02a9` |
| `AGENTS.md` core (bytes before `## 13.`) | `9b442240b95c6b6f94d6e99d0c597561689c2dbdbe74f202cfbc7ae99f40364e` |

## Alternatives considered
| Option | Why not |
|---|---|
| Keep `omni_drone` and `world_model` as `producer` values and rename only repositories and packages | contradicts the owner's decision; contract records would name projects that no longer exist under those names |
| New major contract release (`schema_version` 2.0.0, `contracts/v2/`) | the owner directed a change to `contracts/v1/`; a migration for fixtures alone adds a version with nothing to migrate |
| Accept both old and new `producer` values | keeps retired names in the contract permanently, and no record needs them |
| Rename the contract and its URNs too | outside the owner's list, and it changes every schema id for no functional gain |

## Consequences
- Any record using `producer: omni_drone` or `producer: world_model` now fails validation. None exists outside the fixtures changed here.
- The change is not complete until both repositories carry the same bytes and each one's `make check` is green. Neither repository's change merges to `main` until the shared hashes are confirmed in both, or until the owner records why not (`AGENTS.md §11.3`).
- The owner's Claude Project copy of `PROGRAM.md` must be updated to version 1.1.
- This decision authorizes no remote, purchase or hardware action.

## Reversibility
Low cost while no real records exist: revert the rename commits in both repositories. After real episodes exist, changing `producer` values again would be a breaking contract release under `AGENTS.md §11.3`.
