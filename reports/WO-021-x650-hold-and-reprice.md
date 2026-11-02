# WO-021 — X650 decision and hold recorded; list re-priced

**Status:** passed, with six owner decisions listed in the re-priced list
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-021 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing here ran on hardware or in the simulator.

## 1. Claim and scope
The owner's decision and purchase hold are in `ledgers/approvals.jsonl`. `docs/BUY_LIST-REPRICED-2026-11-01.md` holds one table and a planning total of $7,205.93 (estimated). ADR-0007 records the X500 as superseded. Nothing is bought. The envelope, standoffs and D2 tests are WO-022.

## 2. Findings
- **The baseboard does not support the planned stack.** Holybro lists JetPack 5.1.2–6.0 and 6.2.2; ADR-0007 plans Isaac ROS 4.6.0 on JetPack 7.2, Ubuntu 24.04 and Jazzy. An owner decision.
- **The bundle already includes** a 512 GB SSD, the 12 A UBEC, PM02D, PDB and cables, so the UBEC needs no line and the NVMe line is probably unneeded.
- **A US reseller has the bundle,** at $2,399 with a case. Holybro direct is about $3,134 with estimated duty.
- **No 6S 10 Ah LiPo with XT60 was found in US stock.** The Bat-Safe is rated for one such pack, not three. Holybro's X650 spares are all sold out. ARK Flow MR and RP3 V2 are on backorder.
- **Fisheye:** BasaltVIO's source handles Kannala-Brandt and pinhole-radtan; Isaac ROS's current docs accept `fisheye`. The 3.2 list is not confirmed. Not run.
- **C2:** the correction was recorded in WO-020. The owner's repeat is recorded as a confirmation, and ADR-0007's telemetry item now points at it.

## 3. Limits of the readings
Read directly on 2026-11-01: Holybro, Kilitronic and Pyrodrone product records; RMRC and RaceDayQuads search or product pages; ARK; T-Motor; Luxonis through a page summariser. Not read: GetFPV (403), Arrow, grant databases, Holybro's certification attachments. Duty rates are from secondary sources. "Tier B" is recorded in the owner's words; its definition was not found in the repository or this session.

## 4. Verification
`make check` passes. CI only under the owner's review rule; the D2 exit-test change is in WO-022 with its full review.

## 5. Retro
Compare a bundle's package list with the lines it replaces before pricing separately. Two requested lines were already in the box.
