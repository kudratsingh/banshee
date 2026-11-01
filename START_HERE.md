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
- See `docs/STATUS_BOARD.md` for stage and work-order states. No simulator has run; no hardware exists; no flight has happened. Fixtures are fabricated.
- `config/repo.json`: the private remote `kudratsingh/banshee` is designated (ADR-0006). No other remote may be added. Agents merge their own pull requests when all required checks are green, after a full review where `AGENTS.md §13.9` requires one. Owner approval is only for the authorization matrix (`AGENTS.md §2`).
- `config/budget.json`: $0 approved. Hardware purchase is an owner action that follows D0 and D1.
- Test space: a large open field, outdoors; all flight stages outdoors. Airframe: X500 V2 with Pixhawk 6X (ADR-0007). No purchase is authorized (`ledgers/approvals.jsonl`).

## 4. First work order
WO-001 closes on the owner's decisions (see the status board). WO-002 (SITL) needs an Ubuntu machine, VM or container (`docs/ENVIRONMENT.md`). WO-003 is superseded: the paid launcher moved to `ironclad`.

## 5. Unresolved owner decisions you may hit
`docs/CONTEXT_AND_DECISIONS.md §5` and `PROGRAM.md §12`. Test space, airframe, flight controller, companion computer and camera are decided (`ledgers/approvals.jsonl`, ADR-0007); `PROGRAM.md` has not caught up, and a dated owner message takes precedence. Stack pins and the frame convention remain: take the recorded default, write the assumption into the report, and continue. Stop only at `AGENTS.md §2.3` gates or §12 conditions. **Never connect to or command any physical flight controller in D0–D1.**

## 6. Exact next actions
WO-002, simulation only, with no purchase. Target `px4_fmu-v6x_default` for the compile check; SITL uses `make px4_sitl gz_x500`. Jazzy first, Humble as the fallback (ADR-0007).
1. Branch from the updated `main`. Record `ready` and `in_progress` for WO-002 and phase D1, after the D1 exit tests are frozen.
2. Follow `work_orders/WO-002-d1-sitl-offboard-mission-and-contract-export.md`; the D1 verification plan is in ADR-0007.

The first-session prompt the owner pastes into a fresh agent is `prompts/FIRST_SESSION.md`.
