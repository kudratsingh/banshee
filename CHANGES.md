# CHANGES.md — what this kit changed relative to the 2026-10-30 reference bundle, and why

Reference inputs: `Omni_Drone_World_Model_Starter_Kits_2026-10-30.zip` (reference starter), `Handoff_and_Release_Notes.zip`, `START_HERE.md`, the review prompt `Final_Starter_Kits_Review_Agent_Prompt.md`, and the Sept–Oct 2026 planning conversations (recorded in `PROGRAM.md` and `docs/CONTEXT_AND_DECISIONS.md`).

## Audit of the reference bundle (what was checked, what was found)
- Reran the reference tests in a clean environment (Python 3.13.18, jsonschema 4.26.0, pytest 9.1.1): **43 passed** per project, matching the reference claim. Contract hashes matched `SHA256SUMS.json` and `config/contract-lock.json`. Both JSON Schemas validate as Draft 2020-12.
- Lint: the reference utilities failed 144 `ruff` findings (compressed one-line style, unsorted imports, unused imports); `mypy --strict` passed on `validate.py`. Behaviour was correct; readability was not.
- Contradictions found: (1) "no branches/PRs/GitHub writes" and "stop after every work order" vs the owner's autonomous-development instruction; (2) `WO-002` id used twice in the drone kit; (3) the drone kit's `CLAUDE.md` carried world-model-only rules; (4) the contract README implied evidence is added by editing an episode manifest, which conflicts with the owner's never-overwrite rule; (5) the handoff prompt said "do not advance to another work order automatically".
- No fabricated results, secrets, or machine-specific paths were found in the reference.

## Substantive changes
| Area | Change | Reason |
|---|---|---|
| Program document | New `PROGRAM.md`, identical in both kits and in the Claude Project; hash-pinned (`config/program-lock.json`) | Owner asked for one central document every agent can refer to for the trajectory of all projects and his ML/robotics advancement |
| Policy source | `AGENTS.md` (shared core + project addendum) is the single authoritative policy; `CLAUDE.md` is a pointer | Review prompt §2; avoids independently maintained copies of the same rules |
| Authorization | Explicit matrix (`AGENTS.md §2`): autonomous work inside the repository; remote ops only after designation; separate dated approvals for spending, hardware motion, destructive ops, access, publication, sealed access, existing-project changes, scope/safety changes; agents continue to the next ready WO | Owner's Oct 30 instruction; reconciles the old blanket prohibitions |
| Git/subagent/CI | Feature branches, worktrees per subagent with file ownership, integrating agent, merge rule on exact candidate, CI tiers, rollback by revert, least-privilege CI (`AGENTS.md §4`, `docs/WORKFLOW.md`, `.github/workflows/ci.yml`, `Makefile`, `.pre-commit-config.yaml`) | Review prompt §4 |
| Append-only records | Rule (`AGENTS.md §6`), detail (`docs/DATA_POLICY.md`), CI enforcement (`tools/check_immutable.py`: pure-append for ledgers/reports, write-once for data/manifests, frozen accepted WOs), code enforcement (`src/*/core/`: append-mode ledgers, content-addressed store with no delete, exclusive-create run dirs; `contracts/v1/writer.py` write-once export) | Owner's rule: never delete or overwrite data, runs, logs; always append or create a new record |
| Phases and exit tests | `config/phases.json` (machine-readable, D0–D7 with ET ids, evidence, thresholds as proposed defaults) + `docs/PHASES.md` narrative + consistency test; `AGENTS.md §5` rules (frozen before start; state machine; evidence-only passes) | Owner asked for exit tests per stage and a ladder anyone can follow |
| Status tracking | Append-only `work_orders/STATUS.jsonl` with validated transitions; derived `docs/STATUS_BOARD.md` (`tools/status_board.py`) | Anyone can track and follow the plan |
| Agile process | Cycle, definition of ready/done, WIP limits, sizing with estimate-vs-actual, retro note per report (`AGENTS.md §3`, `docs/WORKFLOW.md §1`) | Owner asked for agile development |
| ML/software fundamentals | `AGENTS.md §8` (reproducibility, pins, baselines first, tracking, tests, typed code, dependencies, resource bounds, simplicity, ADRs) and §10 (security) | Owner asked for fundamental rules for agents |
| Contract release | Schemas unchanged (v1.0.0); utilities reformatted without semantic change; added `validation_ledger.schema.json` and `validate.py --ledger` (append-only evidence); added `writer.py` (write-once reference exporter); added `RELEASE.json`; tests 32 → 41; `SHA256SUMS.json` regenerated; both kits pinned to the new manifest hash | Append-only rule; actionable export path for WO-001 and D1 |
| Work orders | Five WOs with the standard header (phase, exit tests, size, prerequisites, authorization, files); WO-001 D0, WO-002 D1 SITL and WO-003 budget detailed; WO-004 fault matrix and WO-005 D2 milestone-level; the duplicate `WO-002` id fixed | Review prompt §2; numbering fix |
| Scaffolding | `src/banshee/core/` (tested), `freshness.py` (tested setpoint-freshness / estimator-validity gate: heartbeat never counts, no universal hover, land on lost localization), `interfaces.py` (typed Protocols incl. CommandGate and a reject-able LearnedProposalAdapter); `pyproject.toml` with ruff/mypy/pytest config | Makes WO-002/WO-004 actionable; typed interfaces per review prompt §7 |
| Docs | `ARCHITECTURE` (layered conventional stack, command authority, exact interfaces), `CONTEXT_AND_DECISIONS` (conversation context + contradictions table), `OPERATING_ENVELOPE` (template with proposed defaults and corrected FAA notes), `TEST_PROTOCOL` (fault matrix, freshness, pre-flight checklist, statistics), `REFERENCE_AND_SENSING`, `BOM_WORKSHEET` (two airframe options with dated price observations), `ENVIRONMENT` (Ubuntu-only flight stack; Macs via VM), `BUDGET_AND_LAUNCHER`, `SOURCES` (dated; hardware sources added; unverified items listed), `REPORT_TEMPLATE`, `ADR_TEMPLATE` + two program ADRs | Review prompt §1–§7 |
| Handoff | `prompts/FIRST_SESSION.md` rewritten under the new authorization; `START_HERE.md` with exact next actions | Review prompt §2–§3 |
| Verification | `VERIFICATION.md` written from the actual packaging run (environment, commands, outcomes, not run); kit-level `SHA256SUMS.json` | Review prompt §8 |

## Preserved from the reference (audited, kept)
Contract schemas and fixtures (fabricated, labelled); validator semantics; split-audit semantics; budget preflight semantics and tests; the D0–D7+ ladder with D3 optional; operating-envelope fields; the fault matrix; freshness and heartbeat separation; outside-in reference qualification; corrected FAA guidance; the $0 default budget; regulatory sources S1–S5 and the technical sources S6–S11.

## Not done in this pass (honest list)
No SITL, offboard bridge, export adapter, fault harness, reference pipeline, mission executive or launcher was implemented. No stack pins were resolved (`config/stack-lock.pending.json`). No web re-verification of PX4/ManiSkill/Isaac versions (owner declined the searches); hardware prices were verified on 2026-10-30 and are recorded with dates. No remote repository, CI run on GitHub, paid service, hardware, or other project was touched.

## After import: program-wide rename (2026-10-31, ADR-0003, WO-006)
The starter kit shipped as `omni-drone`. The repository and package are now `banshee`, and the sibling project is `vishwaroop`. Paths in this file were updated so they still resolve. The contract `producer` enum and fixtures, `PROGRAM.md` (version 1.1), the shared `AGENTS.md` core (policy version 1.1), manifests and locks changed with it. The one behaviour change: the validator now rejects the retired `producer` values and accepts the new ones. `schema_version` stays 1.0.0 because the rename predates any data. No other behaviour, threshold or authorization changed. Planned ADR numbers moved up one (`docs/adr/ADR-0003-PROGRAM-project-names.md`).

## After import: starter-kit defects fixed (2026-10-31, WO-008)
The rename did not cause these. They are in WO-008, in commits `95f7a34` and `e412aea`, separate from the rename, on the owner's instruction.
- **`tools/status_board.py`:** `--phase` and `--et` appends were always refused, because the record carried `"wo": null` and took the work-order path. The command line now drops unset fields before `append()`, and `current_states` tests its keys by `.get()` truthiness. `tests/test_tools.py` adds tests for these appends through the command line. A record naming more than one of `--wo`, `--phase` and `--et` is now refused: the fix had otherwise let a combined call mark a phase as passed without recording the exit test.
- **`tests/test_project_consistency.py`:** deleted `test_no_fixture_claims_in_reports` on the owner's instruction. It failed on any file in `reports/`, so it blocked every real work-order report.
- **`.gitignore`:** `*secret*` silently dropped `tools/scan_secrets.py` from `git add -A` and hid it from `ruff`. WO-008 replaced it with specific patterns plus an exception for the scanner; WO-009 then returned to the broad rule and kept the exception.

## After import: accepted work orders and secret scan (2026-10-31, WO-009)
These also came with the starter kit, and the owner asked for them before WO-001.
- **`tools/status_board.py`:** a `created` event is refused for any work order that already has a ledger record, so the tool cannot reset an accepted work order.
- **`tools/check_immutable.py`:** the freeze now holds once any `accepted` event exists, so a line appended by hand cannot lift it, and replacing a protected file with a symlink is rejected. This goes beyond the tool the owner named, because the owner's stated goal was that the freeze cannot be reset.
- **`tools/scan_secrets.py`:** adds Hugging Face (`hf_`) and RunPod (`rpa_`) patterns, each requiring 30 or more alphanumerics, and now scans files with no extension. One consequence: a local `.env`, though ignored by git, is scanned too, so a real key in it makes `make secrets` fail.
- **`.gitignore`:** back to the broad `*secret*` rule plus `!tools/scan_secrets.py`, keeping `secrets/` and `.secrets*`, on the owner's instruction. The specific-pattern list left names like `secret_prod.env`, `mysecret` and `secretkey` trackable. The WO-009 file was renamed to `...-token-scan.md`, because the broad rule would have ignored its old name and its report, and a new test fails if any tracked file is ignored.
- **`tests/test_tools.py`:** adds tests for all of these, with token literals built at runtime.

## After import: rename merged and accepted (2026-10-31)
Pull request 1 merged at `292d368` on the owner's approval, after both repositories were verified. WO-006, WO-008 and WO-009 are `accepted`, each with a report in `reports/`. `START_HERE.md` no longer says the rename is waiting; a later pull request still needs its own owner approval.

## After import: merge and review rule (2026-10-31)
On the owner's instruction, agents merge their own pull requests when all required checks are green, and owner approval is only for the authorization matrix. `AGENTS.md §13.9` now requires a full review first for milestone exit tests, RL-loop and evaluator work orders, and anything touching the contract; everything else merges on CI alone. This replaces the per-pull-request approval wording in `START_HERE.md`, `prompts/FIRST_SESSION.md` and WO-001. The shared `AGENTS.md` core did not change.

## After import: WO-011 and WO-012 superseded (2026-10-31)
On the owner's instruction, the shared material is being built by its own agent in `ironclad`, from `main` at `9f77ea7`. WO-011 and WO-012 were never started. Each has a short file so the status ledger can name it. This repository authors no program ADR or policy text from now on.

## After import: WO-003 superseded (2026-10-31)
On the owner's instruction, the paid launcher moved to `ironclad`. WO-003 was never started. Paid execution stays blocked here.

## After import: owner decisions on WO-001 (2026-10-31)
All flight stages move outdoors to an open field, so D3 is required and D4 now follows it. The X500 V2 stays, with a Pixhawk 6X, and Option B is dropped. `PROGRAM.md` still calls D3 optional and describes indoor stages; it is a shared file, left for `ironclad`.

## After import: ironclad adopted (2026-10-31, WO-013, ADR-0008)
The shared contract, core, tools and tests now come from the pinned `ironclad-kit` v1.1.0, and the vendored copies are gone. `sync-policy` added a marker line to each policy copy, without changing the `AGENTS.md` core or `PROGRAM.md` otherwise, and updated `docs/WORKFLOW.md`, `docs/DATA_POLICY.md`, `docs/BUDGET_AND_LAUNCHER.md` and `work_orders/README.md` to the new commands and the launcher. The root `SHA256SUMS.json` is removed, because nothing would maintain it.

## After import: D1 nominal missions (2026-10-31, WO-002, ADR-0005)
SITL now runs from a measured lock, and flies a route through the offboard velocity interface, with an independent judge and a contract export per run. Ten of ten counted missions passed in simulation. See `reports/WO-002-d1-sitl-offboard-mission-and-contract-export.md`, including an unexplained 0.9 m landing offset carried to WO-004.

## After import: D1 fault matrix (2026-11-01, WO-004, ADR-0009)
Every D1 fault case now runs against the real command path in SITL, with a log and a contract export per case, and deviations are reported. The first recording found the mission node overriding the operator from a land latch. That is fixed, and the matrix was recorded four times in all, with the fourth as the results of record. Nothing armed in the vision-only world, so that flight was not shown, and ADR-0010 proposes carrying it to D4. Estimator age during landing came within 8 ms of its bound, which D2 has to measure.

## After import: owner decisions after D1 (2026-11-01, WO-015)
ADR-0010 is accepted. The D3 standoffs are frozen at 8.6 m and 3.35 m in `evals/D3-standoffs.json`, and the envelope now states that the 150 m exclusion radius covers position loss on its own, with its arithmetic. The VM disk cap and free-space check are recorded as done.

## After import: the node yields to a mode chosen while disarmed (2026-11-01, WO-016, ADR-0009)
Before flight, the node now asks for offboard only from Hold and yields on anything else. WO-004's node would take the aircraft from a mode the operator had selected, then arm it. New case R-07 shows the fix, and the 47 earlier cases keep their mode sequences in one new recording. Simulation only.

## After import: purchase request and D2 freeze (2026-11-01, WO-017)
The re-priced Option A order is one table in `docs/PURCHASE_REQUEST-2026-11-01.md`, with a planning total of $3,884.44. D2's exit tests are frozen in `evals/D2-exit-tests.json`, with sample sizes added. D2 is not started, and nothing was bought.

## After import: purchase approval recorded (2026-11-01, WO-018)
The owner's line-by-line approval is in `ledgers/approvals.jsonl`, and `docs/BUY_LIST-2026-11-01.md` applies its substitutions and sourcing rule. The planning total is $3,352.02. Nothing is bought yet. WO-019 holds the stale-status window to close before D3.

## After import: buy-list decisions recorded (2026-11-01, WO-020)
Each decision is in `ledgers/approvals.jsonl`, including the owner's correction of C2: the SiK V3 is withdrawn, and an RFD900x-US is the D3 substitute. The planning total is $3,506.19 at Standard FOV or $3,615.19 at Wide. The field-of-view pick is open. Nothing is bought yet.

## After import: X650 platform, purchases on hold (2026-11-01, WO-021)
The owner chose the X650 and the Pixhawk Jetson bundle and put all purchases on hold. `docs/BUY_LIST-REPRICED-2026-11-01.md` holds the new list and FCC check; ADR-0007 records the X500 as superseded. WO-022 recomputes the envelope and updates the D2 tests.
