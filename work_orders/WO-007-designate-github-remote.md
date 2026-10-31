# WO-007 | Designate the private GitHub remote and create the repository
**Phase:** D0
**Exit tests advanced:** none; this is repository setup ahead of WO-001.
**Size:** S
**Prerequisites:** owner request dated 2026-10-31, recorded in `ledgers/approvals.jsonl`.
**Authorization:** AGENTS §2.2, on the owner's request. It does not authorize public visibility, spending, a purchase or any hardware action.
**Files:** `config/repo.json`, `docs/adr/ADR-0006-github-remote.md`, `ledgers/approvals.jsonl`, `work_orders/`, `docs/STATUS_BOARD.md`, `SHA256SUMS.json`.

Serves `PROGRAM §12` decision 7, for this repository only.

## Objective
Give this repository the private remote the owner asked for, following `docs/WORKFLOW.md §8`.

## Scope
Set `config/repo.json`; create `kudratsingh/banshee` as a private repository; push `main` and the open work-order branch; request the protection in `docs/WORKFLOW.md §8`.

## Out of scope
Any remote for the `vishwaroop` project; public visibility; collaborators, secrets or tokens; merging WO-006.

## Deliverables
The designated configuration, ADR-0006, the private repository, and an approval record.

## Steps
1. Record the owner's request, then set `config/repo.json`.
2. Merge to `main` after `make check` passes.
3. Create the repository, push, and request protection.
4. Confirm visibility and CI results.

## Verification
```bash
make check
gh repo view kudratsingh/banshee --json visibility,defaultBranchRef
gh run list --repo kudratsingh/banshee
```
Expected: `make check` exits 0, visibility is `PRIVATE`, the default branch is `main`, and the CPU tier passes on the pushed commits.

## Exit criteria
No exit test closes here. Accepted when the verification above is recorded.

## Stop conditions
The name is taken; the repository would not be private; a step would need spending or a permission change beyond this scope.

## Report
`VERIFICATION.md` on the rename branch records the result, because `test_no_fixture_claims_in_reports` blocks files under `reports/` until WO-008.
