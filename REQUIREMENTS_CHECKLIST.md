# REQUIREMENTS_CHECKLIST.md — requirement → where it lives → status

Status words: **confirmed** (owner decision), **proposed default** (suggested, not objected to), **unknown**, **future option**. Milestone references point to `docs/PHASES.md`.

| # | Requirement (owner or review) | Where it lives | Status |
|---|---|---|---|
| 1 | One central program document for all agents, covering the trajectory of all projects and the owner's ML/robotics advancement | `PROGRAM.md` (identical in both kits; `config/program-lock.json`) | confirmed |
| 2 | Two independent projects; the drone is conventional-first and never waits for the world model; exports to it through the contract only | `PROGRAM.md §5–6`, `docs/PHASES.md`, ADR-0001 | confirmed |
| 3 | No Microduck, no rocket warm-up, no third project / shared runtime | `PROGRAM.md §5.5`, ADR-0001 | confirmed |
| 4 | Conventional-first D0–D7+ ladder; optional outdoor checkout; qualified localization/reference sensing; setpoint freshness; degraded modes; real connection-loss tests; operator authority | `docs/PHASES.md`, `docs/TEST_PROTOCOL.md`, `docs/REFERENCE_AND_SENSING.md`, `src/omni_drone/freshness.py` | confirmed |
| 5 | Exit tests for every stage, written before the stage starts; clear ladder anyone can follow | `config/phases.json`, `docs/PHASES.md`, `AGENTS.md §5`, `docs/STATUS_BOARD.md` | confirmed |
| 6 | Never delete or overwrite data/runs/logs; append or new record | `AGENTS.md §6`, `docs/DATA_POLICY.md`, `tools/check_immutable.py`, `src/omni_drone/core/`, `contracts/v1/writer.py`, validation ledger | confirmed |
| 7 | Agile development: backlog of WOs, ready/done, WIP, cycles, retros | `AGENTS.md §3`, `docs/WORKFLOW.md §1`, `work_orders/README.md` | confirmed |
| 8 | Fundamental ML/software rules for agents | `AGENTS.md §8, §10` | confirmed |
| 9 | Autonomous iterative development; branches/PRs/merges in designated repos; no approval request per ordinary PR | `AGENTS.md §2.1, §4.6`, ADR-0002, `prompts/FIRST_SESSION.md` | confirmed |
| 10 | Separate approval for spending, hardware motion, paid compute outside envelope, deployment, destructive ops, access, publication, existing-project changes, scope/safety changes, sealed access | `AGENTS.md §2.3`, `ledgers/approvals.jsonl` | confirmed |
| 11 | Remote operations only for an explicitly designated repository; never invent a remote or make public | `config/repo.json`, `AGENTS.md §2.2`, `docs/WORKFLOW.md §8` | confirmed (remote: unknown) |
| 12 | Git/subagent/CI workflow: worktrees, ownership, integrating agent, merge rule, tiers, rollback, least privilege | `AGENTS.md §4`, `docs/WORKFLOW.md`, `.github/workflows/ci.yml` | confirmed |
| 13 | One shared versioned contract, identical in both kits, with conformance tests and labelled fixtures | `contracts/v1/`, `config/contract-lock.json`, `tools/check_hashes.py` | confirmed |
| 14 | Contract steward, release and compatibility rules, migration requirement; model manifests in the same boundary | `contracts/v1/RELEASE.json`, `contracts/v1/README.md`, `AGENTS.md §11` | confirmed |
| 15 | Safety checks inside stage acceptance criteria; code merged / SITL passed / flight-ready are separate states | `config/phases.json`, `AGENTS.md §13.1`, `docs/PHASES.md` | confirmed |
| 16 | Operating envelope written before hardware choice; test space decides the airframe; priced BOM with dated sources; purchase is an owner action | `docs/OPERATING_ENVELOPE.md`, `docs/BOM_WORKSHEET.md`, WO-001, ET-D0-6 | confirmed (space: unknown) |
| 17 | Pin and test the actual command path (PX4 release, bridge, offboard velocity interface); proposed vs tested pins distinguished | `config/stack-lock.pending.json`, WO-001, WO-002, ET-D0-3, ET-D1-1 | confirmed (pins: unknown) |
| 18 | Measured results separate from estimates, mocks, plans; every report has methods, baselines, versions, lineage, commands, outcomes, limits, failures, costs | `AGENTS.md §7`, `docs/REPORT_TEMPLATE.md` | confirmed |
| 19 | Protect existing projects; isolate environments; no broad cleanup | `AGENTS.md §1` | confirmed |
| 20 | Budgets: default $0; measured pilot; authorization-bound files; reservations; time/step limits; cost ledger; provider teardown verification; preflight is not a launcher | `config/budget.json`, `docs/BUDGET_AND_LAUNCHER.md`, `tools/budget_preflight.py`, WO-003 | confirmed |
| 21 | Reproducible environment guidance; platform/GPU assumptions; what runs where | `docs/ENVIRONMENT.md`, `config/stack-lock.pending.json` | confirmed (pins: unknown) |
| 22 | Credentials outside source control; untrusted inputs; safe loading; licenses; privacy; retention; manifests | `AGENTS.md §6.6–6.7, §10`, `docs/DATA_POLICY.md`, `tools/scan_secrets.py` | confirmed |
| 23 | Simple modular components, typed interfaces, structured logs, no enterprise infrastructure | `AGENTS.md §8.6, §8.9`, `src/omni_drone/interfaces.py`, `core/log.py` | confirmed |
| 24 | Validation of the final packages with checksums and a verification report | `VERIFICATION.md`, `SHA256SUMS.json` | confirmed |
| 25 | Future missions (object search, mapping, onboard autonomy) one at a time; drone research question (uncertainty-gated trust in learned dynamics) | `PROGRAM.md §7–8`, `docs/PHASES.md` D7 | confirmed / future option |
| 26 | Hardware plan recorded, nothing purchased by these files | `PROGRAM.md §9` | confirmed intent |
| 27 | FAA: Part 107 for non-recreational flights; 250 g is not a blanket exemption; indoor-only outside Part 107 but controlled | `docs/OPERATING_ENVELOPE.md`, `docs/SOURCES.md` [S1]–[S5] | confirmed |
| 28 | Outside-in reference is an evaluator, never an operational input in unaided-VIO tests; qualified for accuracy/coverage/latency | `docs/REFERENCE_AND_SENSING.md`, `AGENTS.md §13.6` | confirmed |
| 29 | Learned components (world-model residual dynamics) enter only via held-out → shadow → controlled closed-loop with kill switch and drone-owned acceptance | `docs/PHASES.md` D7, `AGENTS.md §13.3`, `src/omni_drone/interfaces.py: LearnedProposalAdapter` | confirmed / future option |
| 30 | Verification of current PX4/ROS 2/Gazebo pairings and VIO package | `docs/SOURCES.md` "Not verified" | unknown (WO-001/WO-002 resolve) |
