# BOM_WORKSHEET.md — D0 delivered-cost worksheet

**Status: dated price observations from suppliers' pages, not quotes and not a purchase recommendation. Nothing was bought.** Every line was read on 2026-10-31; prices move, so recheck before acting. Bracketed references are in `docs/SOURCES.md` and `docs/SOURCES-D0.md`. Generated from one table, so totals follow the lines. **Nothing here authorizes a purchase.**

## Summary
| Option | Planning total (USD) | What it is | Main problem |
|---|---:|---|---|
| A: X500 V2 | 3,725 | 500 mm kit for a garage, warehouse or field | above the owner's planning range |
| B-1: QAV250 + Pixhawk 6C Mini | 2,414 | cheapest room-scale build that can carry the camera and computer | **no verified guards**, so it does not yet meet the option's definition |
| B-2: Starling 2 | 4,501 | integrated vehicle with onboard VIO | price and stock not confirmed; guards third-party and unverified |

**The owner's $1,900–2,300 range does not cover Option A as specified.** Option A is about $1,425 above the top of the range. The largest differences from the original plan are the net ($461.97 against $60–150 planned), the kit bought piece by piece because it is sold out (see below), and the tax, shipping and contingency the range left out. Ways to bring it down are listed under Option A.

## Option A — 500 mm class kit (garage / warehouse / field)
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Airframe (no autopilot) | Holybro X500 V2 ARF kit | 1 | 396.71 | 396.71 | [readymaderc.com](https://www.readymaderc.com/products/details/87064-holybro-x500-v2-almost-ready-to-fly-arf-kit) | in stock | 500 mm; 2216 KV920 motors, BLHeli S 20A ESCs, 4S [D13]; platform board has holes for companion computers [D13] |
| Autopilot | Holybro Pixhawk 6C, plastic case, PM02 V3 | 1 | 275.15 | 275.15 | [readymaderc.com](https://www.readymaderc.com/products/details/86046-holybro-pixhawk-6c-with-plastic-case-pm02-power-module-no-gps) | in stock | PX4 target `px4_fmu-v6c_default` [D7] |
| GPS | Holybro M10, 10-pin | 1 | 52.79 | 52.79 | [readymaderc.com](https://www.readymaderc.com/products/details/86930-holybro-m10-gps-with-standard-10-pin-connector) | in stock | kit part [D12]; indoor tests do not use it |
| Telemetry | Holybro SiK V3 915 MHz, pair | 1 | 71.98 | 71.98 | [readymaderc.com](https://www.readymaderc.com/products/details/86245-holybro-sik-telemetry-radio-v3-100mw-915mhz-2-pcs) | in stock | seller says an amateur licence is required in the US (owner question Q6) |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399.00 | 399.00 | [sparkfun.com](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) | backorder; page conflicts | 175 g, 9–20 V input [D15]; 4S direct power is not approved by that document; Holybro names Jetson Nano, not Orin Nano, so hole fit is unverified |
| Depth / stereo camera | Luxonis OAK-D Pro | 1 | 429.00 | 429.00 | [shop.luxonis.com](https://shop.luxonis.com/products/oak-d-pro) | add-to-cart shown | global-shutter stereo, BNO086 IMU [D21]; mass not published; driver `depthai_ros_v3` on Jazzy [D20] |
| Camera mount | Holybro Depth Camera Mount | 1 | 10.59 | 10.59 | [holybro.com](https://holybro.com/products/depth-camera-mount) | available | names RealSense and Structure Core, not OAK; fit unverified |
| Batteries | Tattu 5200 mAh 4S 35C XT60 | 3 | 62.99 | 188.97 | [readymaderc.com](https://www.readymaderc.com/products/details/tattu-5200mah-4s1p-35c-xt60) | in stock | 4S as Holybro recommends (2000–5000 mAh); 5200 mAh is the PX4 kit page's figure; ground shipping only |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | 1–6S LiPo; page's wattage figures conflict |
| LiPo bag | TBS LiPo bag, 23 × 30 cm | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging procedure |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | independent takeover link; batteries not included |
| RC receiver | RadioMaster RP1 V2 ELRS | 1 | 21.15 | 21.15 | [readymaderc.com](https://www.readymaderc.com/products/details/85669-radiomaster-rp1-2-4ghz-expresslrs-elrs-nano-receiver-v2) | in stock | PX4 lists ExpressLRS with CRSF as validated [D18]; CRSF telemetry needs custom firmware [D19] |
| Containment | US Netting drone panel, 20 × 20 ft, 4 in mesh | 1 | 461.97 | 461.97 | [usnetting.com](https://www.usnetting.com/drone-netting/panels) | not stated | no guards found for the X500; tensile field blank on the page |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | reach sized in `docs/REFERENCE_AND_SENSING.md`; rolling shutter is inferred, so measure it |
| Spares: props | Holybro 1045 props, 2 pair | 2 | 11.59 | 23.18 | [holybro.com](https://holybro.com/products/spare-parts-x500-v2-kit) | sold out | no in-stock US source found |
| Spares: arms | Holybro carbon fiber arm tube | 2 | 6.59 | 13.18 | [holybro.com](https://holybro.com/products/spare-parts-x500-v2-kit) | sold out | no in-stock US source found |
| Remote ID (outdoor only) | Dronetag Beacon gen 2 | 1 | 149.00 | 149.00 | [shop.dronetag.com](https://shop.dronetag.com/products/21-dronetag-beacon.html) | in stock | DoC RID000001121 per a third-party mirror dated 2026-09-26 [D28]; check the FAA list before buying |
| Part 107 knowledge test (outdoor only) | FAA initial exam | 1 | 175.00 | 175.00 | [faa.gov](https://www.faa.gov/faq/how-much-does-it-cost-get-remote-pilot-certificate) | — | “approximately $175” [S2]; personal; planning reference, not a transaction here |
| Part 107 registration (outdoor only) | per aircraft, three years | 1 | 5.00 | 5.00 | [faa.gov](https://www.faa.gov/uas/getting_started/register_drone) | — | $5 per drone [S3]; after purchase |

| Landed total (USD) | |
|---:|---:|
| Goods, measured from the lines above | 2,928.84 |
| Fees | 180.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 263.60 |
| Shipping, *estimated*; suppliers state none for these orders | 60.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 292.88 |
| **Planning total** | **3,725.32** |

**The kit itself.** Holybro lists it at $609.00 (SKU 30189), sold out in all four variants. NewBeeDrone lists $584.99, not available. Kilitronic lists $999.00, in stock, shipped from the USA with free UPS Ground (SKU 30189X). The lines above buy the same named parts from one US seller for $796.63. That they equal the kit is an inference, and Holybro's documentation page and store disagree on the GPS and power module, so confirm with the seller.

**Payload correction.** Holybro's documentation says about 1 kg with 4S 5000 mAh at 70% throttle [D13]. The 1.5 kg recorded earlier from the store page is not used here. Estimated payload: Jetson 175 g, camera about 91 g (unverified; weigh it), Remote ID 16 g, mount and tag array about 80 g (*estimated*), about 360 g in all.

**Ways to reduce it (planning total after each change, *estimated*):**
| Change | Total | Cost of the change |
|---|---:|---|
| Holybro restocks the $609 kit | 3,502 | wait; no date is published |
| RadioMaster Pocket ELRS at $76.99 instead of the TX16S | 3,549 | smaller radio, still an independent link |
| Indoor only: no Remote ID, exam or registration | 3,368 | closes D3 and all outdoor work |
| No SiK radio, if the licence question goes that way (Q6) | 3,640 | Wi-Fi only; a kit purchase would include one anyway |
| Jetson later | 3,251 | hand-carried D2 only, on a laptop; D4 cannot fly VIO without onboard compute |

## Option B — 3–5 inch guarded indoor frame (room-scale test space)
**No candidate read today has all four of: full guards, a current PX4 target, a published payload that carries camera and computer, and stock.** Two are priced because they fail differently.

### B-1: QAV250 ARF + Pixhawk 6C Mini
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Frame, motors, ESCs | Holybro QAV250 ARF kit | 1 | 219.00 | 219.00 | [holybro.com](https://holybro.com/products/qav250-kit) | in stock | 347.2 g; 500 g payload; 5 in props; 4S 2200–3000 mAh; **no guards as sold** |
| Autopilot | Holybro Pixhawk 6C Mini, Model A | 1 | 179.00 | 179.00 | [holybro.com](https://holybro.com/products/pixhawk-6c-mini) | available | 42.4 g; same target `px4_fmu-v6c_default` as Option A [D7]; PX4 lists this kit with Pixhawk 6c, not the Mini, so the pairing is unverified |
| Companion computer | NVIDIA Jetson Orin Nano Super 8 GB dev kit | 1 | 399.00 | 399.00 | [sparkfun.com](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) | backorder; page conflicts | 175 g fits the 500 g payload by mass; mounting and power unverified |
| Camera for VIO | Luxonis OAK-D Lite | 1 | 269.00 | 269.00 | [docs.luxonis.com](https://docs.luxonis.com/hardware/products/OAK-D%20Lite) | not shown | 61 g; global-shutter stereo; BMI270 IMU |
| Batteries | Tattu 2300 mAh 4S 75C XT60 (EU seller; €31.79 at an assumed 1.15 USD/EUR) | 3 | 36.56 | 109.68 | [rotorama.com](https://www.rotorama.com/product/tattu-2300mah-4s-75c) | in stock | within Holybro's advice; no US source read at this capacity |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | 1–6S LiPo |
| LiPo bag | TBS LiPo bag, 23 × 30 cm | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging procedure |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | independent takeover link |
| RC receiver | RadioMaster RP1 V2 ELRS | 1 | 21.15 | 21.15 | [readymaderc.com](https://www.readymaderc.com/products/details/85669-radiomaster-rp1-2-4ghz-expresslrs-elrs-nano-receiver-v2) | in stock | as Option A |
| Containment | US Netting drone panel, 10 × 10 ft, 4 in mesh | 2 | 176.97 | 353.94 | [usnetting.com](https://www.usnetting.com/drone-netting/panels) | not stated | two panels as a curtain; guards do not replace the net |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | reach sized in `docs/REFERENCE_AND_SENSING.md` |

| Landed total (USD) | |
|---:|---:|
| Goods, measured from the lines above | 1,986.94 |
| Fees | 0.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 178.82 |
| Shipping, *estimated*; suppliers state none for these orders | 50.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 198.69 |
| **Planning total** | **2,414.46** |

Estimated mass: 347.2 + 42.4 + 270 (battery) + 61 (camera) + 175 (Jetson) = 895.6 g before guards, receiver and mounts. **Guards are the blocking gap:** the only lead is a third-party 5 in guard seen in a search snippet, whose page could not be read. Without verified guards this build is not Option B as defined, and the net has to do all the protecting.

### B-2: Starling 2
| Item | Candidate | Qty | Unit USD | Line USD | Supplier (read 2026-10-31) | Stock read | Compatibility evidence |
|---|---|---:|---:|---:|---|---|---|
| Complete vehicle | ModalAI Starling 2 (price from a comparison table; store page unread) | 1 | 2949.99 | 2949.99 | [modalai.com](https://www.modalai.com/products/starling-2-max) | not read | 285 g; 120 mm props; VOXL 2 runs PX4 and OpenVINS onboard; about 85 g payload per a staff estimate; no first-party guards |
| Charger | ToolkitRC M6AC | 1 | 63.71 | 63.71 | [readymaderc.com](https://www.readymaderc.com/products/details/86179-toolkitrc-m6ac-charger) | in stock | vehicle uses 2S 18650 packs; fit unverified |
| LiPo bag | TBS LiPo bag, 23 × 30 cm | 1 | 7.61 | 7.61 | [readymaderc.com](https://www.readymaderc.com/products/details/tbs-lipo-battery-bag) | in stock | storage and charging procedure |
| RC transmitter | RadioMaster TX16S MK3 ELRS | 1 | 224.87 | 224.87 | [readymaderc.com](https://www.readymaderc.com/products/details/86685-radiomaster-tx16s-mk3-elrs-dual-band-gemini-v6-hall-gimbals-black) | in stock | vehicle's receiver options not read |
| Containment | US Netting drone panel, 10 × 10 ft, 4 in mesh | 2 | 176.97 | 353.94 | [usnetting.com](https://www.usnetting.com/drone-netting/panels) | not stated | as Option B-1 |
| Outside-in reference | Logitech C920s | 2 | 69.99 | 139.98 | [logitech.com](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html) | in stock | as Option B-1 |

| Landed total (USD) | |
|---:|---:|
| Goods, measured from the lines above | 3,740.10 |
| Fees | 0.00 |
| Sales tax, *estimated* at an assumed 9% of goods | 336.61 |
| Shipping, *estimated*; suppliers state none for these orders | 50.00 |
| Contingency, *estimated* at 10% of goods (unpriced items below) | 374.01 |
| **Planning total** | **4,500.72** |

The price comes from the comparison table on the Starling 2 Max page, which may be stale; stock and lead time could not be read (the Max ships within 60 business days). Mass is 285 g (datasheet), 280 g (PX4). Flight-time figures disagree: over 35 min (datasheet), 40 min (PX4). Guards are a third-party printable design with unverified fit.

### Rejected for Option B
| Candidate | Why not |
|---|---|
| Holybro Kopis CineWhoop PNP, $195.00 | ducted and in stock, but its Kakute F7 is discontinued in PX4's documentation (last published in v1.17), and no payload is published |
| GEPRC CineLog35 + Kakute H7 Mini, about $167 plus £86.80 and €98.36 | guards and a current PX4 target, but the motor is "on the way" for Nov 12, 2026, one ESC is left, hole fit is unverified, and no payload figure exists |
| Starling 2 Max, $4,199.99 | 180 mm props are outside the size range |

## Not priced, covered by contingency
Cells for the radio (18650), XT60 charge lead, net hanging hardware or frame, printed tag array and backing plate, reference camera mounts, tape or laser measure, onboard power regulator for the Jetson, guards for Option B-1, and spares for Option B. The contingency is an estimate; none of these has a quote.

## Rules for completing this worksheet
- Every line: supplier URL, date observed, unit price, shipping/tax estimate, and the compatibility evidence (a documentation page, not a forum post). The exceptions are marked: the Starling 2 payload is a staff forum estimate.
- Record totals per option; present both to the owner; the owner decides (ET-D0-6).
- Exam and registration lines are planning references, not transactions.
- Do not assume the planning range covers the final configuration.
- Sales tax depends on the owner's location, which is not recorded here; 9% is an assumption. Regenerate the totals when real quotes exist.
