# D3 approval package (draft, 2026-11-02)

**Not for purchase.** It collects the items the owner asked to see together at the D3 approval. Prices are from search results unless a line says the page was read; recheck at D3.

## 1. Telemetry radio
| Option | FCC ID | Rule part | Price | Status |
|---|---|---|---:|---|
| RFDesign RFD900x-US bundle | 2ADLE-900X | 15.247 (owner's reading) | 281.21 | backorder, read 2026-11-01. The grant date against the 2025-12-22 cutoff is still to be checked |
| Holybro SiK Telemetry Radio, Long Range, 1 W, 915 MHz | **2BNF8-HT051WRF915**, from Holybro's product page via a search result | **not confirmed.** The same line on the page reads "100mW, 915.06~927.04MHz" against a stated 1 W output, so which rule part the grant is under, and at what power, must be read from the grant before it is considered (owner, 2026-11-02) | not read | Check at D3 |

## 2. Spare propellers
Gemfan 1555 carbon, from a source other than Holybro, whose stock is sold out. To find at D3.

## 3. RTK GPS (rover and base station)
The M10 stays as the backup receiver; the baseboard has a second GPS port. RTK also gives ET-D3-6 its truth for drift measurements.

| Option | Rover | Base | Pair | Origin | FCC Covered List | Source |
|---|---:|---:|---:|---|---|---|
| Holybro F9P: DroneCAN H-RTK F9P Rover, SKU 12034, and H-RTK F9P Base, SKU 12022 | 296.99 | 415.99 | 712.98 | China (Holybro), u-blox receiver | **FLAG:** a GNSS receiver for UAS; its FCC grant or SDoC date must be read against the cutoff | rover from Holybro's store, base from Pyrodrone (out of stock), both search results |
| Holybro H-RTK Unicore UM982, dual antenna, with a base | 249.99 | 415.99 if the F9P base is used | 665.98 | China (Holybro; Unicore receiver) | **FLAG:** as above | Holybro's store via a search result; out of stock at World Drone Market and GetFPV |
| ARK RTK GPS and ARK RTK Base | 615.00–670.00 | 575.00 | 1,190.00–1,245.00 | **USA** (ARK; u-blox F9P receiver) | Exempt candidate: vendor states made in the USA; Blue UAS Framework listed per ArduPilot's page | ARK's category and product pages via search results; the base also appears at 595.00 |

Holybro direct imports would add the estimated 37.5% duty of `docs/BUY_LIST-REPRICED-2026-11-01.md`. The UM982's heading from two antennas is a second yaw source, which matters near magnetic interference.

## 4. What the D3 data must show to raise the limits
The temporary D3 rule is 10 m, 4 m/s and 160 m. The owner expects 4 m/s to cost flying days in Los Angeles and wants a path to 6–8 m/s and a higher cap. ET-D3-6 collects the data and ET-D3-7 decides, in `config/phases.json`:
- **Shear at the site:** the handheld reading at 1.5 m against an anemometer at 10 m on every flight day. A 6–8 m/s handheld limit is only as good as the shear behind it.
- **Flow-aided position loss:** with GPS aiding off and the ARK Flow MR fused, drift against truth at 3, 6 and 10 m across the wind bands D3 allows. If flow holds velocity, the position-lost reach stops scaling with wind × time, which is what makes 160 m necessary today.
- **Wind authority:** tilt and motor output in hover at each wind, to predict the reserve at 6–8 m/s.
- **The criteria:** predicted p99 reach inside the radius by 10 m at p95 shear with a 5 s delay; held-out error at most 15%; at least 25% of thrust in reserve. Any raise is the owner's decision, and the first flights at a raised limit are their own approved test.

**What D3 cannot show:** behaviour at 6–8 m/s itself, because D3 flies at 4 m/s or less. Raising to 8 m/s doubles the highest measured wind, so the model carries most of that claim. That is why the criteria need held-out checks, and why the first flights at a raised limit are a separate test.
