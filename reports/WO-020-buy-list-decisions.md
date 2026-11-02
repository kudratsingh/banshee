# WO-020 — Buy-list decisions recorded, and the C2 correction

**Status:** passed, with three items open in the buy list
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-020 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing here ran on hardware or in the simulator.

## 1. Claim and scope
Each owner decision has its own record in `ledgers/approvals.jsonl`, with the owner's words. `docs/BUY_LIST-2026-11-01.md` applies them. The planning total is $3,506.19 with a Standard FOV camera, or $3,615.19 with Wide (estimated). Nothing is bought, and no email was sent. Earlier ledger records are unchanged; the C2 correction is a new record.

## 2. Findings
- **Line 11's field of view is blank in the owner's message.** It stays open, and the total shows both.
- **Line 27, Holybro's 1045 props, reads sold out,** on two reads on 2026-11-01. With line 19 dropped, no approved line supplies spare props today. D2 is props-off.
- **The cheapest in-stock NVMe could not be established.** The total carries the $100 cap as a ceiling.
- **The RFD900x-US grant date is not on record.** It is a check for the D3 approval.
- **Line 18 is on backorder, and ET-D2-5 needs it.**
- **Arrow's part number needs checking.** One reseller labels 945-13766-0005-000 as a kit for named non-US regions.

## 3. Limits of the readings
Read directly on 2026-11-01: RMRC search pages (RP3 V2, RFD900x-US, Holybro props), ProgressiveRC, Holybro's product record, and Luxonis's pages through a page summariser.

Not read: GetFPV (403), Arrow (timed out), fccid.io (403), B&H (403), Amazon (503). Best Buy's pages showed no price tied to a listing. FCC IDs, grant dates, rule parts, the test report, GetFPV's price and stock, and Arrow's price and stock are the owner's readings. The agent checked the 15.249 correction only by arithmetic on the owner's figure (calculated).

## 4. Verification
`make check` passes. CI only under the owner's review rule; this is not a milestone exit test.

## 5. Retro
A closure that rests on a page nobody here could read should stay labelled as unverified. The earlier entry did say so, and the owner's own reading of the test report is what caught it.
