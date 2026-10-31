# WO-009 | Protect accepted work orders and widen the secret scan
**Phase:** D0
**Exit tests advanced:** none; this must finish before WO-001.
**Size:** S
**Prerequisites:** none. Owner instruction of 2026-10-31, recorded in `ledgers/approvals.jsonl`.
**Authorization:** AGENTS §2.1 only
**Files:** `.gitignore`, `tools/status_board.py`, `tools/check_immutable.py`, `tools/scan_secrets.py`, `tests/test_tools.py`, `CHANGES.md`, `VERIFICATION.md`, `ledgers/approvals.jsonl`, `work_orders/`, `docs/STATUS_BOARD.md`, `SHA256SUMS.json`.

Serves `PROGRAM §10`. Both defects came with the starter kit and were recorded in `VERIFICATION.md` during the rename review. The sibling kit ships the same two tools.

## Objective
Stop an accepted work order and its freeze from being reset, and make the secret scan catch the tokens this program is most likely to hold.

## Scope
1. `tools/status_board.py`: refuse a `created` event for any work order that already has a ledger record. `tools/check_immutable.py`: keep the freeze once any `accepted` event exists, so a line appended by hand cannot lift it, and reject replacing a protected file with a symlink.
2. `tools/scan_secrets.py`: add patterns for Hugging Face tokens (`hf_` followed by 30 or more alphanumerics) and RunPod API keys (`rpa_` followed by 30 or more alphanumerics), and scan files with no extension.
3. Tests for both, with token literals built at runtime so the scanner does not flag its own tests.
4. `.gitignore`: return to the broad `*secret*` rule plus `!tools/scan_secrets.py`, keeping `secrets/` and `.secrets*`, on the owner's instruction, because the specific-pattern list left names like `secret_prod.env` trackable. Test that the scanner stays tracked and that `secret_prod.env` is ignored.

## Out of scope
Anything in `contracts/v1/`, `PROGRAM.md` or the `AGENTS.md` core; other scanner patterns; any other status behaviour.

## Deliverables
The two fixes and their tests in commits of their own, logged in `CHANGES.md`. A follow-up commit closes gaps that the review of the first commit found.

## Steps
1. Add the failing tests, then the fixes.
2. Run `make check`, regenerate `SHA256SUMS.json` last, and commit on `wo/WO-006-program-rename` with no amends.

## Verification
```bash
make check
python tools/status_board.py --append --wo WO-007 --event created   # in a scratch copy: must be refused, exit 2
```
Also in a scratch copy: a Hugging Face or RunPod token, in a `.md` file or a file with no extension, must make `python tools/scan_secrets.py --root <copy>` exit 1.

## Exit criteria
No exit test closes here. Accepted when these checks pass on the merged commit.

## Stop conditions
A fix would touch shared bytes, or a scan pattern would flag text that is not a credential and cannot be narrowed.

## Report
`reports/WO-009-status-freeze-and-secret-scan.md`, written at acceptance, once this work order has merged. Until then the fixes are logged in `CHANGES.md`.
