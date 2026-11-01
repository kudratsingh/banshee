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
make check          # lint, types, tests, ironclad verify, secrets scan, link check
make board          # regenerate docs/STATUS_BOARD.md
ironclad contract-info
```
These commands do not run PX4 or Gazebo and are not flight logs. The contract fixtures are fabricated.

## Current status (2026-10-31)
| Implemented and tested here | Specified, not implemented |
|---|---|
| contract v1 (schemas, validator with append-only ledger merge, split audit, write-once reference writer, fixtures, 41 tests) | live-link and hardware testing (D2 onward) |
| core record helpers: append-only ledgers, content-addressed artifacts, write-once run dirs, structured logs, strict config | fault-matrix harness (WO-004); outside-in reference pipeline (D2) |
| setpoint-freshness / estimator-validity gate (pure logic; bounds frozen in D1) | mission executive and skills (D5–D6) |
| typed Protocol interfaces (estimator, command gate, skill, mission executive, outcome judge, learned-proposal adapter) | world-model adapter in shadow mode (D7+) |
| tools: status ledger/board, append-only CI check, hash locks, secrets scan, link check, budget preflight | enforcing paid launcher (moved to `ironclad`) |
| SITL launch and version lock, offboard mission, independent judge, contract export (WO-002; simulation only) |  |
| CI workflow (CPU tier), Makefile, pre-commit hooks | hardware (none owned), compliance steps |

See `docs/STATUS_BOARD.md` for each stage's state. Offboard flight has run in simulation only. No flight controller, VIO stack, avoidance system, reference tracker or aircraft has been connected or tested. All physical gates are closed. No purchase is needed for D0/D1.

## Layout
```
PROGRAM.md  AGENTS.md  CLAUDE.md  START_HERE.md  CHANGES.md  REQUIREMENTS_CHECKLIST.md  VERIFICATION.md
config/      phases.json, budget.json, repo.json, stack-lock.proposed.json, stack-lock.pending.json, sealed-access schema
docs/        PHASES, ARCHITECTURE, CONTEXT_AND_DECISIONS, OPERATING_ENVELOPE, TEST_PROTOCOL, REFERENCE_AND_SENSING,
             BOM_WORKSHEET, ENVIRONMENT, WORKFLOW, DATA_POLICY, BUDGET_AND_LAUNCHER, REPORT_TEMPLATE, ADR_TEMPLATE, SOURCES, STATUS_BOARD, adr/
src/banshee/      freshness.py, interfaces.py   (sitl/, offboard/, export/, outcome/, faults/, reference/, mission/, learned/ to come)
tests/       project tests; shared tests and contract conformance come from ironclad's pytest plugin
work_orders/ WO-001..009 + STATUS.jsonl (append-only)      prompts/FIRST_SESSION.md
data/ runs/ ledgers/ artifacts/ reports/ evals/   append-only record locations
```
