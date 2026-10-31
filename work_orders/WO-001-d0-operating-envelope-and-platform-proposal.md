# WO-001 | D0 operating envelope, platform proposal, stack matrix, compliance plan
**Phase:** D0
**Exit tests advanced:** ET-D0-1, ET-D0-2, ET-D0-3, ET-D0-4, ET-D0-5, ET-D0-6
**Size:** M
**Prerequisites:** the rename pull request merged, and WO-006, WO-008 and WO-009 `accepted` (status ledger). Entirely desk work: documents, sourced prices, documentation reading. No hardware, no purchase, no flight-stack installation required (installation is WO-002).
**Authorization:** AGENTS §2.1 only. Purchasing is a §2.3 owner action and is **not** part of this WO. It closes milestone exit tests, so it needs a full review before merging (`AGENTS.md §13.9`).
**Files:** `docs/OPERATING_ENVELOPE.md`, `docs/BOM_WORKSHEET.md`, `docs/REFERENCE_AND_SENSING.md` (plan section), `config/stack-lock.proposed.json`, `docs/adr/ADR-0007-d0-airframe-and-stack-proposal.md`, `evals/D1-exit-tests.json` (draft of frozen D1 bounds), `reports/WO-001-d0-operating-envelope-and-platform-proposal.md`, `docs/SOURCES-D0.md`, `docs/ENVIRONMENT.md`.

## Objective
Give the owner a one-page, numerically justified operating envelope and a priced, sourced comparison of at least two compatible platforms, with a proposed (not tested) stack version matrix and a compliance plan — so the purchase decision is made on evidence and D1 can start on pinned software.

## Scope
1. **Operating envelope** (`docs/OPERATING_ENVELOPE.md`): fill every row; where the owner has not decided (test space), write the row for *both* candidate answers and a named owner question. Derive speed/height/clearance limits from sensing range, assumed latency (to be measured in D1/D2) and stopping distance; show the arithmetic.
2. **BOM** (`docs/BOM_WORKSHEET.md`): Option A (X500 V2 class) and Option B (3–5 inch guarded frame) priced line by line with supplier URL, date, shipping/tax estimate, spares, batteries, RC link, containment, reference equipment, compute, compliance. Compatibility evidence per line from documentation (payload, PX4 board support, mount holes, power).
3. **Stack matrix** (`config/stack-lock.proposed.json`): PX4 release/commit, ROS 2 distribution, Gazebo version, PX4↔ROS 2 bridge commit, QGroundControl version, candidate VIO package, sensor drivers — each with a documentation URL and date showing the pairing is supported; every entry labelled `proposed`. Write ADR-0007 with alternatives.
4. **Compliance plan** in the envelope: Part 107 path, registration, Remote ID route, indoor-only applicability, site permission, VLOS limits, with [S1]–[S5] and recheck dates.
5. **Reference and containment plan**: accuracy target, camera placement, coverage, synchronization, session check; containment method per airframe/test configuration.
6. **D1 verification plan**: how WO-002 will test each proposed pin (launch, offboard velocity, logging) and the proposed D1 freshness bounds (`evals/D1-exit-tests.json`, status `frozen` only after the owner has not objected and before WO-002 runs them).
7. **Owner decision request**: a short section in the report listing the decisions needed (test space, airframe candidate, companion computer, depth camera) with the reversible defaults; record the owner's answer or deferral in `ledgers/approvals.jsonl` (ET-D0-6).

## Out of scope
Purchasing; installing the flight stack; connecting any hardware; flight; paid services; changes to other repositories.

## Deliverables
The five documents above completed; ADR-0007; report with the owner decision request; `frozen` status events for ET-D1-5 bounds once agreed.

## Steps
1. `make check` green; status WO-001 `ready` → `in_progress`; phase D0 `ready` → `in_progress`.
2. Read the PX4 offboard and external-vision documentation for the proposed release; record URLs and dates in the stack matrix and `docs/SOURCES-D0.md` (new sources with dates; `docs/SOURCES.md` is a shared file and stays unchanged).
3. Price both BOM options; fill compatibility evidence; compute landed totals.
4. Fill the envelope, derive limits, write the compliance and reference/containment sections.
5. Write ADR-0007 and the D1 verification plan; draft `evals/D1-exit-tests.json`.
6. Write the report with the owner decision request. Run the full review (`AGENTS.md §13.9`), open the PR and merge it when `AGENTS.md §4.6` holds. Then ask the owner for the decision.
7. When the owner records a decision or deferral, append it to `ledgers/approvals.jsonl`, append `accepted` for WO-001 with report and commit, `make board`, and continue to WO-002 (software only; no purchase needed).

## Verification
```bash
make check
python tools/check_links.py
python - <<'EOF'
import json; cfg=json.load(open("config/stack-lock.proposed.json")); assert all(v.get("status")=="proposed" and v.get("evidence_url") for v in cfg["flight_stack"].values()), "every pin needs status=proposed and an evidence URL"
EOF
grep -c "unknown" docs/OPERATING_ENVELOPE.md   # each remaining 'unknown' must map to a named owner question in the report
```
Expected: all documents complete; every BOM line sourced and dated; every pin labelled proposed with evidence; the report lists owner decisions with defaults.

## Exit criteria
ET-D0-1 … ET-D0-5 pass on the merged documents; ET-D0-6 passes when the owner's decision or deferral is recorded. Phase D0 `passed` with the report.

## Stop conditions
Missing site information that changes the platform choice (keep both options, ask); any temptation to assume a large outdoor aircraft is safe indoors; any pin that cannot be sourced (leave it `null` with the question, never "latest").

## Report
`reports/WO-001-d0-operating-envelope-and-platform-proposal.md`
