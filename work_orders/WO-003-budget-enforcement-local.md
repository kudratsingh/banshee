# WO-003 | Supervised resource and spend enforcement (local, no paid execution)
**Phase:** D0
**Exit tests advanced:** none directly (prerequisite for any paid compute or purchase tracking; keeps the cost ledger honest from the first flight hour)
**Size:** M
**Prerequisites:** none (pure local engineering). May run in parallel with WO-001/WO-002 in its own worktree; file ownership below does not overlap.
**Authorization:** AGENTS §2.1 only. Real cloud launch, payment, credentials and provider writes stay §2.3 gates.
**Files:** `tools/launcher/`, `tests/test_launcher.py`, `config/budget.schema.json`, `docs/BUDGET_AND_LAUNCHER.md` (append an "Implemented" section), `reports/WO-003-budget-enforcement-local.md`.

## Objective
Implement the enforcing side of `docs/BUDGET_AND_LAUNCHER.md` without enabling paid execution: approval validation bound to run id and hashes, atomic reservation in the cost ledger, local process supervision with wall and step limits, a fake-provider lifecycle adapter, and failure-injection tests. For this project the same ledger also records hardware purchases (owner actions) and flight hours so cost per flight hour and per mission attempt can be reported (ET-D6-4).

## Scope
1. `tools/launcher/approval.py`: parse `ledgers/approvals.jsonl`; valid only if it binds `run_id`, `command_sha256`, `config_sha256`, `cost_ceiling_usd`, `resource_count`, `expires_at`, unexpired.
2. `tools/launcher/reserve.py`: project-wide lock; atomic `planned`/`reserved` events; refuse when live reservations would exceed the project cap; cap not raisable from the CLI (test).
3. `tools/launcher/supervise.py`: child run without shell interpolation; wall timeout; step limit with progress watchdog; children terminated on parent exit; terminal events appended.
4. `tools/launcher/provider_fake.py`: fake provider whose instance can stay billable after child death; teardown verification and reconciliation.
5. `tools/launcher/flight_hours.py`: append a `flight_hours` cost line per flight run (battery cycles, operator time optional) so later stages can report cost per attempt.
6. Failure-injection tests: crash, stale progress, SIGTERM, parent loss, API timeout/retry idempotency, duplicate launch, concurrency, stale quote, overspend, leftover billable resource.

## Out of scope
Real provider APIs, secrets, network writes, actual spend, changes to `config/budget.json` caps.

## Verification
```bash
make check
python -m pytest tests/test_launcher.py -q
python tools/launcher/supervise.py --dry-run --plan config/cpu-smoke-plan.json --budget config/budget.json   # must refuse: no approval
```
Expected: all failure-injection tests pass; a run without a matching approval is refused; concurrent reservations never exceed the cap; leftover-instance case triggers teardown and reconciliation.

## Exit criteria
Tests green; report lists the remaining gap (real provider adapter with a $1-class owner-approved pilot, its own future WO). `config/budget.json` unchanged.

## Stop conditions
Any need for credentials, network writes or real resources.

## Report
`reports/WO-003-budget-enforcement-local.md`
