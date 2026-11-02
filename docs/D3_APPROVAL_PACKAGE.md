# D3 approval package (draft, 2026-11-02)

**Not for purchase.** It collects the items the owner asked to see together at the D3 approval. Prices are from search results unless a line says the page was read; the RFD900x-US line was read on 2026-11-01. Recheck everything at D3.

## 1. Telemetry radio
| Option | FCC ID | Rule part | Price | Status |
|---|---|---|---:|---|
| RFDesign RFD900x-US bundle | 2ADLE-900X | 15.247 (owner's reading) | 281.21 | backorder, read 2026-11-01. The grant date against the 2025-12-22 cutoff is still to be checked |
| Holybro SiK Telemetry Radio, Long Range, 1 W, 915 MHz | **2BNF8-HT051WRF915**, from Holybro's product page via a search result; **the certification page the owner named was not read** | **not confirmed.** Grantee code 2BNF8 differs from 2AP22 on Holybro's HT03-V3, so whose grant it is must also be read. The same line on the page reads "100mW, 915.06~927.04MHz" against a stated 1 W output, so which rule part the grant is under, and at what power, must be read from the grant before it is considered (owner, 2026-11-02) | not read | Check at D3 |

## 2. Spare propellers
Gemfan 1555 carbon, from a source other than Holybro, whose stock is sold out. **No US seller was found on 2026-11-02:** a search found only German eBay listings for a generic 1555 carbon pair, one of which does not ship to the USA. GetFPV and RaceDayQuads showed no 1555. To search again at D3, including Amazon and asking a US dealer.

## 2a. Deferred lines and new items
- From `docs/BUY_LIST-REPRICED-2026-11-01.md`, deferred to D3: lines 22, 24, 25, 26 and F2.
- For ET-D3-6: a second anemometer and a 10 m mast, sited outside the 8.7 m standoff, both with logging at 1 Hz or faster. Not priced.

## 3. RTK GPS (rover and base station)
The M10 stays as the backup receiver; the baseboard has a second GPS port. RTK also gives ET-D3-6 its truth for drift measurements.

| Option | Rover | Base | Pair | Origin | FCC Covered List | Source |
|---|---:|---:|---:|---|---|---|
| Holybro F9P: DroneCAN H-RTK F9P Rover, SKU 12034, and H-RTK F9P Base, SKU 12022 | 296.99 | 415.99 | 712.98 | China (Holybro), u-blox receiver | **FLAG:** a GNSS receiver for UAS; its FCC grant or SDoC date must be read against the cutoff | rover from Holybro's store, base from Pyrodrone (out of stock), both search results |
| Holybro H-RTK Unicore UM982, dual antenna, with a base | 249.99 | 415.99 if the F9P base is used | 665.98 | China (Holybro; Unicore receiver) | **FLAG:** as above | Holybro's store via a search result; out of stock at World Drone Market and GetFPV |
| ARK RTK GPS and ARK RTK Base | 615.00–670.00 | 575.00 | 1,190.00–1,245.00 | **USA** (ARK; u-blox F9P receiver) | Exempt candidate: vendor states made in the USA; Blue UAS Framework listed per ArduPilot's page | ARK's category and product pages via search results; the base also appears at 595.00 |

Holybro direct imports would add the estimated 37.5% duty of `docs/BUY_LIST-REPRICED-2026-11-01.md`. The UM982's heading from two antennas is a second yaw source, which matters near magnetic interference. **A UM982 rover with an F9P base: RTCM3 MSM compatibility is not checked.**

**The correction link.** RTCM corrections must reach the rover: over the telemetry radio through the GCS, or over a separate radio, which is another transmitter with its own FCC rule-part question. The base needs a survey-in or a known point before each session, and a GCS that forwards corrections. Neither is in this package yet.

## 4. What the D3 data must show to raise the limits
The temporary D3 rule is 10 m, 4 m/s and 160 m. The owner expects 4 m/s to cost flying days in Los Angeles and wants a path to 6–8 m/s and a higher cap. ET-D3-6 collects the data and ET-D3-7 decides, in `config/phases.json`:
- **Shear at the site:** the handheld reading at 1.5 m against an anemometer at 10 m on every flight day. A 6–8 m/s handheld limit is only as good as the shear behind it.
- **Flow validity:** flow quality, range validity, surface and sun angle in every flight at 3, 6 and 10 m.
- **Flow-aided position loss:** with GPS aiding off and the ARK Flow MR fused, drift against truth at 3, 6 and 10 m across the wind bands D3 allows, once separately approved. If flow holds velocity, the position-lost reach stops scaling with wind × time, which is what makes 160 m necessary today.
- **Wind authority:** tilt and motor output in hover at each wind, to predict the reserve at 6–8 m/s.
- **The criteria, proposed by the agent:** with flow, predicted p99 reach inside the radius by 10 m at p95 shear with a 5 s delay; without flow, reach inside the radius too unless flow validity is shown; held-out per-trial error at most 15%; peak actuator output at most 0.75. Any raise is the owner's decision, and the first flights at a raised limit are their own approved test.

**What D3 cannot show:** behaviour in 6–8 m/s ambient wind, or above 10 m, where flow is never measured. Upwind legs reach about 6.5 m/s airspeed, which covers some of the aerodynamics but not ambient wind at that speed. Held-out checks test the model only inside the measured range. A raise to those values rests on extrapolation and on the separately approved first flights at the raised limit.

**The GPS-off trials need their own approval.** Turning GPS aiding off in flight puts the aircraft in Altitude mode if flow is not fused, where the D3 speed limit does not hold and the fence does not act. ET-D3-6 (b) and (d) therefore need a dated owner approval naming the configuration, and an ADR; flow must be fused and range valid before each cut. Without RTK, the M10's logged position is the truth; the outside-in reference covers a 1.5 m box and cannot serve.
