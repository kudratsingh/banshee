# OPERATING_ENVELOPE.md — D0 deliverable

**Status: proposed, written 2026-10-31 by WO-001. Not a flight authorization.** Limits are *estimated* from the arithmetic below until D1, D2 and D4 measure them. Q1–Q7 are the named owner questions in `reports/WO-001-d0-operating-envelope-and-platform-proposal.md`. Where the test space decides a row, each answer is given.

| Decision | Room | Garage or warehouse | Field (D3 only) |
|---|---|---|---|
| Mission and site | First mission (D6): fixed-target inspection from N viewpoints and return. Site unknown (Q1) | Same; site unknown (Q1) | Same; site unknown (Q1) |
| Airframe | 3–5 in guarded frame: no candidate fully qualifies yet (Q2, `docs/BOM_WORKSHEET.md`); or an X500 if the floor allows | Holybro X500 V2, about 1 kg payload [D13] | Holybro X500 V2 |
| Horizontal speed | ≤ 0.5 m/s | ≤ 0.5 m/s; ≤ 1.0 m/s only on a floor of at least 8.05 m square | ≤ 2.5 m/s |
| Vertical speed | ≤ 0.5 m/s up and down, enforced by the command gate; landing at PX4's 0.7 m/s | Same | Same |
| Clearance to any obstacle or net | ≥ 1.5 m hold (D4); ≥ 1.9 m moving (D5–D6) | Same at 0.5 m/s; ≥ 2.5 m and ≥ 2.9 m at 1.0 m/s | ≥ 7.5 m |
| Height | ≥ 1.2 m; ≤ ceiling − 1.4 m (small frame) or − 1.5 m (X500); ≤ 2.5 m | Same | ≤ 30 m AGL |
| Minimum ceiling | 2.6 m (small frame); 2.7 m (X500) | 2.7 m | none |
| Minimum clear floor (1.5 m flight box; add about 1 m on one side for the operator bay) | small frame, span about 0.45 m: 4.95 m (D4), 5.75 m (D5–D6); X500: 5.25 m, 6.05 m | X500 at 0.5 m/s: 5.25 m (D4), 6.05 m (D5–D6); at 1.0 m/s: 8.05 m | set at the site |
| Containment | Net between the aircraft and the operator bay, doors, windows and anything not to be hit. 1-3/4 in mesh [D39]. Guards do not replace it | Same; no X500 guards were found | People excluded to 100 m, PX4's rule of thumb [D40]; geofence below |
| Sensors | OAK-D Lite, 61 g; stereo global shutter, IMU | OAK-D Pro (default, Q4) or D435i; stereo global shutter, IMU [D21][D26] | Same, plus M10 GPS |
| Compute | Jetson Orin Nano Super from D2 proposed (Q3). If later, D2 is hand-carried on a laptop, which rules out the first VIO candidate. **Flying VIO needs onboard compute** | Same | Same |
| Energy | 4S 2300 mAh × 3 (B-1); land at ≥ 25%; endurance has no published basis | 4S 5200 mAh × 3; land at ≥ 25% | Same as garage |
| Human control | Trained operator on an independent RC link, behind the net, with kill switch and mode switch assigned; observer. Takeover tested props off (D2), then in flight (D4) | Same | Same, within visual line of sight |
| Reference (evaluation only) | Two fixed cameras, tag box on the aircraft, independent clock; static RMS target ≤ 2 cm (`docs/REFERENCE_AND_SENSING.md`) | Same | Not used for D3 |
| Data and privacy | Test volume only; faces excluded or blurred; retention per `docs/DATA_POLICY.md`; GPS stripped from anything shared | Same | Same |

## How the limits were derived (estimated, not measured)
Required clearance = reaction distance + braking distance + peak position error.
- **Braking:** jerk-limited, `d = v·√(v/j)` for v ≤ a²/j = 2.25 m/s, otherwise `d = v·(v/a + a/j)/2`, with PX4 defaults a = 3 m/s² (`MPC_ACC_HOR`) and j = 4 m/s³ (`MPC_JERK_AUTO`) [D24]. No page read says these govern Hold braking, so D1 must measure it.
- **Reaction, worst case:** 1.35 s. That is 1.0 s for PX4's default `COM_OF_LOSS_T` [D23], plus the proposed setpoint (200 ms) and sensor (150 ms) age bounds that can run before the link is lost. The last setpoint may be applied throughout, which D1 tests.
- **Peak position error:** twice the RMS bound, an assumption D4 replaces with a measurement. Hold: 2 × 0.3 m (ET-D4-2). Moving flight: 2 × 0.5 m (ET-D5-1). GPS: 2 × 1.0 m (ET-D3-2).

| Speed | Reaction | Braking | Clearance, hold | Clearance, moving | Moving, if `COM_OF_LOSS_T` is 0.5 s |
|---:|---:|---:|---:|---:|---:|
| 0.25 m/s | 0.34 m | 0.06 m | 1.00 m | 1.40 m | 1.28 m |
| 0.5 m/s | 0.68 m | 0.18 m | **1.45 m** | **1.85 m** | 1.60 m |
| 1.0 m/s | 1.35 m | 0.50 m | **2.45 m** | **2.85 m** | 2.35 m |
| 2.5 m/s (GPS) | 3.38 m | 1.98 m | — | **7.35 m** | — |

Minimum floor = flight box + aircraft span + 2 × clearance, plus about 1 m (*estimated*) on one side where the operator and observer stand behind the net. **The earlier default of ≤ 1.0 m/s with ≥ 0.5 m clearance fails this arithmetic by a wide margin, and many rooms and garages are too small at these limits (Q1).** ET-D5-3's proposed ≥ 0.5 m must be re-proposed at no less than this clearance when D5 is frozen (`AGENTS.md §13.5`).

**Vertical.** At 0.5 m/s, either way: 0.68 m reaction + 0.18 m braking + 0.3 m error (*estimated*; no exit test bounds it) = 1.15 m. Toward the floor that gives a hover of at least 1.2 m. Toward the ceiling, add what stands above the position reference: about 0.35 m on an X500 with its tag box and 0.2 m on a small frame (*estimated*), so 1.5 m and 1.4 m. The minimum ceiling is the sum of the two margins, 2.7 m and 2.6 m, **which rules out a typical 2.44 m garage ceiling**. Setting `COM_OF_LOSS_T` to 0.5 s would bring an X500's minimum to 2.15 m, if D1 confirms it. The command gate holds commanded descent to 0.5 m/s, because PX4's `MPC_Z_VEL_MAX_DN` of 0.7 m/s applies to every climb-rate mode. The 2.5 m cap is carried over: no mission through D6 needs more indoors, and lower flight limits a fall. The 30 m field cap is a choice well inside the 400 ft limit [D29], enough for D3's checkout and easy to keep in unaided sight.

**Sensing range does not set these limits yet.** No stage through D6 uses depth to avoid obstacles while moving, and routes are declared in advance. At 0.5 m/s the stopping distance is well inside the OAK-D Pro's ideal 0.8–12 m range [D21]. A stage that plans from depth must add this term.

**This excludes loss of the estimator,** which the table assumes is good. If VIO fails, the gate's sensor-age check trips within 150 ms and inertial drift follows, by an amount not known. If the Jetson fails, the setpoint stream stops too and offboard loss fires. Solid walls and the net bound both cases. D1 tests both.

**Net layout.** People are excluded from the volume, so a solid wall with no door or window counts as containment. Nets go between the aircraft and the operator bay and across every door, window or open side, floor to ceiling. Panel height follows the ceiling: 10 ft panels up to 3.05 m, 15 ft above that. Panel count is the open length divided by 20 ft, rounded up. Two 10 × 20 ft panels are priced. A space with no solid walls needs four on a floor up to 6.1 m square and six at 8.05 m (`docs/BOM_WORKSHEET.md`). The ceiling must be solid, or the space counts as outdoors. No source gives net strength for a drone (the supplier's tensile field is blank), so a net hit is tested only after D4's first hold. **Whether doors stay closed decides the rest; see Compliance.**

## Failsafes and controls to configure and test in D1 (proposed values)
| Parameter | PX4 default [D23][D24] | Proposed | Why |
|---|---|---|---|
| `MPC_XY_VEL_MAX` | 12 m/s | speed limit for the space | the only horizontal limit that also holds under RC; otherwise full stick commands up to 10 m/s (`MPC_VEL_MANUAL`). The source clamps cruise and manual speed to it, though their metadata minimum is 3 m/s, so D1 must confirm Position mode obeys it. The command gate enforces the same limit on setpoints |
| `MPC_Z_VEL_MAX_UP`, `_DN` | 3, 1.5 m/s | 0.5, 0.7 m/s | vertical limit; the default could climb 3 m on a stale setpoint in 1 s |
| `COM_OF_LOSS_T` | 1.0 s | 1.0 s until D1 measures it | used in the arithmetic |
| `COM_OBL_RC_ACT` | 0 Position | 5 Hold | see the origin row. The docs misname value 2 and omit 5–7, so the source is used |
| EKF global origin | not set | set each indoor session with `SET_GPS_GLOBAL_ORIGIN` | Hold needs global position, and VIO alone gives none [D44]. Without an origin PX4 falls through to Land, which is acceptable but must be known. D1 tests both, with GPS disabled |
| `COM_RC_OVERRIDE` | 1, auto only | 3, auto and offboard | stick override is off in offboard by default |
| `RC_MAP_FLTMODE` | unassigned | assigned, with Position mode on it | takeover needs a switch. Stick override and the mode switch are both tested |
| `RC_MAP_KILL_SW` | 0, unassigned | assigned | no kill switch otherwise; `COM_KILL_DISARM` restarts motors if reverted within 5 s |
| `NAV_RCL_ACT` | 2 Return | 3 Land | Return is wrong indoors |
| `COM_LOW_BAT_ACT` | 0 Warning | 2 Land | with the defaults, nothing enforces the reserve |
| `BAT_LOW_THR`, `BAT_CRIT_THR` | 0.15, 0.07 | 0.30, 0.25 | Land fires at critical, so critical sits at the 25% reserve |
| `EKF2_NOAID_TOUT` | 5 s | 1 s | a shorter time on drift; test for false triggers |
| `COM_POS_FS_EPH` | 5 m | 0.5 m indoors on vision; 5 m on GPS, in SITL and in D3 until measured | 5 m exceeds any room. Position becomes valid below this value and is lost at 2.5 times it, here 1.25 m. It is too tight for GPS, which ET-D3-2 allows 1.0 m RMS. D1 measures EPH and may change it |
| `COM_FAIL_ACT_T` | 5.0 s | test it | the aircraft waits in Hold first, and stick override is not available then. If Hold persists, the operator takes over or uses the kill switch |
| `GF_MAX_HOR_DIST`, `GF_MAX_VER_DIST`, `GF_ACTION` | 0, 0 (off), 2 | 40 m, 30 m, 5 Land; D3 on GPS only | enforces the field cap, and acts only after a breach [D25]. Indoors the net is the containment, because the fence on vision-only position is unverified |

## Energy (estimated)
Holybro states about 18 min hover with no added payload on 5000 mAh [D13]; 75% of that is 13.5 min. Added mass and up to 25 W for the Jetson reduce it by an amount not published. Plan flights of ≤ 8 min until D4 measures it. Never charge unattended; store in the LiPo bag.

## Compliance (rechecked 2026-10-31; recheck before any outdoor stage)
| Item | Plan | Source | Recheck |
|---|---|---|---|
| Part 107 path | Non-recreational flying is regulated by Part 107; development flights are not assumed recreational. Age 16 or over; FAA Tracking Number through IACRA; scheduled knowledge test; form 8710-13; recurrent training every 24 calendar months | [S1][D29][D32] | before D3 |
| Knowledge test | About $175, paid to the test center | [S2] | before booking |
| Registration | $5 per drone, three years, on FAADroneZone. The 250 g exception applies only to recreational flying, so it is not a route here. A registration cannot move between Part 107 and recreational | [S3] | before D3 |
| Remote ID | Registered drones must comply. Route chosen: a broadcast module with its serial on an FAA-accepted declaration, registered per device. A FRIA is also a legal route [S4], but it is not planned, because it ties testing to someone else's fixed site | [S4][D29] | before buying a module; check the FAA list directly [D28] |
| Indoor only | Part 107 does not apply indoors [S5]; the FAA's 2016 wording is "inside an enclosed structure" [D33]. **Open doors and part-enclosed spaces are not settled by any source read, so doors stay closed and an open space counts as outdoors unless the owner decides otherwise (Q1)** | [S5][D33] | before D4 |
| Site permission | Project rule, not an FAA citation: written permission recorded for any site; people excluded from the volume during armed tests | `AGENTS.md §13.7` | each site |
| Visual line of sight | Unaided sight of the aircraft throughout; a broadcast module also requires it. No BVLOS or waiver is assumed. Part 108 is not in force: Final Rule at OIRA since 07/10/2026, not in the eCFR | [D29][D31] | before D3 |
| Altitude, speed | 400 ft AGL and 100 mph limits sit far above this envelope | [D29] | before D3 |
| Operation over people | Prohibited without a stated basis; people are excluded | [D29] | before D3 |
| Radio | One seller says the 915 MHz SiK radio needs an amateur licence in the US. No FCC page was read (Q6) | `docs/BOM_WORKSHEET.md` | before buying |

## Budget status
Both options' planning totals are above the owner's $1,900–2,300 range (`docs/BOM_WORKSHEET.md`, Q7). **No purchase authorization is implied by any document in this repository.**
