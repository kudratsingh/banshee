# ADR-0006 — Private GitHub remote for this repository

**Date:** 2026-10-31 · **Status:** accepted · **Work order:** WO-007 · **Program link:** PROGRAM §12 decision 7

## Context
The owner asked for the GitHub repository to be created on 2026-10-31. `AGENTS.md §2.2` allows remote operations only once a remote is designated in `config/repo.json`, and only under an account the owner has named, never public. The owner did not spell out an account. `gh` is logged in to the owner's personal account `kudratsingh`, which is also the owner's git identity.

## Decision
- Remote: `https://github.com/kudratsingh/banshee.git`, private, default branch `main`.
- Protection requested for `main`, per `docs/WORKFLOW.md §8`: pull requests required, CPU-tier checks required, force-push and deletion disallowed. GitHub may decline this on a private repository, depending on the plan; the result is recorded in `VERIFICATION.md`.
- ADR numbers 0004 and 0005 stay reserved by ADR-0003, so this ADR takes 0006.

## Alternatives considered
| Option | Why not |
|---|---|
| One of the organizations the account belongs to | none is the owner's stated home for this work |
| Public repository | forbidden without a separate owner decision (`AGENTS.md §2.3`); no license is chosen (PROGRAM §12 decision 8) |

## Consequences
Pushes and CI become available for this repository. CI on a private repository uses the account's GitHub Actions allowance. The `vishwaroop` project is unaffected and has no remote from this decision.

## Reversibility
The owner can set `designated` back to `false` and delete or move the repository on GitHub. Deleting it is a §2.3 action for the owner.
