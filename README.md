# Banshee (Omni Drone)

`banshee` is the repository and Python package of Omni Drone, named for the spirit whose wail forewarns a death, and for the sound a quadrotor makes. A general-purpose aerial autonomy platform developed as a ladder of bounded, demonstrated missions. Conventional control, estimation, perception and navigation first; learned components only through evidence gates. "Omni" means growing mission capability, not a mechanically omnidirectional airframe. Part of the owner's physical-AI program — read `PROGRAM.md` first.

## The ladder
D0 operating envelope → D1 SITL + offboard velocity interface + contract logging + fault matrix → D2 props-off sensor/localization/reference checkout → D3 outdoor GPS checkout → D4 VIO position hold → D5 GPS-denied known route → D6 fixed-target inspection mission → D7+ further missions one at a time and learned-component gates. Details and exit tests: `docs/PHASES.md`.

## Read in order
`PROGRAM.md` → `AGENTS.md` → `START_HERE.md` → `docs/PHASES.md` → `docs/ARCHITECTURE.md` → `docs/CONTEXT_AND_DECISIONS.md` → `docs/OPERATING_ENVELOPE.md` → `docs/TEST_PROTOCOL.md` → `docs/REFERENCE_AND_SENSING.md` → `work_orders/WO-001-d0-operating-envelope-and-platform-proposal.md`.

## CPU-tier checks (any machine)
```bash
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check          # lint, types, tests, hash locks, secrets scan, link check
make board          # regenerate docs/STATUS_BOARD.md
python contracts/v1/validate.py contracts/v1/examples/drone_sim/episode.json
```
These commands do not run PX4 or Gazebo and are not flight logs. The contract fixtures are fabricated.

## Current status (2026-10-31)
| Implemented and tested here | Specified, not implemented |
|---|---|
| contract v1 (schemas, validator with append-only ledger merge, split audit, write-once reference writer, fixtures, 41 tests) | SITL launch + version lock, offboard velocity bridge, mission runner, contract export (WO-002) |
| core record helpers: append-only ledgers, content-addressed artifacts, write-once run dirs, structured logs, strict config | fault-matrix harness (WO-004); outside-in reference pipeline (D2) |
| setpoint-freshness / estimator-validity gate (pure logic; bounds frozen in D1) | mission executive and skills (D5–D6) |
| typed Protocol interfaces (estimator, command gate, skill, mission executive, outcome judge, learned-proposal adapter) | world-model adapter in shadow mode (D7+) |
| tools: status ledger/board, append-only CI check, hash locks, secrets scan, link check, budget preflight | enforcing paid launcher (moved to `ironclad`) |
| CI workflow (CPU tier), Makefile, pre-commit hooks | hardware (none owned), compliance steps |

All stages are `not_started`; see `docs/STATUS_BOARD.md`. No flight controller integration, VIO stack, avoidance system, reference tracker or aircraft has been built or tested. All physical gates are closed. No purchase is needed for D0/D1.

## Layout
```
PROGRAM.md  AGENTS.md  CLAUDE.md  START_HERE.md  CHANGES.md  REQUIREMENTS_CHECKLIST.md  VERIFICATION.md
config/      phases.json, budget.json, repo.json, locks, stack-lock.pending.json, sealed-access schema
contracts/v1 the one shared boundary (byte-identical in vishwaroop)
docs/        PHASES, ARCHITECTURE, CONTEXT_AND_DECISIONS, OPERATING_ENVELOPE, TEST_PROTOCOL, REFERENCE_AND_SENSING,
             BOM_WORKSHEET, ENVIRONMENT, WORKFLOW, DATA_POLICY, BUDGET_AND_LAUNCHER, REPORT_TEMPLATE, ADR_TEMPLATE, SOURCES, STATUS_BOARD, adr/
src/banshee/      core/, freshness.py, interfaces.py   (sitl/, offboard/, export/, outcome/, faults/, reference/, mission/, learned/ to come)
tests/       CPU tier;  contracts/v1/tests/  conformance
tools/       status_board, check_immutable, check_hashes, scan_secrets, check_links, budget_preflight
work_orders/ WO-001..009 + STATUS.jsonl (append-only)      prompts/FIRST_SESSION.md
data/ runs/ ledgers/ artifacts/ reports/ evals/   append-only record locations
```
