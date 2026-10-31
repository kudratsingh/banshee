# START_HERE — Omni Drone

**You are a coding agent starting a session in the `banshee` repository. This page tells you what to read, what to run, and what to do first.**

## 1. Read (in this order, every session)
1. `PROGRAM.md` — where the whole program is going and why this project exists (§5.1, §6).
2. `AGENTS.md` — the rules: authorization matrix (§2), workflow (§3–4), stages and exit tests (§5), append-only records (§6), evidence words (§7), stop conditions (§12), drone addendum (§13).
3. `docs/STATUS_BOARD.md` — where the project is right now.
4. The active or next work order in `work_orders/`.
On a first session also read `docs/PHASES.md`, `docs/ARCHITECTURE.md`, `docs/CONTEXT_AND_DECISIONS.md`, `docs/OPERATING_ENVELOPE.md`, `docs/TEST_PROTOCOL.md`, `docs/REFERENCE_AND_SENSING.md`, `docs/BOM_WORKSHEET.md`, `docs/ENVIRONMENT.md`.

## 2. Run (before touching anything)
```bash
python3 -m venv .venv && . .venv/bin/activate && python -m pip install -r requirements-dev.txt
make check && make board
git status   # if this is not yet a git repository: git init -b main && git add -A && git commit -m "Starter kit import"
```
`make check` must be green. If it is not, fixing it is the first task and gets its own PR.

## 3. Status today (2026-10-31)
- Every stage `not_started`. See `docs/STATUS_BOARD.md` for work-order states: WO-006 (the program-wide rename, ADR-0003), WO-008 and WO-009 (starter-kit tooling fixes) are accepted, and WO-001 is next. No simulator has run; no hardware exists; no flight has happened. Fixtures are fabricated.
- `config/repo.json`: the private remote `kudratsingh/banshee` is designated (ADR-0006). No other remote may be added. Agents merge their own pull requests when all required checks are green, after a full review where `AGENTS.md §13.9` requires one. Owner approval is only for the authorization matrix (`AGENTS.md §2`).
- `config/budget.json`: $0 approved. Hardware purchase is an owner action that follows D0 and D1.
- The test space (room vs garage/field) is undecided; D0 must surface it (ET-D0-6).

## 4. First work order
`work_orders/WO-001-d0-operating-envelope-and-platform-proposal.md` — desk work, any machine. Then WO-002 (SITL) needs an Ubuntu machine, VM or container (`docs/ENVIRONMENT.md`). WO-003 (budget enforcement) can run in parallel in its own worktree.

## 5. Unresolved owner decisions you may hit
`docs/CONTEXT_AND_DECISIONS.md §5` and `PROGRAM.md §12`: test space; airframe; companion computer and depth camera; stack pins; frame convention. Take the recorded default, write the assumption into the report, and continue — stop only at `AGENTS.md §2.3` gates or §12 conditions. **Never connect to or command any physical flight controller in D0–D1.**

## 6. Exact next actions
Branch from the updated `main`.
1. `make check` green → `python tools/status_board.py --append --wo WO-001 --event ready`, then `--event in_progress`; `--phase D0 --event ready`, then `in_progress`.
2. Branch `wo/WO-001-d0`; fill `docs/OPERATING_ENVELOPE.md` and `docs/BOM_WORKSHEET.md` (both airframe options, sourced and dated); write `config/stack-lock.proposed.json` with every pin labelled `proposed` and an evidence URL; write ADR-0007; draft `evals/D1-exit-tests.json`.
3. Write `reports/WO-001-d0-operating-envelope-and-platform-proposal.md` with the owner decision request. This work order closes milestone exit tests, so run the full review (`AGENTS.md §13.9`); then open the PR and merge it when `AGENTS.md §4.6` holds. Then ask the owner for the decision.
4. When the owner records a decision or deferral in `ledgers/approvals.jsonl`, append `accepted`; `make board`; continue to WO-002 (software only).

The first-session prompt the owner pastes into a fresh agent is `prompts/FIRST_SESSION.md`.
