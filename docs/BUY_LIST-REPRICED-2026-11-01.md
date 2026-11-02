# Re-priced buy list — X650 platform, 2026-11-01

**Superseded on 2026-11-02 by `docs/BUY_LIST-FINAL-2026-11-02.md`,** which applies the owner's decisions of that date. This page stays as the record of 2026-11-01.

**Status: ALL PURCHASES ON HOLD by the owner's decision of 2026-11-01 (`ledgers/approvals.jsonl`), until the owner approves this list line by line.** Earlier line approvals in `docs/BUY_LIST-2026-11-01.md` are held with it. The owner places the orders; the agent places none. Prices are dated page readings, not quotes. "Read" means read by the agent on 2026-11-01, unless the row says otherwise.

## Decisions to make before ordering
1. **Bundle software: the baseboard does not support the planned stack.** Holybro's [flashing guide](https://docs.holybro.com/autopilot/pixhawk-baseboards/pixhawk-jetson-baseboard/flashing-guide.md) says the board "only supports Jetpack versions 5.1.2 to 6.0 and 6.2.2". [PX4's page](https://docs.px4.io/main/en/companion_computer/holybro_pixhawk_jetson_baseboard) says it was tested with JetPack 6.0, Ubuntu 22.04 and ROS 2 Humble. ADR-0007 plans Ubuntu 24.04, Jazzy and Isaac ROS Visual SLAM 4.6.0, which needs JetPack 7.2. **Recommended: buy the bundle and run JetPack 6.2.2, Ubuntu 22.04, Humble and Isaac ROS 3.2 on the Jetson.** ADR-0007 already names Humble as its fallback, and [Isaac ROS 3.2](https://nvidia-isaac-ros.github.io/v/release-3.2/getting_started/index.html) lists JetPack 6.1 and 6.2 with Humble. The cost: Humble's support ends in May 2027, and D1's results were on Jazzy, so the node needs re-verifying on Humble before it commands anything.
2. **Bundle seller.** Not Holybro only: Kilitronic has it. **Recommended: Kilitronic, $2,399,** even though it sells only the with-case version. Holybro's no-case version is $2,279 plus an estimated $854.63 duty, about $3,134 (see Duty). Check that the case still fits the X650's baseboard mounting holes; the case's fit is unread.
3. **NVMe, line 7: probably not needed.** The bundle includes a 512 GB NVMe SSD; Kilitronic names a Samsung PM9B1. The line is in the total as you specified. **Dropping it saves $109.00** with tax. Kilitronic's listing also includes a Wi-Fi module and an IMX219-200 camera.
4. **12 A UBEC: already in the bundle.** Holybro and Kilitronic both list "UBEC 12A (3-14S)" in the package, with the PM02D, PDB and cables. So there is no separate line. Line 8, the Matek BEC, loses its job and is dropped from the total, unless you want it as a spare.
5. **Packs: no 6S 10 Ah LiPo with XT60 was found in US stock.** The total uses Tattu 30C with EC5, in stock at RMRC, which needs EC5-to-XT60 adapters or a re-termination rated for the current. In-stock XT60 packs at this size are Li-ion, not LiPo: [Lumenier NAV](https://www.racedayquads.com/products/lumenier-nav-10000mah-6s-21700-lithium-ion-battery-xt60) and STRIX Power Stix, both $149.99, and their current ratings are unread. XT90 LiPo: [Lumenier 25C](https://www.racedayquads.com/products/lumenier-10000mah-6s-25c-lipo-battery-xt90), $251.49.
6. **Bat-Safe holds one of these packs, not three.** Its [listing](https://997rcraceway.com/products/bafbatsafe-bat-safe-lipo-battery-charging-safe-box) rates it for "two 6S 5000mAh (222Wh)", and one 6S 10 Ah pack is 222 Wh. It can guard the pack on charge. Storing three, 666 Wh, needs more boxes; the envelope's rule to store packs in the box cannot be met with one. It is kept as you said. **A second and third box are not in the total.**

## The list
| Line | Replaces | Seller | Item | Qty | Unit USD | Line USD | Stock | Date read | FCC Covered List status |
|---:|---|---|---|---:|---:|---:|---|---|---|
| 1 | X500 ARF | [Kilitronic](https://kilitronic.com/products/x650-kits) | Holybro X650 ARF, SKU 30179 | 1 | 999.00 | 999.00 | available | 11-01 | Frame and props: not a critical component (reasoning). Motors, ESCs: **FLAG** |
| 2 | 2, 3, 6, 9, 10 | [Kilitronic](https://kilitronic.com/products/pixhawk-jetson-baseboard) | Pixhawk Jetson Baseboard Bundle: 6X (ICM-45686), Orin NX 16 GB, with case, SKU 20340 | 1 | 2,399.00 | 2,399.00 | available | 11-01 | **FLAG**, parts below |
| 11 | OAK-D Pro | [Luxonis](https://shop.luxonis.com/products/oak-d-pro-w) | OAK-D Pro W, fixed-focus RGB, SKU A00573 | 1 | 529.00 | 529.00 | Add to Cart; no stock text | 11-01 | Not a critical component (reasoning); no FCC ID read |
| 28 | new | [ARK Electronics](https://arkelectron.com/product/ark-flow-mr/) | ARK Flow MR, DroneCAN | 1 | 350.00 | 350.00 | **On Backorder** | 11-01 | Exempt candidate: vendor states made in the USA |
| 13 | 4S packs | [RMRC](https://www.readymaderc.com/search?q=6s+10000mah) | Tattu 22.2 V 30C 6S 10000 mAh, **EC5** | 3 | 216.99 | 650.97 | In Stock | 11-01 | **FLAG**: batteries are named; no grant possible |
| 14 | M6AC | [RaceDayQuads](https://www.racedayquads.com/products/toolkitrc-m6dac-pro-v2-800w-16a-1-6s-ac-dc-dual-channel-charger-xt60) | ToolkitRC M6DAC Pro V2, AC input max 330 W | 1 | 129.99 | 129.99 | In stock | 11-01 | Not a UAS component (reasoning) |
| 16 | unchanged | [997 RC](https://997rcraceway.com/products/bafbatsafe-bat-safe-lipo-battery-charging-safe-box) | Bat-Safe | 1 | 89.99 | 89.99 | "Only 1 left!" at the earlier read | 11-01 | Not a UAS component (reasoning) |
| 15 | unchanged | [RMRC](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | TBS LiPo bag; fit with these packs unread | 1 | 7.61 | 7.61 | In Stock | 11-01 | Not a UAS component (reasoning) |
| 29 | 20, 21 | [T-Motor](https://store.tmotor.com/product/mn4014-kv330-motor-navigator-type.html) | MN4014 KV330 spare, direct import; CW and CCW fit unverified | 2 | 96.90 | 193.80 | Add to Cart; no stock text | 11-01 | **FLAG**: motors are named; no grant possible |
| 30 | 19, 27 | [Holybro](https://holybro.com/products/spare-parts-x650-kit) | Propeller 1555, 1 pair, SKU 520095 | 2 | 12.59 | 25.18 | **Sold out**; no other source found | 11-01 | Not a critical component (reasoning) |
| 4 | not mentioned; kept | [RMRC](https://www.readymaderc.com/products/details/86930-holybro-m10-gps-with-standard-10-pin-connector) | Holybro M10 GPS | 1 | 52.79 | 52.79 | In Stock | 11-01 | Grandfathered candidate: SDoC 2023-11-20 |
| 12 | not mentioned; kept | [Holybro](https://holybro.com/products/depth-camera-mount) | Depth Camera Mount; made for RealSense, OAK-D Pro W fit unverified | 1 | 10.59 | 10.59 | available on its own page | 11-01 | Not a critical component (reasoning) |
| 17 | unchanged | GetFPV | RadioMaster TX16S MKII ELRS, HP0157.0020 | 1 | 279.49 | 279.49 | In stock, the owner's reading | 11-01, owner | Grandfathered: 2A337-TX16S, grant 2022-06-22, the owner's reading |
| 18 | unchanged | [RMRC](https://www.readymaderc.com/search?q=radiomaster+rp3) | RadioMaster RP3 V2 | 1 | 22.96 | 22.96 | **Backorder** | 11-01 | Grandfathered: 2A337-HP-157, grant 2023-04-12, the owner's reading |
| 23 | unchanged | [Logitech](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | C920s | 2 | 69.99 | 139.98 | In stock | 11-01 | Not a critical component (reasoning) |
| 7 | as specified | B&H, Amazon or Best Buy | 500 GB NVMe, 2242 or 2280; **decision 3** | 1 | 100.00 | 100.00 | Not read; ceiling | — | Not a critical component (reasoning) |

Dropped from the list: lines 2, 3, 6, 9, 10 (bundle); 5 (withdrawn); 8 (decision 4); 19, 20, 21, 27 (spares above).

## Total
| | USD | Label |
|---|---:|---|
| Goods | 5,980.35 | read from pages or the owner's reading; line 7 at its ceiling |
| Sales tax, assumed 9% of goods | 538.23 | estimated |
| Duty on direct imports: lines 12, 29, 30, $229.57 at 37.5% | 86.09 | estimated; see Duty |
| Shipping, flat allowance | 120.00 | estimated, doubled from $60: 11 sellers, and LiPo ships as hazmat |
| U1, your ceiling | 306.26 | ceiling, not a price |
| F1, Part 107 test | 175.00 | about $175; FAA page of 2026-10-31 |
| **Planning total** | **7,205.93** | |

That is $3,590.74 over the earlier $3,615.19, and $4,905.93 over the top of the $1,900–2,300 range.

| Ways it changes | USD |
|---|---:|
| Drop the NVMe (decision 3) | −109.00 |
| X650 ARF from Holybro at $899, with estimated duty of $337.13 and tax | +228.13 |
| No-case bundle from Holybro at $2,279, with estimated duty of $854.63, less $10.80 tax | +723.83 |
| Lumenier NAV Li-ion XT60 instead of the Tattu (decision 5) | −219.09 |

**Not in the total, for a D3 approval:** RFD900x-US, $281.21, FCC ID 2ADLE-900X (backorder; read 11-01), lines 22, 24, 25, 26 and F2.

## Duty
**Estimated, from secondary sources; no USTR or CBP notice was read.** China-origin goods: 0% base rate on the assumed HTS 8471 class, plus 25% Section 301, plus the 12.5% Section 301 forced-labor duty in effect since 2026-07-24, for 37.5% ([summary](https://www.tariffstool.com/tariffs-from-china), [schedule](https://gingercontrol.com/blog/section-301-tariff-rates-china)). So $2,279 × 37.5% = **$854.63**, before any broker fee. The classification of a mixed bundle, the exclusions that expire on 2026-11-09, and Holybro's actual shipping origin are not settled here. Kilitronic's $120 premium is cheaper unless the duty is under about 5.3%.

## FCC Covered List check, new lines
**A planning check, not legal advice,** by the method in `docs/BOM_WORKSHEET.md`. FCC notices were searched through DA 26-1154 (2026-10-23): the Blue UAS and domestic-end-product exemptions run to 2028-01-01. DA 26-742, which would bar continued import and marketing of some already-authorized foreign UAS, is a proposal; no final order was found, and it would not stop use of parts already bought. Grant databases return 403 to automated reads, so **no grant date below was read by the agent.**

| Part | Status | Evidence |
|---|---|---|
| X650 frame, props | Not a critical component (reasoning) | Not named; inferred from silence, and the list is open-ended |
| MN4014 motors, kit and spare | **FLAG** | Motors are named. Foreign-produced, and a passive motor can have no grant, so it fits none of the three categories. Same treatment as the X500's motors |
| Tekko32 F4 45A ESCs | **FLAG** | Not named, but the list is open-ended. [Holybro's certification page](https://docs.holybro.com/company/certification-iso-fcc-ce-rohs-etc) has an ESC entry for this model; its attachments were not readable |
| Pixhawk 6X module | Grandfathered candidate | SDoC 2022-07-19, may not cover Rev 8; the bundle's listing says Rev 8. The C1 email asks this |
| Pixhawk Jetson Baseboard | **FLAG** | A flight-controller carrier, primarily for UAS. Holybro's page has an entry with three attachments, not readable, so the date against the 2025-12-22 cutoff is unknown. **Open these on the page before approving line 2** |
| Orin NX, SSD | Not a critical component (reasoning) | General-purpose compute and storage |
| Wi-Fi module; IMX219-200 camera | Not a critical component (reasoning) | General-purpose parts; FCC IDs not read |
| PM02D, UBEC, PDB | Not a critical component (reasoning) | No radio. Not on Holybro's page. The list is open-ended, and "battery management systems" is named |
| OAK-D Pro W | Not a critical component (reasoning) | Cameras are named, but the test is primary use, and this is a general robotics camera. No FCC ID read |
| ARK Flow MR | Exempt candidate | Sensors are named. The vendor states "Made in the USA, NDAA Compliant", but place of production and the domestic end product test decide, and neither was verified |
| 6S packs | **FLAG** | Batteries are named. Foreign-produced, and no grant is possible, so it fits none of the three categories |
| RFD900x-US, at D3 | Grandfathered candidate | 2ADLE-900X, 15.247, the owner's reading. Grant date not on record |

## Fit and mass, from the seller's pages
- **Payload and limit:** kit 2,000 g without battery; 3.1 kg payload with a 1,200 g 10 Ah pack; takeoff limit 6,300 g at 70% throttle ([Holybro](https://holybro.com/products/x650-kits)). The kit's battery recommendation is 6S 5000–12000 mAh with XT60, and it names the Pixhawk Jetson baseboard as a fit.
- **Charger:** 6S 10 A is 252 W at 25.2 V, under the V2's 330 W AC input. It charges one pack at a time at 1C, with the taper making it somewhat over an hour; three packs take over three hours. Its output per channel is 400 W, and the AC-input split between channels is unread.
- **ARK Flow MR:** rangefinder AFBR-S50LX85D, typically to 50 m; flow PAA3905, with PX4's `SENS_FLOW_MAXHGT` of 25 m. [PX4's page](https://docs.px4.io/main/en/dronecan/ark_flow_mr) says it needs an SD card in the flight controller to boot.
- **Holybro's X650 spares are all sold out,** which is why line 29 goes to T-Motor at $96.90 instead of Holybro's $80.

## VIO and the fisheye lens
**Supported on paper by both candidates, not run, and not settled for this unit.** The OAK-D Pro W's stereo pair is global shutter, 150° diagonal [D62].
- **BasaltVIO:** `depthai-core`'s [source](https://raw.githubusercontent.com/luxonis/depthai-core/main/src/basalt/BasaltVIO.cpp) builds Kannala-Brandt 4 from a device's Fisheye calibration and pinhole-radtan from Perspective, and throws on anything else. Luxonis calls its VSLAM host nodes early access.
- **Isaac ROS Visual SLAM:** the current docs accept `pinhole`, `brown5k`, `polynomial` and `fisheye` (k1–k4). The Isaac ROS 3.2 page read says only that `rectified_images` defaults to true, so the distortion list for 3.2, the version the baseboard allows, is **not confirmed**.
- **Open:** a Luxonis forum post shows a Pro W publishing `rational_polynomial` through `depthai-ros`. Which model a given unit's factory calibration reports, and how well it fits at 150°, can only be read from the unit. WO-022 proposes this as a D2 check.
