# BOM_WORKSHEET.md — D0 delivered-cost worksheet

**Status: dated price observations from suppliers' pages, not quotes and not a purchase recommendation. Nothing was bought.** Every line was read on 2026-10-31; prices move, so recheck before acting. Bracketed references are in `docs/SOURCES.md` and `docs/SOURCES-D0.md`. Generated from one table, so totals follow the lines. **Nothing here authorizes a purchase.**

## Summary
| Option | Planning total (USD) | What it is | Main problem |
|---|---:|---|---|
| A: X500 V2 | 4,018 | 500 mm kit for a garage, warehouse or field | above the owner's planning range |
| B-1: QAV250 + Pixhawk 6C Mini | 2,836 | cheapest room-scale build that can carry the camera and computer | **no verified guards**, so it does not yet meet the option's definition |

**The owner's $1,900–2,300 range does not cover either option as specified.** Option A is about $1,718 above the top of the range, and Option B-1 about $536. The largest differences from the original plan are the net ($707.94 against $60–150 planned), the kit bought piece by piece because it is sold out (see below), and the tax, shipping and contingency the range left out. Ways to bring it down are listed under Option A.

## Option A — 500 mm class kit (garage / warehouse / field)
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Airframe (no autopilot) | Holybro X500 V2 ARF kit | 1 | 396.71 | 396.71 | [readymaderc.com](https://www.readymaderc.com/products/details/87064-holybro-x500-v2-almost-ready-to-fly-arf-kit) | in stock | 500 mm; 2216 KV920 motors, BLHeli S 20A ESCs, 4S [D13]; platform board has holes for companion computers [D13] |
| Autopilot | Holybro Pixhawk 6C, plastic case, PM02 V3 | 1 | 275.15 | 275.15 | [readymaderc.com](https://www.readymaderc.com/products/details/86046-holybro-pixhawk-6c-with-plastic-case-pm02-power-module-no-gps) | in stock | PX4 target `px4_fmu-v6c_default` [D7] |
| GPS | Holybro M10, 10-pin | 1 | 52.79 | 52.79 | [readymaderc.com](https://www.readymaderc.com/products/details/86930-holybro-m10-gps-with-standard-10-pin-connector) | in stock | kit part [D12]; indoor tests do not use it |
| Telemetry | Holybro SiK V3 915 MHz, pair | 1 | 71.98 | 71.98 | [readymaderc.com](https://www.readymaderc.com/products/details/86245-holybro-sik-telemetry-radio-v3-100mw-915mhz-2-pcs) | in stock | seller says an amateur licence is required in the US (owner question Q6) |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399.00 | 399.00 | [sparkfun.com](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) | backorder; page conflicts | 175 g, 9–20 V input [D15]; 4S direct power is not approved by that document; Holybro names Jetson Nano, not Orin Nano, so hole fit is unverified |
| Depth / stereo camera | Luxonis OAK-D Pro | 1 | 429.00 | 429.00 | [shop.luxonis.com](https://shop.luxonis.com/products/oak-d-pro) | add-to-cart shown | 91 g per Luxonis; global-shutter stereo, BNO086 IMU [D21]; driver `depthai_ros_v3` on Jazzy [D20] |
| Camera mount | Holybro Depth Camera Mount | 1 | 10.59 | 10.59 | [holybro.com](https://holybro.com/products/depth-camera-mount) | available | names RealSense and Structure Core, not OAK; fit unverified |
| Batteries | Tattu 5200 mAh 4S 35C XT60 | 3 | 62.99 | 188.97 | [readymaderc.com](https://www.readymaderc.com/products/details/tattu-5200mah-4s1p-35c-xt60) | in stock | 4S as Holybro recommends (2000–5000 mAh); 5200 mAh is the PX4 kit page's figure; ground shipping only |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | 1–6S LiPo; page's wattage figures conflict |
| LiPo bag | TBS LiPo bag, 23 × 30 cm | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging procedure |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | independent takeover link; batteries not included |
| RC receiver | RadioMaster RP1 V2 ELRS | 1 | 21.15 | 21.15 | [readymaderc.com](https://www.readymaderc.com/products/details/85669-radiomaster-rp1-2-4ghz-expresslrs-elrs-nano-receiver-v2) | in stock | PX4 lists ExpressLRS with CRSF as validated [D18], but RC input over CRSF needs a custom firmware build, not `px4_fmu-v6c_default` [D19]; route in ADR-0007 |
| Containment | US Netting drone panel, 10 × 20 ft, 1-3/4 in mesh | 2 | 353.97 | 707.94 | [usnetting.com](https://www.usnetting.com/drone-netting/) | not stated | two panels for the operator bay and any open side; layout in `docs/OPERATING_ENVELOPE.md`; no guards found for the X500; tensile field blank on the page [D39] |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | reach sized in `docs/REFERENCE_AND_SENSING.md`; rolling shutter is inferred, so measure it |
| Spares: props | Holybro 1045 props, 2 pair | 2 | 11.59 | 23.18 | [holybro.com](https://holybro.com/products/spare-parts-x500-v2-kit) | sold out | no in-stock US source found |
| Spares: arms | Holybro carbon fiber arm tube | 2 | 6.59 | 13.18 | [holybro.com](https://holybro.com/products/spare-parts-x500-v2-kit) | sold out | no in-stock US source found |
| Remote ID (outdoor only) | Dronetag Beacon gen 2 | 1 | 149.00 | 149.00 | [shop.dronetag.com](https://shop.dronetag.com/products/21-dronetag-beacon.html) | in stock | DoC RID000001121 per a third-party mirror dated 2026-09-26 [D28]; check the FAA list before buying |
| Part 107 knowledge test (outdoor only) | FAA initial exam | 1 | 175.00 | 175.00 | [faa.gov](https://www.faa.gov/faq/how-much-does-it-cost-get-remote-pilot-certificate) | — | “approximately $175” [S2]; personal; planning reference, not a transaction here |
| Part 107 registration (outdoor only) | per aircraft, three years | 1 | 5.00 | 5.00 | [faa.gov](https://www.faa.gov/uas/getting_started/register_drone) | — | $5 per drone [S3]; after purchase |

| Landed total (USD) | |
|---:|---:|
| Goods, summed from the lines above | 3,174.81 |
| Fees | 180.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 285.73 |
| Shipping, *estimated*: a flat allowance, because the suppliers state no figure for these orders | 60.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 317.48 |
| **Planning total** | **4,018.02** |

**The kit itself.** [Holybro](https://holybro.com/products/px4-development-kit-x500-v2) lists it at $609.00 (SKU 30189), sold out in all four variants. [NewBeeDrone](https://newbeedrone.com/products/holybro-x500-v2-full-kit-pixhawk-6c915mhz-telemetry-radio) lists $584.99, not available. [Kilitronic](https://kilitronic.com/products/holybro-drone-development-kit-x500-v2) lists $999.00, in stock, shipped from the USA with free UPS Ground (SKU 30189X). The lines above buy the same named parts from one US seller for $796.63. That they equal the kit is an inference, and Holybro's documentation page and store disagree on the GPS and power module, so confirm with the seller.

**Payload correction.** Holybro's documentation says about 1 kg with 4S 5000 mAh at 70% throttle [D13]. The 1.5 kg recorded earlier from the store page is not used here. Estimated payload: Jetson 175 g, camera 91 g (Luxonis; weigh on receipt), Remote ID 17 g, mount and tag box about 120 g (*estimated*), about 400 g in all.

**Ways to reduce it (planning total after each change, *estimated*):**
| Change | Total | Cost of the change |
|---|---:|---|
| Holybro restocks the $609 kit | 3,795 | wait; no date is published |
| [RadioMaster Pocket ELRS](https://www.readymaderc.com/products/details/85660-radiomaster-pocket-radio-controller-expresslrs-elrs-2-4ghz-charcoal-mode-2) at $76.99 instead of the TX16S | 3,842 | smaller radio, still an independent link |
| Indoor only: no Remote ID, exam or registration | 3,661 | closes D3 and all outdoor work |
| No SiK radio, if the licence question goes that way (Q6) | 3,932 | Wi-Fi only; a kit purchase would include one anyway |
| Jetson later | 3,543 | D2 hand-carried on a laptop, which rules out the first VIO candidate (it needs NVIDIA hardware), leaving BasaltVIO or nothing; D4 cannot fly VIO without onboard compute |

**Adds to it, on the same basis.** The two panels fit a ceiling up to 3.05 m and open sides up to 12.2 m in all. A taller ceiling needs [15 × 20 ft panels at $469.97](https://www.usnetting.com/drone-netting/), 276 more for two. A space with no solid walls needs four panels on a floor up to 6.1 m square, 842 more, and six on the 8.05 m floor that 1.0 m/s needs, 1,685 more.

## Option B — 3–5 inch guarded indoor frame (room-scale test space)
**No candidate read today has all four of: full guards, a current PX4 target, a published payload that carries camera and computer, and stock.** B-1 is priced because it fails only on guards.

### B-1: QAV250 ARF + Pixhawk 6C Mini
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Frame, motors, ESCs | Holybro QAV250 ARF kit | 1 | 219.00 | 219.00 | [holybro.com](https://holybro.com/products/qav250-kit) | in stock | 347.2 g; payload up to 500 g with a 4S 3000 mAh pack; 5 in props; 4S 2200–3000 mAh; **no guards as sold** |
| Autopilot | Holybro Pixhawk 6C Mini, Model A | 1 | 179.00 | 179.00 | [holybro.com](https://holybro.com/products/pixhawk-6c-mini) | available | 42.4 g; same target `px4_fmu-v6c_default` as Option A [D7]; Holybro sells this pairing as a kit, now sold out ($424.99 Complete), which is the pairing evidence |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399.00 | 399.00 | [sparkfun.com](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) | backorder; page conflicts | 175 g fits the 500 g payload by mass; mounting and power unverified |
| Camera for VIO | Luxonis OAK-D Lite | 1 | 269.00 | 269.00 | [shop.luxonis.com](https://shop.luxonis.com/products/oak-d-lite-1) | add-to-cart shown | 61 g per Luxonis; global-shutter stereo; BMI270 IMU |
| Batteries | Tattu 2300 mAh 4S 75C XT60 (EU seller; €31.79 at an assumed 1.15 USD/EUR) | 3 | 36.56 | 109.68 | [rotorama.com](https://www.rotorama.com/product/tattu-2300mah-4s-75c) | in stock | within Holybro's 2200–3000 mAh advice; no US source read at this capacity |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | 1–6S LiPo |
| LiPo bag | TBS LiPo bag, 23 × 30 cm | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging procedure |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | independent takeover link |
| RC receiver | RadioMaster RP1 V2 ELRS | 1 | 21.15 | 21.15 | [readymaderc.com](https://www.readymaderc.com/products/details/85669-radiomaster-rp1-2-4ghz-expresslrs-elrs-nano-receiver-v2) | in stock | as Option A |
| Containment | US Netting drone panel, 10 × 20 ft, 1-3/4 in mesh | 2 | 353.97 | 707.94 | [usnetting.com](https://www.usnetting.com/drone-netting/) | not stated | as Option A; guards do not replace the net [D39] |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | reach sized in `docs/REFERENCE_AND_SENSING.md` |

| Landed total (USD) | |
|---:|---:|
| Goods, summed from the lines above | 2,340.94 |
| Fees | 0.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 210.68 |
| Shipping, *estimated*: a flat allowance, because the suppliers state no figure for these orders | 50.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 234.09 |
| **Planning total** | **2,835.72** |

Estimated mass: 347.2 + 42.4 + 270 (battery) + 61 (camera) + 175 (Jetson) = 895.6 g before guards, receiver and mounts. **Guards are the blocking gap:** the one candidate read, [Unmanned Tech's 5 in guards](https://www.unmannedtechshop.co.uk/products/5-inch-universal-drone-propeller-guards-4-pack-anti-collision-shields-for-22-series-motors), is out of stock at £1.95, and its fit on this frame, its mass and its thrust effect are unverified. Until a guard is verified, this build is not Option B as defined, and the net has to do all the protecting. Endurance for this build has no published basis.

### Rejected for Option B
| Candidate | Why not |
|---|---|
| ModalAI Starling 2 | [its store page redirects](https://www.modalai.com/products/starling-2) to one listing only the Max, so it is **not listed as of 2026-10-31**. The $2,949.99 is a launch-price figure from a comparison table that also shows the Max at $2,999.99 while selling it at $4,199.99. No current price, so no total. It would need a quote. It runs PX4 and OpenVINS onboard; payload is about 85 g per a [staff estimate](https://forum.modalai.com/topic/5202/starling-2-payload); no first-party guards |
| [Holybro Kopis CineWhoop PNP](https://www.myfpvstore.com/brands/holybro/), $195.00 | ducted and in stock, but its Kakute F7 is discontinued in PX4's documentation (last published in v1.17), and no payload is published |
| GEPRC [CineLog35](https://www.myfpvstore.com/88rc), $61.99, + [Kakute H7 Mini](https://holybro.com/products/kakute-h7-mini), $82.00 | guards and a current PX4 target, but the [motor](https://www.rotorama.com/product/geprc-speedx2-2105-5-2650kv-m5) is "on the way" for Nov 12, 2026, one [ESC](https://www.flyingtech.co.uk/product/holybro-tekko32-f4-mini-4-in-1-50a-esc-am32/) is left, hole fit is unverified, and no payload figure exists |
| [Starling 2 Max](https://www.modalai.com/products/starling-2-max), $4,199.99 without a battery | 180 mm props are outside the size range |

## Not priced, covered by contingency
Cells for the radio (18650), XT60 charge lead, net hanging hardware, tag box and its mount, reference camera mounts, tape or laser measure, onboard power regulator for the Jetson, a 128 GB or larger NVMe drive (Isaac ROS 4.6 lists one for Jetson Orin [D16]), guards and spares for Option B-1 (no spares source was read for it). The contingency is an estimate; none of these has a quote.

## Rules for completing this worksheet
- Every line: supplier URL, date observed, unit price, shipping/tax estimate, and the compatibility evidence (a documentation page, not a forum post).
- Record totals per option; present both to the owner; the owner decides (ET-D0-6).
- Exam and registration lines are planning references, not transactions.
- Do not assume the planning range covers the final configuration.
- Sales tax depends on the owner's location, which is not recorded here; 9% is an assumption. Regenerate the totals when real quotes exist.
