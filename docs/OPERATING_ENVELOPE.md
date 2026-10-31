# OPERATING_ENVELOPE.md — D0 deliverable

**Status: proposed, written 2026-10-31 by WO-001. Not a flight authorization.** Limits are *estimated* from the arithmetic below until D1 and D2 measure them. Q1–Q7 are the named owner questions in `reports/WO-001-d0-operating-envelope-and-platform-proposal.md`. Where the test space decides a row, both answers are given.

| Decision | Room (Option B) | Garage / warehouse (Option A) | Field (Option A, D3 only) |
|---|---|---|---|
| Mission and site | First mission (D6): fixed-target inspection from N viewpoints and return. Site unknown (Q1) | Same; site unknown (Q1) | Same; site unknown (Q1) |
| Airframe | 3–5 in guarded frame: no candidate fully qualifies yet (Q2, `docs/BOM_WORKSHEET.md`) | Holybro X500 V2, about 1 kg payload [D13] | Holybro X500 V2 |
| Speed | ≤ 0.5 m/s | ≤ 1.0 m/s | ≤ 2.5 m/s |
| Clearance to any obstacle or net | ≥ 1.0 m | ≥ 1.8 m | ≥ 6 m |
| Height | ≤ ceiling − 1.0 m, and ≤ 2.5 m | ≤ ceiling − 1.8 m, and ≤ 2.5 m | ≤ 30 m AGL, inside the 400 ft limit [D29] |
| Minimum clear floor (flight box 1.5 m square, X500 span about 0.75 m) | 4.25 m square with an X500; less with a small frame | 5.85 m square | Set at the site |
| Containment | Net curtain, 4 in mesh; guards do not replace it | Net enclosure, 4 in mesh; X500 guards were not found | People exclusion; PX4's rule of thumb is no people within 100 m [D40] |
| Sensors | OAK-D Lite class, 61 g; stereo global shutter, IMU | OAK-D Pro (default, Q4) or D435i; stereo global shutter, IMU [D21][D26] | Same, plus M10 GPS |
| Compute | Hand-carried D2 on a laptop; **flying VIO needs onboard compute** (Q3) | Same; Jetson Orin Nano Super from D2 proposed (Q3) | Same |
| Energy | 4S 2300 mAh × 3 (B-1); land at ≥ 25% | 4S 5200 mAh × 3; land at ≥ 25% | Same as garage |
| Human control | Trained operator on an independent RC link, kill switch assigned, observer. Takeover tested props off (D2), then in flight (D4) | Same | Same, within visual line of sight |
| Reference (evaluation only) | Two fixed cameras, tag array on the aircraft, independent clock; static RMS target ≤ 2 cm (`docs/REFERENCE_AND_SENSING.md`) | Same | Not used for D3 |
| Data and privacy | Test volume only; faces excluded or blurred; retention per `docs/DATA_POLICY.md`; GPS stripped from anything shared | Same | Same |

## How the limits were derived (estimated, not measured)
Required clearance = reaction distance + braking distance + position error.
- **Braking:** jerk-limited, `d = v·√(v/j)` for v ≤ a²/j = 2.25 m/s, otherwise `d = v·(v/a + a/j)/2`, with PX4 defaults a = 3 m/s² (`MPC_ACC_HOR`) and j = 4 m/s³ (`MPC_JERK_AUTO`) [D24]. No page read says these govern Hold braking, so D1 must measure it.
- **Reaction, gate working:** 0.35 s, the sum of the proposed setpoint (200 ms) and sensor (150 ms) age bounds.
- **Reaction, link lost:** 1.0 s, PX4's default `COM_OF_LOSS_T` [D23], during which the last setpoint may still be applied (worst case; D1 tests it).
- **Position error:** 0.3 m indoors, ET-D4-2's proposed bound; 1.0 m on GPS, ET-D3-2's.

| Speed | Braking | Clearance, gate working | Clearance, link lost |
|---:|---:|---:|---:|
| 0.25 m/s | 0.06 m | 0.45 m | 0.61 m |
| 0.5 m/s | 0.18 m | 0.65 m | **0.98 m** |
| 1.0 m/s | 0.50 m | 1.15 m | **1.80 m** |
| 2.5 m/s (GPS) | 1.98 m | 3.86 m | **5.48 m** |

**The earlier default of ≤ 1.0 m/s with ≥ 0.5 m clearance fails this arithmetic:** at 1.0 m/s the aircraft can need 1.15–1.80 m. The limits above use the link-lost column. Setting `COM_OF_LOSS_T` to 0.5 s would reduce 1.80 m to 1.30 m, if D1 confirms it.

Limits PX4 will not enforce for us: `MPC_XY_CRUISE` and `MPC_VEL_MANUAL` have a 3 m/s floor [D24], so the indoor speed limit is enforced in this project's command gate and by `MPC_XY_VEL_MAX`. Whether the geofence works on vision-only position is unverified, and it acts only after a breach [D25], so the net is the containment and the fence is not counted on.

## Failsafes to configure and test in D1 (proposed values)
| Parameter | PX4 default [D23][D24] | Proposed | Why |
|---|---|---|---|
| `COM_OF_LOSS_T` | 1.0 s | 1.0 s until D1 measures it | used in the arithmetic |
| `COM_OBL_RC_ACT` | 0 Position | 5 Hold | a value the source lists; the docs misname value 2 and omit 5–7 |
| `NAV_RCL_ACT` | 2 Return | 3 Land | Return is wrong in a room |
| `RC_MAP_KILL_SW` | 0, unassigned | assigned | no kill switch otherwise |
| `COM_FAIL_ACT_T` | 5.0 s | test it | the aircraft waits in Hold first, and stick override is not available then |
| `EKF2_NOAID_TOUT` | 5 s | test it | how long position may be lost before PX4 reacts |

## Energy (estimated)
Holybro states about 18 min hover with no added payload on 5000 mAh [D13]; 75% of that is 13.5 min. Added mass and up to 25 W for the Jetson reduce it by an amount not published. Plan flights of ≤ 8 min until D4 measures it. Never charge unattended; store in the LiPo bag.

## Compliance (rechecked 2026-10-31; recheck before any outdoor stage)
| Item | Plan | Source | Recheck |
|---|---|---|---|
| Part 107 path | Non-recreational flying is regulated by Part 107; development flights are not assumed recreational. Age 16 or over; FAA Tracking Number through IACRA; scheduled knowledge test; form 8710-13; recurrent training every 24 calendar months | [S1][D29][D32] | before D3 |
| Knowledge test | About $175, paid to the test center | [S2] | before booking |
| Registration | $5 per drone, three years, on FAADroneZone. The 250 g exception applies only to recreational flying, so it is not a route here. A registration cannot move between Part 107 and recreational | [S3] | before D3 |
| Remote ID | Registered drones must comply. Route: a broadcast module with its serial on an FAA-accepted declaration, registered per device. A FRIA is not a route, because only community-based organizations and educational institutions can hold one | [S4][D29] | before buying a module; check the FAA list directly [D28] |
| Indoor only | Part 107 does not apply indoors [S5]; the FAA's 2016 wording is "inside an enclosed structure" [D33]. **Open doors and part-enclosed spaces are not settled by any source read, so doors stay closed and an open space counts as outdoors until the owner has an answer** | [S5][D33] | before D4 |
| Site permission | Written permission recorded for any site; people excluded from the volume during armed tests | [S5] | each site |
| Visual line of sight | Unaided sight of the aircraft throughout; a broadcast module also requires it. No BVLOS or waiver is assumed. Part 108 is not in force: Final Rule at OIRA since 07/10/2026, not in the eCFR | [D29][D31] | before D3 |
| Altitude, speed | 400 ft AGL and 100 mph limits sit far above this envelope | [D29] | before D3 |
| Operation over people | Prohibited without a stated basis; people are excluded | [D29] | before D3 |
| Radio | One seller says the 915 MHz SiK radio needs an amateur licence in the US. No FCC page was read (Q6) | `docs/BOM_WORKSHEET.md` | before buying |

## Budget status
Option A's planning total is above the owner's $1,900–2,300 range (`docs/BOM_WORKSHEET.md`, Q7). **No purchase authorization is implied by any document in this repository.**
