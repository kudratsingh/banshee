# WO-017 — Purchase request for Option A, and the D2 freeze

**Status:** passed
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-017 · **Phase:** D2 (exit tests frozen; not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing here ran on hardware or in the simulator.

## 1. Claim and scope
The owner has one table to approve line by line, in `docs/PURCHASE_REQUEST-2026-11-01.md`, and D2's exit tests are frozen before any D2 result exists. Nothing was bought, D2 did not start, and work stops here until the owner approves lines.

## 2. Purchase request
Prices are dated page readings, not quotes. Line 7, F1 and F2 could not be reread and carry 2026-10-31. Every other line was read on 2026-11-01, and no price differed from the worksheet. Tax, shipping and U1 are estimated. No Covered List status was upgraded.

Holybro's pages kept returning 429, so four were read from its public product records, one every 70 seconds, as its `Retry-After` header asks.

## 3. D2 freeze
`evals/D2-exit-tests.json`, with the sha256 in the `frozen` status events. Statements and evidence stay in `config/phases.json`. Values that read "proposed default" there are frozen at those values.

**Added here, and not in `config/phases.json`, so the owner should know they are my choices:**
- 3 trials for ET-D2-2.
- At least 3 sessions, and a 95% confidence level, for ET-D2-1.
- Every trial must meet its threshold.
- Five items to report in D2 that are not thresholds, carried from earlier reports.

ET-D2-5 names the Pixhawk 6X. If the owner ticks the ARKV6X line, that statement changes by a dated approval before any result exists.

## 4. Records corrected
`work_orders/STATUS.jsonl` was missing WO-015 and WO-016's later events. The tool had refused them because `ready` must come first, and I did not see the refusal. I appended them late, and their notes say so.

## 5. Owner's other instructions
- **SITL VM:** stopped on 2026-11-01 at 15:48 PST and read back as `Stopped`.
- **Caffeinate:** the 14-hour process I started has ended. A `caffeinate -i -t 300` still appears, a child of this Claude Code session. It is the app's own short keep-awake, not one I started, so I left it.

## 6. Verification
`make check` passes. Review: section 7.

## 7. Independent review
Pending at this commit; recorded below when done.

## 8. Retro
My status appends had their output sent to `/dev/null`, which hid the refusals. Check the ledger after appending.
