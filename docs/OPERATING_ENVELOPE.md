# OPERATING_ENVELOPE.md — D0 deliverable (fill before any hardware choice)

**Status: template with proposed defaults. Not a flight authorization.** WO-001 fills every row; unknowns become named owner questions (ET-D0-1). The envelope bounds every later exit test.

| Decision | Required record | Proposed default / current knowledge |
|---|---|---|
| Mission and site | First mission (D6): fixed-target inspection from N viewpoints and return. Site dimensions, access, people exclusion, owner permission | Site **unknown** — owner question #1 (room vs garage/warehouse vs field). Decides the airframe class |
| Airframe | Conventional guarded multirotor; mass, payload, propulsion compatibility | 500 mm class (Holybro X500 V2, 1.5 kg payload) for a garage/field; 3–5 inch guarded frame for a room. No purchase |
| Speed / height / clearance | Numerical limits justified by sensing range, latency, stopping distance and containment | *proposed:* ≤ 1.0 m/s indoors, ≤ 2.5 m altitude indoors, ≥ 0.5 m clearance; derive stopping distance from measured latency in D1/D2 |
| Sensors | Camera/IMU timing; VIO suitability; depth sensing; mounting and calibration; vibration plan | OAK-D Pro or RealSense D435i as depth/stereo; Pixhawk IMU; VIO candidate chosen in WO-001 with evidence of PX4 external-vision support [S6] |
| Compute | Laptop prototype vs onboard; link budget and latency; independent onboard loss response | Laptop over Wi-Fi for D1–D4; Jetson Orin Nano Super onboard from D7; PX4 offboard-loss failsafe handles link loss regardless |
| Energy | Battery and charger compatibility; reserve; charging/storage procedure; spares | 4S 5000 mAh × 3; reserve ≥ 25% at landing; LiPo-safe bag; never charge unattended |
| Reference (evaluation only) | Outside-in cameras and tags; calibrated coverage, timing, uncertainty, session check | 1–2 fixed webcams on the wall tracking a rigid tag array on the aircraft; independent clock; target static RMS ≤ 2 cm (`docs/REFERENCE_AND_SENSING.md`) |
| Containment | Airframe-specific: prop guards; net enclosure or tether for first indoor armed tests; controlled field arrangement outdoors | Decided per airframe in WO-001; no universal tether rule |
| Human control | Qualified operator, independent takeover link, checklists, observers | RadioMaster TX16S on an independent link; operator takeover tested in D2 (props off) and D4 (in flight) |
| Compliance (outdoor) | Part 107 path; registration; Remote ID; airspace and site review; VLOS | Plan Part 107 certificate (~$175 exam [S2]); registration $5/3 years [S3]; Remote ID route [S4]; development flights are not assumed recreational [S1] |
| Compliance (indoor) | Part 107 does not apply indoors-only [S5]; permission and physical controls still required | Site permission recorded; people excluded from the volume during armed tests |
| Data and privacy | Camera permissions; access control; sensitive-location and footage retention policy | Bench/test volume only; faces excluded or blurred; raw footage retained per `docs/DATA_POLICY.md`; GPS stripped from any public release |

## FAA planning notes (checked 2026-10-30; recheck at execution)
- Non-recreational flights generally fall under Part 107; unpaid is not the same as recreational [S1].
- Initial knowledge test ≈ $175 [S2]; study time is a personal estimate (15–20 h).
- Registration $5 per Part 107 aircraft for three years [S3]. The sub-250 g exception is recreational-only; it is not a blanket exemption for this project [S3][S4].
- Indoor-only operations are outside Part 107 [S5]; site permission and test controls remain.
- A certificate does not authorize every operation or location; plan within VLOS and airspace rules. No BVLOS or waiver is assumed.

## Budget status
Hardware totals are planning ranges until the BOM is quoted (`docs/BOM_WORKSHEET.md`). The owner's $1.9–2.3k range is not a commitment that the final configuration fits it. **No purchase authorization is implied by any document in this repository.**
