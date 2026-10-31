# BOM_WORKSHEET.md — D0 delivered-cost worksheet

**Status: candidate options with dated price observations, not quotes and not a purchase recommendation.** WO-001 completes the table with supplier quotes (URL + date), landed cost, and compatibility evidence for at least two airframe options (ET-D0-2). Prices below were observed 2026-10-30 ([H5]–[H7] in `docs/SOURCES.md`) and move weekly. **Nothing here authorizes a purchase.**

## Option A — 500 mm class kit (garage / warehouse / field)

| Item | Candidate | Qty | Observed unit USD | Source / date | Compatibility evidence needed |
|---|---|---:|---:|---|---|
| Airframe + autopilot + GPS + telemetry | Holybro X500 V2 PX4 Dev Kit, Pixhawk 6C, M10 GPS, 915 MHz SiK | 1 | 609 (Holybro; sold out 2026-10-30); 540–950 at dealers | [H5] | PX4 build for FMUv6C; 1.5 kg payload; ~18 min hover @ 5000 mAh |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399 (was 249 before July 2026) | [H6] | mount holes on the X500 platform board; power budget; defer to D7 if laptop-first |
| Depth / stereo camera | OAK-D Pro **or** Intel RealSense D435i | 1 | 350–400 | owner's plan, 2026-10-30 | driver + timestamping with the chosen VIO; Holybro depth-camera mount |
| Batteries + charger | 3 × 4S 5000 mAh 20C+ XT60; balance charger; LiPo bag | 1 set | 230–280 | owner's plan | 4S matches the kit's ESCs; reserve policy |
| RC link | RadioMaster TX16S (or Pocket) + receiver | 1 | 150–220 | owner's plan | independent takeover path |
| Containment | prop guards; net enclosure or tether rig per D0 decision | 1 | 60–150 | owner's plan | airframe-specific |
| Outside-in reference | 2 webcams, wall mounts, printed tag array, tape/laser measure | 1 set | 100–200 | `docs/REFERENCE_AND_SENSING.md` | coverage of the test volume |
| Spares | props, arms, screws, XT30/XT60 connectors | 1 set | 60–100 | — | — |
| Remote ID | route-dependent (built-in module vs broadcast module vs FRIA) | 1 | 0–150 | [S4] | FAA-accepted route |
| Part 107 knowledge test | FAA initial exam | 1 | ≈175 | [S2] | personal; not a transaction here |
| Part 107 registration | per aircraft, 3 years | 1 | 5 | [S3] | after purchase |
| Shipping / tax / contingency | quote-dependent | — | — | — | no double counting |
| **Planning total** | | | **≈ 1,900–2,300** | owner's plan | before quotes |

## Option B — 3–5 inch guarded indoor frame (room-scale test space)

| Item | Candidate | Qty | Observed unit USD | Source / date | Compatibility evidence needed |
|---|---|---:|---:|---|---|
| Frame + motors + ESC + guards | 3–5 inch FPV frame with full prop guards (choose in WO-001) | 1 | **unknown** — quote in WO-001 | — | payload for camera + companion; PX4-compatible FC |
| Flight controller | PX4-compatible small FC (Pixhawk 6C Mini class or FMUv6 FPV board) | 1 | unknown | — | PX4 support for the board |
| Companion compute | laptop-first; small SBC later | — | — | — | weight budget |
| Camera for VIO | small global-shutter camera + IMU or integrated module | 1 | unknown | — | VIO suitability |
| Batteries, RC link, reference, spares, compliance | as Option A, smaller batteries | — | — | — | — |
| **Planning total** | | | **unknown** | — | WO-001 prices it |

## Rules for completing this worksheet
- Every line: supplier URL, date observed, unit price, shipping/tax estimate, and the compatibility evidence (a documentation page, not a forum post).
- Record totals per option; present both to the owner; the owner decides (ET-D0-6).
- Exam and registration lines are planning references, not transactions.
- Do not assume the planning range covers the final configuration.
