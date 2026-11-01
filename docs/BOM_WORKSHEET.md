# BOM_WORKSHEET.md — D0 delivered-cost worksheet

**Status: dated price observations from suppliers' pages, not quotes. Nothing was bought and no purchase is authorized (owner, 2026-10-31).** The order would follow D1. Every line was read on 2026-10-31; prices move, so recheck before acting. Bracketed references are in `docs/SOURCES.md` and `docs/SOURCES-D0.md`. Generated from one table, so totals follow the lines.

**Decided by the owner on 2026-10-31 (`ledgers/approvals.jsonl`):** an open outdoor field, an X500 V2, and no Option B. Netting is removed, D3 items are in the main list, and the owner's list of additions is included. An X650-class 6S airframe is the planned D7+ platform (see the end).

## Option A: post-D1 order
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Airframe | Holybro X500 V2 ARF kit: frame, props, 2216 KV920 motors, BLHeli S 20A ESCs, PDB | 1 | 396.71 | 396.71 | [readymaderc.com](https://www.readymaderc.com/products/details/87064-holybro-x500-v2-almost-ready-to-fly-arf-kit) | in stock | 500 mm; about 1 kg payload at 70% throttle on 4S 5000 mAh [D13]; Holybro lists it at $329.00, sold out |
| Autopilot | Holybro Pixhawk 6X, Standard v2A baseboard, PM02D | 1 | 422.99 | 422.99 | [holybro.com](https://holybro.com/products/pixhawk-6x) | in stock | PX4 target `px4_fmu-v6x_default`; three ICM-45686 IMUs; CRSF in the default build; Ethernet; PM02D takes 2S–12S [D49] |
| Autopilot mount | Holybro mounting plate, Pixhawk 6X | 1 | 5.59 | 5.59 | [holybro.com](https://holybro.com/products/standard-baseboard-mounting-plate) | in stock | hole data not on the page; the X500 kit is sold with a 6X, so fit is expected |
| GPS | Holybro M10, 10-pin | 1 | 43.99 | 43.99 | [holybro.com](https://holybro.com/products/m10-gps) | in stock | standard GPS port; Holybro also now lists an M10 V2 |
| Telemetry | Holybro SiK V3 915 MHz 100 mW, pair | 1 | 58.99 | 58.99 | [holybro.com](https://holybro.com/products/sik-telemetry-radio-v3) | in stock | FCC ID 2AP22-HT03-V3 on the store page; licence finding under Compliance in the envelope |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399.00 | 399.00 | [sparkfun.com](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) | backorder | **$399 is NVIDIA's list price** ([FAQ](https://developer.nvidia.com/embedded/faq)); see the note below; 175 g; DC jack 9–20 V [D15] |
| Storage | Sandisk Optimus 5100 500 GB NVMe, M.2 2280 | 1 | 109.99 | 109.99 | [amazon.com](https://www.amazon.com/dp/B0GJSFFLXZ) | in stock | M.2 Key-M 2280 slot, PCIe 3.0 x4 [D51]; working on PCIe 3.0 is inferred |
| Jetson power | Matek BEC12S-PRO, 12 V 5 A | 1 | 18.99 | 18.99 | [progressiverc.com](https://www.progressiverc.com/products/matek-bec12s-pro) | available | 9–55 V in, so it also takes 6S at D7. **Needs at least 14 V in for a stable 12 V: a 4S pack drops below that at 3.5 V per cell.** The Jetson's 9–20 V jack should tolerate this; bench test in D2. Default output is 5.2 V: set 12 V before connecting. A 5.5 × 2.5 mm barrel lead is unpriced |
| TELEM2 cable | Holybro UART cable, JST-GH 6-pin to Dupont | 1 | 2.59 | 2.59 | [holybro.com](https://holybro.com/products/uart-cable-for-pixhawk-flight-controllers) | available | Jetson header pins 8, 9, 10, at 3.3 V [D15]; check the wire map with a meter. A reported JetPack 7 UART1 fault may force Ethernet instead [D52] |
| Jetson mount | Holybro Payload Platform Board V2, as a base for a printed adapter | 1 | 10.59 | 10.59 | [holybro.com](https://holybro.com/products/spare-parts-x500-v2-kit) | available | platform holes are 49 × 58 and 58 × 86 mm, and the dev kit has no bottom holes [D53], so an edge-capture bracket is printed. Fit is resolved in D2 |
| Depth camera | Luxonis OAK-D Pro | 1 | 429.00 | 429.00 | [shop.luxonis.com](https://shop.luxonis.com/products/oak-d-pro) | add-to-cart shown | 91 g per Luxonis; global-shutter stereo, BNO086 IMU [D21]; **sunlight performance is unresolved** [D54] |
| Camera mount | Holybro Depth Camera Mount | 1 | 10.59 | 10.59 | [holybro.com](https://holybro.com/products/depth-camera-mount) | conflicting: one page available, one sold out | names RealSense and Structure Core, not OAK; fit unverified |
| Batteries | Tattu 5200 mAh 4S 35C XT60 | 3 | 62.99 | 188.97 | [readymaderc.com](https://www.readymaderc.com/products/details/tattu-5200mah-4s1p-35c-xt60) | in stock; ground shipping only | 4S as Holybro recommends; 5200 mAh is the PX4 kit page's figure |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | 1–6S LiPo; 100 W AC, 300 W DC per the seller |
| LiPo bag | TBS LiPo bag | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging |
| Fire-safe box | Bat-Safe | 1 | 89.99 | 89.99 | [997rcraceway.com](https://997rcraceway.com/products/bafbatsafe-bat-safe-lipo-battery-charging-safe-box) | only 1 left | field storage and transport; fire rating not checked |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | independent takeover link; batteries not included |
| RC receiver | RadioMaster RP1 V2 ELRS | 1 | 21.15 | 21.15 | [readymaderc.com](https://www.readymaderc.com/products/details/85669-radiomaster-rp1-2-4ghz-expresslrs-elrs-nano-receiver-v2) | in stock | ExpressLRS over CRSF, in the 6X default build; set `RC_CRSF_PRT_CFG` [D49] |
| Spare props | Master Airscrew 10 × 4.5 set | 2 | 11.64 | 23.28 | [readymaderc.com](https://www.readymaderc.com/products/details/85904-master-airscrew-mr-series-10x4-5-prop-set-x2-black) | in stock | same size; fit on the motor and retainer unverified; Holybro's spares are sold out |
| Remote ID | Dronetag Beacon | 1 | 149.00 | 149.00 | [shop.dronetag.com](https://shop.dronetag.com/products/21-dronetag-beacon.html) | in stock | standalone broadcast module; 17 g. The generation is not on the page. DoC RID000001121 for gen 2 per a third-party mirror [D28] |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | `docs/REFERENCE_AND_SENSING.md`; rolling shutter is inferred |
| Landing pad | Hoodman weighted pad, 3 ft | 1 | 89.99 | 89.99 | [hoodmanusa.com](https://hoodmanusa.com/collections/drone-mapping-accessories-1/products/hoodman-weighted-uav-drone-landing-pad-line-3-ft) | available | outdoor takeoff point |
| Hi-vis vests | Uline Class 2, for operator and spotter | 2 | 8.00 | 16.00 | [uline.com](https://www.uline.com/Product/Detail/S-12517O-L/High-Visibility-Vests/Class-2-Standard-Hi-Vis-Safety-Vest-Orange-L-XL) | in stock | crew identification |
| Part 107 knowledge test | FAA initial exam | 1 | 175.00 | 175.00 | [faa.gov](https://www.faa.gov/faq/how-much-does-it-cost-get-remote-pilot-certificate) | — | “approximately $175” [S2]; personal; planning reference, not a transaction here |
| Part 107 registration | X500, three years | 1 | 5.00 | 5.00 | [faa.gov](https://www.faa.gov/uas/getting_started/register_drone) | — | $5 per drone [S3]; the X650 at D7 is likely a new registration [D55] |

| Landed total (USD) | |
|---:|---:|
| Goods, summed from the lines above | 2,923.57 |
| Fees | 180.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 263.12 |
| Shipping, *estimated*: a flat allowance, because the suppliers state no figure for these orders | 60.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 292.36 |
| **Planning total** | **3,719.05** |

**Confirmed present, as the owner asked:** LiPo charger, Part 107 exam fee, FAA registration, Remote ID module (the X500 has none built in).

**Against the owner's $1,900–2,300 range:** about $1,419 above the top.

**Jetson price.** The owner's instruction was NVIDIA list price at $249 from a listed partner, not the $399 backorder listing. **That cannot be met: $399 is the list price.** NVIDIA's [FAQ](https://developer.nvidia.com/embedded/faq) gives $399, press reports the rise from $249 in [July 2026](https://hwbusters.com/news/nvidia-jetson-prices-jump-up-to-101-the-249-orin-nano-super-is-now-399/), and SparkFun states "$399 retail price". No page that loaded shows $249. In stock, [Seeed](https://www.seeedstudio.com/NVIDIAr-Jetson-Orintm-Nano-Developer-Kit-p-5617.html) lists $450.30 and Amazon sellers start at $472.90. [SabrePC](https://www.sabrepc.com/945-13766-0000-000-NVIDIA-S116360058) lists $283.86, out of stock. NVIDIA's store, Arrow, Mouser, Micro Center, Newegg and B&H did not load, so a lower price there cannot be excluded; check them before ordering. At $249 this total would be $3,541. A successor, the Orin Nano 2, is reported for the first half of 2027 ([one source](https://jetsonhacks.com/2026/08/26/jetsonhacks-august-2026-newsletter/)), after this order.

**Not in the total: tariffs.** $555.33 of these goods comes from Holybro directly, whose store says orders ship from Hong Kong and the buyer pays US duties at an unstated rate. A superseded notice there said "up to 69%", a worst case of about $383. The contingency does not cover that, because it is assigned to unpriced items. A US reseller avoids this but costs more; the 6X set's reseller price was not read.

**Ways to reduce it (planning total after each change, *estimated*):**
| Change | Total | Cost of the change |
|---|---:|---|
| Holybro restocks the X500 ARF at $329.00 | 3,638 | wait; no date is published |
| [RadioMaster Pocket ELRS](https://www.readymaderc.com/products/details/85660-radiomaster-pocket-radio-controller-expresslrs-elrs-2-4ghz-charcoal-mode-2) at $76.99 instead of the TX16S | 3,543 | smaller radio, still an independent link; its FCC status was not read |
| Pixhawk 6C instead of 6X | 3,480 | not the owner's lean; needs a custom build for CRSF, and has no Ethernet |

## Flight controller comparison
| | Pixhawk 6C | Pixhawk 6X | ARKV6X + ARK carrier |
|---|---|---|---|
| Set priced | Aluminium, PM02 V3, $227.99 at Holybro (plastic set sold out there; $275.15 at RMRC) | Standard v2A, PM02D, $422.99 | [Bundle](https://arkelectron.com/product/arkv6x-bundle/) $750 + [power module](https://arkelectron.com/product/ark-pab-power-module/) $100 |
| With M10, $43.99 | $271.98 | $466.98 | $893.99 |
| Parts against the 6C at Holybro, $271.98 | — | +$195.00 | **+$622.01** |
| Parts against the plan the owner reviewed, RMRC, $327.94 | — | +$139.04 | **+$566.05** |
| Within the owner's $300, on parts? | — | yes | **no, on either basis** |
| FCC Covered List | candidate: SDoC 2022-07-19, vendor-hosted | candidate: SDoC 2022-07-19; may not cover Rev 8 | module exempt if still listed: Blue Framework since 2025-02-15, last readable 2026-05-25 [D60], until 2028-01-01. **The carrier and power module have no Framework row** |
| Stated origin | CN, per reseller RMRC, not Holybro | CN on RMRC's 6X Pro and module listings, not the priced set; Holybro states none | USA, a vendor claim, not a domestic-end-product finding |
| PX4 target at v1.17.0 | `px4_fmu-v6c_default` | `px4_fmu-v6x_default` | `ark_fmu-v6x_default` |
| CRSF in the default build | **no, custom build needed** | yes; 6,160 bytes of flash free | yes; 41,180 bytes free |
| IMUs | 2 | 3 | 3 |
| X500 mounting | sold as an X500 kit | sold as an X500 kit | none documented; hole pattern unread |
| 6S 650-class reuse at D7 | documented for the X650; PM02 V3 takes 2S–12S | documented for the X650; PM02D takes 2S–12S | in range (5.8–33 V), not documented on the X650 |
| Ethernet | no | yes | yes |

**Planning default: Pixhawk 6X, target `px4_fmu-v6x_default`, with 6X or ARKV6X decided by the owner at purchase, after the Covered List check for each line,** as the owner's stated lean to standardize on FMUv6X and the Pixhawk Autopilot Bus. The owner's preference for ARKV6X applied only within about $300 of the 6C plan, and the ARK stack is well over that. **"Interchangeable" holds at the hardware level only:** PX4 lists these as interchangeable carriers and modules, but the firmware differs (board id 53 and 57), and so do board defaults and PWM channel count (9 and 8), so a swap means a reflash and recalibration. No documented test of that swap was found.

**One route does fit $300, and the owner may prefer it:** an ARKV6X module ($400) on a [Holybro Mini baseboard](https://holybro.com/products/pixhawk-baseboards) ($95) with PM02D ($24.99) and M10, $563.98, which is +$292.00 or +$236.04 on the same two bases. It was not chosen, because the combination is undocumented, the baseboard is a foreign-made Holybro part with no separate SDoC listed, and Mini fit on the X500 is unread. It remains available later, by swapping the module.

## FCC Covered List check, per line
**A planning check, not legal advice.** The action is [DA 25-1086](https://docs.fcc.gov/public/attachments/DA-25-1086A1.pdf), 2025-12-22. It bars *new* FCC equipment authorizations for foreign-produced UAS and critical components. Previously authorized models "can continue to be imported, sold, and used" [D50]. What the sources add to the owner's summary:
- **The list is open-ended and wider than stated:** "includes but is not limited to" data transmission devices, communications systems, flight controllers, ground control stations and controllers, navigation systems, **sensors and cameras**, batteries and battery management systems, motors, and associated software.
- **The test is primary use:** "designed and intended primarily for use in UAS". So a multi-use camera is outside it. This is FAQ guidance, and FCC 26-50 only proposes codifying it.
- **Frames and general-purpose computers are not addressed by any FCC text read,** so "not a critical component" is reasoning, not an FCC statement.
- **The owner's three categories do not cover everything.** A battery or motor is named but has no grant to show, so it fits none of them (the FAQ: no device newly requires authorization). The list also excepts Conditional Approvals and Toy Drones.
- **Exemptions expire:** Blue UAS and domestic end products until 2028-01-01. "Blue UAS" includes the Framework list ([DA 26-761](https://docs.fcc.gov/public/attachments/DA-26-761A1.pdf)). The live list could not be read; the newest row data is 2026-05-25 [D60].
- **Grandfathering is not permanent:** 47 CFR 2.939(e) lets the FCC stop import and marketing of authorized covered equipment. It has done so for 2024-or-earlier entries, but [DA 26-635](https://docs.fcc.gov/public/attachments/DA-26-635A1.pdf) excludes the UAS entry. Proposals for UAS (DA 26-742, DA 26-758) are pending and would leave already-bought equipment usable. **So re-check before buying.**
- **"US-made" does not settle it:** place of production governs, with no content threshold stated, and FCC 26-50 proposes that "produced in a foreign country" mean failing the domestic end product test.
- **No FAQ addresses a self-built drone.** How this applies to parts assembled by an owner is not stated in anything read.

| Line | Status | Evidence, read 2026-10-31 |
|---|---|---|
| Airframe | **FLAG** | See the three rows below this table: the frame and props, the motors, and the ESCs differ. |
| Autopilot | Grandfathered candidate | [FCC SDoC](https://docs.holybro.com/company/certification-iso-fcc-ce-rohs-etc) issued 2022-07-19. Not verified complete: lab-issued, no US responsible party named, and valid only for the configuration described, which may predate Rev 8. Ask the seller. |
| Autopilot mount | Not a critical component (reasoning) | Passive part with no radio. No FCC text names it; inferred from silence. |
| GPS | Grandfathered candidate | [FCC SDoC](https://docs.holybro.com/company/certification-iso-fcc-ce-rohs-etc) dated 2023-11-20, same limits as the autopilot. Navigation systems are a named component. Alternative: [ARK SAM GPS](https://arkelectron.com/product/ark-sam-gps/), $75, Blue Framework listed in the data of 2026-05-25 [D60]. |
| Telemetry | Grandfathered candidate | FCC ID published, and a filing letter names it (2018). **The grant itself could not be read**, so date, rule part and antennas are unverified. Read it before buying: [FCC search](https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm), grantee 2AP22. |
| Companion computer | Not a critical component (reasoning) | General-purpose compute. No FCC text names computers as UAS components; this reasons from the FAQ's primary-use test [D50]. |
| Storage | Not a critical component (reasoning) | General-purpose storage, same reasoning. |
| Jetson power | Not a critical component (reasoning) | Not named, no radio; inferred from silence, and the list is open-ended. US-made alternative: [Pololu D36V50F12](https://www.pololu.com/product/4095), $39.95, 13.3 V minimum input and 4.5 A at 36 V, so less suited to 4S. |
| TELEM2 cable | Not a critical component (reasoning) | Passive cable, no radio; inferred from silence. |
| Jetson mount | Not a critical component (reasoning) | Passive part; inferred from silence. |
| Depth camera | Not a critical component (reasoning) | A multi-use robotics camera fits the FAQ's example [D50], inferred; the FCC does not name it. No FCC ID was read. Its IR dot projector is not obviously LiDAR under proposal DA 26-758, which is not adopted. |
| Camera mount | Not a critical component (reasoning) | Passive part; inferred from silence. |
| Batteries | **FLAG** | Batteries are a named component, and Tattu markets these for drones. A battery has no grant to show. The FAQ says generic batteries are unlikely to have needed authorization, and nothing newly requires it [D50]. **Fits none of the three categories.** Proposed: keep. Alternative: MaxAmps says assembled in the USA; no 4S 5000 price could be read. |
| Charger | Not a critical component (reasoning) | Ground equipment, not named; inferred from silence. |
| LiPo bag | Not a critical component (reasoning) | Not a UAS component. |
| Fire-safe box | Not a critical component (reasoning) | Not a UAS component. |
| RC transmitter | **FLAG** | FCC ID 2BUHG-TX16SMK3 is in the manual. **Grant date unread**, and reviews start January 2026, so a grant before 2025-12-22 cannot be assumed. Controllers are a named component. Read the grant before buying. Candidate alternative: the [RadioMaster Pocket](https://www.readymaderc.com/products/details/85660-radiomaster-pocket-radio-controller-expresslrs-elrs-2-4ghz-charcoal-mode-2), with its grant date as the check; its status was not read. No exempt or US-made controller was priced. |
| RC receiver | **FLAG** | **No FCC ID found**, and it transmits telemetry. Fits none of the three on this evidence. Alternative: [ModalAI M0184](https://www.modalai.com/products/m0184), $159.99, Blue Framework per the vendor; pairing with the TX16S is untested. |
| Spare props | Not a critical component (reasoning) | Passive, not named; inferred from silence. |
| Remote ID | **FLAG** | A data transmission device. **No FCC ID was read.** FAA list could not be read automatically. Check both before buying. Alternatives: [BlueMark db120](https://download.bluemark.io/db120.pdf), FAA acceptance stated by the vendor; Pierce Aerospace B1, reported on the Blue Framework, no price found. Holybro's module is not an option: it is not for DIY users and has no serial. |
| Outside-in reference | Not a critical component (reasoning) | A video-call webcam fits the FAQ's example; inferred. |
| Landing pad | Not a critical component (reasoning) | Not a UAS component. |
| Hi-vis vests | Not a critical component (reasoning) | Not a UAS component. |

The airframe line splits as follows:
| Part of the X500 ARF | Status | Evidence |
|---|---|---|
| Frame, props | Not a critical component (reasoning) | Not named; inferred from silence, and the list is open-ended |
| Motors | **FLAG** | Named, and no grant is possible for a passive motor, so it fits none of the three. The owner said to keep them. No priced US-made 2216-class motor was found: KDE's nearest is "manufactured in China", and Vertiq publishes no price here |
| ESCs | **FLAG** | Not named, but the list is open-ended, and no grant or SDoC was found. Alternative: [ARK 4IN1 ESC](https://arkelectron.com/product/ark-4in1-esc/), $218.50, Blue Framework per the vendor; fit unverified |

**Grant dates could not be read for any part:** the FCC's search and its mirrors returned 403 to automated reads. The owner's assistant will check the [FCC search](https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm) for grantees 2AP22 and 2BUHG, the [FAA list](https://uasdoc.faa.gov/listDocs) and Jetson partner pricing before the purchase decision.

## Not priced, covered by contingency
Radio cells (18650), XT60 charge lead, 5.5 × 2.5 mm barrel lead, printed bracket material, tag box and its standoff, reference tripods and ground stakes, tape or laser measure, handheld wind meter, handheld radios for operator and spotter. Spare arms have no in-stock source; a spare [frame kit](https://www.readymaderc.com/products/details/87065-holybro-x500-frame-kit) is $161.14. Field charging power and a table are left out: charge at home for the first outings ([EcoFlow RIVER 3 Plus](https://us.ecoflow.com/products/river-3-plus-portable-power-station), $299.00, if that proves too few).

## D7+ platform (planned, not in this order)
An X650-class 6S airframe, with the same autopilot and stack. Reference: [Holybro X650 kits](https://holybro.com/products/x650-kits), ARF $899.00 in stock at Holybro ($1,150.12 at RMRC), 650 mm, 6S, about 3.5 kg payload with a 5200 mAh battery, T-Motor MN4014 motors and Tekko32 45 A ESCs. The swap is frame, motors, ESCs and batteries, plus paperwork: a Remote ID serial can be on only one registration at a time, and the X650 is likely a new $5 registration. PM02D's 30 A continuous wire rating against the X650's current is unread, and those motors and ESCs need their own Covered List check at that time.
