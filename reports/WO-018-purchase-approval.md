# WO-018 — Purchase approval recorded, and the buy list

**Status:** passed, with four owner decisions open in the buy list
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-018 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing here ran on hardware or in the simulator.

## 1. Claim and scope
The owner's approval is recorded with their words, and `docs/BUY_LIST-2026-11-01.md` applies it. Nothing is bought; the agent has no account or payment access. No email was sent.

## 2. Findings
- **The sourcing rule cannot be met exactly.** No plain 6X set was found in stock at RMRC or GetFPV, and six small Holybro parts, $69.34, were not found at RMRC or Kilitronic. These are open decisions for the owner.
- **RMRC's SiK page says a licence is required,** against the owner's closure of C2. Both are recorded.
- **F1 is in none of the owner's lists,** and C5 remains open for line 18.

## 3. Limits of the readings
Read directly on 2026-11-01: RMRC pages, and Kilitronic and RadioMaster product records. Not read: GetFPV (403), both fccid.io pages (403), Walmart (bot check), PCPartPicker (403). The NVMe price and Kilitronic's US shipping come from search results of unknown age. Line 7 is therefore estimated.

## 4. Verification
`make check` passes. CI only under the owner's review rule; this is not a milestone exit test.

## 5. Retro
A sourcing rule depends on stock, so check it against stock before writing a list that relies on it.
