# OPERATING_ENVELOPE.md — D0 deliverable

**Status: decided by the owner on 2026-10-31 for an open outdoor field (`ledgers/approvals.jsonl`); the limits are proposed and *estimated* until D1 to D4 measure them. Not a flight authorization:** each arming and flight stage still needs its own dated owner approval (`AGENTS.md §13.2`).

| Decision | Record |
|---|---|
| Mission and site | First mission (D6): fixed-target inspection from N viewpoints and return. A large open field or open space, outdoors. The owner secures access and permission before D2. All flight stages are outdoors |
| Airframe | Holybro X500 V2, about 1 kg payload [D13]; Pixhawk 6X, `px4_fmu-v6x_default` (ADR-0007). Planned D7+: an X650-class 6S airframe with the same autopilot and stack |
| Horizontal speed | ≤ 2.5 m/s on GPS (D3); ≤ 1.0 m/s on VIO (D4–D6) until measured. `MPC_XY_VEL_MAX` is set per stage, so the limit holds in Position, Hold, Return and offboard. It does not hold in Altitude or Stabilized, so neither is on the mode switch |
| Vertical speed | ≤ 1.0 m/s up; ≤ 0.5 m/s commanded down, enforced by the command gate; landing at PX4's 0.7 m/s |
| Height and wind | ≥ 1.2 m hover. **All of D3, until logs replace the estimate: ≤ 10 m.** After that, by wind: ≤ 10 m at 5 m/s, 14 m at 4 m/s, 20 m at 3 m/s, 25 m at 2.5 m/s or less. Wind ≤ 5 m/s steady, read on a handheld meter before each flight: *estimated*, because no published X500 limit was found. Fence ceiling is the stage's height limit plus 4 m: 14 m in D3, never above 30 m |
| Standoff from obstacles | **Frozen by the owner, 2026-11-01 (`evals/D3-standoffs.json`):** ≥ 8.6 m from the flight box at 2.5 m/s, ≥ 3.35 m at 1.0 m/s, and outside fence plus overrun for anything not expendable. Staked reference cameras are the one exception: they are expendable, and nobody is near them during a run |
| Geofence | Cylinder of 40 m radius, centred on Home, with the ceiling above. Flight box stays within 30 m of Home |
| Crew | Operator and spotter ≥ 50 m from Home, outside fence plus overrun, with the takeoff point in view. Protection rests on that distance and the kill switch |
| Bystander exclusion | No uninvolved person, road, building or vehicle within 150 m of Home, so the field must be about 300 m across. Part 107 sets no number, so this is the project's rule |
| Containment | Distance plus geofence. No netting. **Distance carries the failures the fence cannot** (below) |
| Sensors | OAK-D Pro, global-shutter stereo, IMU [D21]; M10 GPS. **Sunlight behaviour is unresolved; test it in D2** [D54] |
| Compute | Jetson Orin Nano Super 8 GB from D2, bought after D1 passes; hand-carried in D2, flown from D4, so nothing streams offboard before D4 |
| Telemetry | 915 MHz SiK, 100 mW; Wi-Fi will not reach in a field |
| Energy | 4S 5200 mAh × 3; land at ≥ 25% |
| Human control | Operator on an independent RC link, with kill switch and mode switch assigned, must be able to see the aircraft; a spotter in voice contact. Link and switches tested props off (ET-D2-5). Takeover, fence and RC loss tested at low height on GPS (ET-D3-5). Takeover and offboard loss tested in D4 (ET-D4-3, ET-D4-4). The fence with GPS aiding off is tested only in SITL |
| Reference (evaluation only) | Two fixed cameras, tag box on the aircraft, independent clock; static RMS target ≤ 2 cm (`docs/REFERENCE_AND_SENSING.md`) |
| Weather | Daylight only; visibility ≥ 3 statute miles; ≥ 500 ft below and 2,000 ft from clouds [D29] |
| Data and privacy | Test volume only; faces excluded or blurred; retention per `docs/DATA_POLICY.md`; GPS stripped from anything shared |

## How the limits were derived
The standoff's braking term is measured in SITL (WO-004). Everything else here is estimated until flight logs replace it.

Standoff = reaction distance + braking distance + peak position error.
- **Braking, as first estimated:** jerk-limited, `d = v·√(v/j)` for v ≤ a²/j = 2.25 m/s, otherwise `d = v·(v/a + a/j)/2`, with PX4 defaults a = 3 m/s² (`MPC_ACC_HOR`) and j = 4 m/s³ (`MPC_JERK_AUTO`) [D24]. No page read said these govern Hold braking, and D1 measured more: 3.0–3.2 m from 2.5 m/s against 1.98 m, and 0.93–1.02 m from 1.0 m/s against 0.50 m, net of 0.2 s of reaction (H-01, H-02, K-01, K-02). The table uses the measured values.
- **Reaction, worst case:** 1.35 s. That is 1.0 s for PX4's default `COM_OF_LOSS_T` [D23], plus the frozen setpoint (200 ms) and sensor (150 ms) age bounds that can run before the link is lost. The last setpoint may be applied throughout, which D1 tests.
- **Peak position error:** twice the RMS bound, an assumption that flight logs replace. GPS: 2 × 1.0 m (ET-D3-2). VIO moving: 2 × 0.5 m (ET-D5-1).

| Speed | Reaction | Braking | Error | Standoff |
|---:|---:|---:|---:|---:|
| 1.0 m/s (VIO) | 1.35 m | 1.0 m | 1.0 m | **3.35 m** |
| 2.5 m/s (GPS) | 3.38 m | 3.2 m | 2.0 m | **8.6 m** |

The 8.6 m case sets the standoff, and rounded up to 9 m it sets the fence's overrun margin. These replace 7.35 m and 2.85 m. The measured fence overrun at 2.5 m/s is 3.82–3.94 m (G-01). ET-D5-3's ≥ 0.5 m clearance must be re-proposed at no less than this, excluding the staked reference cameras, when D5 is frozen (`AGENTS.md §13.5`).

**Exclusion radius** = fence radius + overrun margin + a bystander distance = 40 + 9 + 100 m = 149 m, rounded up to 150 m. **Part 107 sets no stand-off** [D56], so the owner sets this number. The 100 m is PX4's first-flight rule of thumb [D40]. For comparison, the EU's A3 category uses 150 m and Canada uses 30 m (foreign rules, for reference only). If the field is smaller, shrink the fence by the same amount; keep R + 109 m.

**Why distance has to carry the failure cases.** Read from v1.17.0 source, not run, so D1 tests each:
- The cylinder is centred on Home, not on the field, so moving the takeoff point moves the fence. It **passes silently if Home is invalid**, so `COM_ARM_WO_GPS` is set to deny arming, which also requires a valid global position.
- It has no check that the position is fresh, so it can pass on stale data. On GPS loss, Position mode falls back to Altitude mode, which does not hold position, and the aircraft holds altitude until the operator commands a descent, then drifts while it comes down: wind × (height ÷ 0.7 m/s + 5 s of operator reaction) (*estimated*). WO-004 measured a further term with no wind, for speed carried into the loss: 12.5–13.1 m from 2.5 m/s (G-04). It also measured that the fence does not act once position is lost (G-04, W-01), so nothing but distance contains this case.

**The owner's rule, 2026-11-01: the 150 m exclusion radius covers position-lost cases on its own.** The arithmetic behind it, *estimated*:

| Start of the drift | Carried speed | Drift at the table's height and wind limits | Reaches |
|---|---:|---:|---:|
| Flight box edge, 30 m out: position loss alone | 13.1 m | 96.4–101.8 m | **139.5–144.9 m, inside 150 m** |
| Fence plus overrun, 49 m out: position loss on top of a fence breach | 13.1 m | 96.4–101.8 m | **158.5–163.9 m, past 150 m** |

So the rule holds for position loss alone, by 5 m at the least. Position loss at the fence's edge is a second failure, like the height excursion below, and it can pass 150 m by up to 14 m. The measured drifts sit well inside this: 41.5–46.1 m in 5.4 m/s of wind from 10 m, with no operator delay (W-01). The stage's height and wind limits are part of the rule, because the drift scales with both. A height excursion to the fence ceiling on top of GPS loss is a second failure and can go further, and the operator's kill switch is the last control.
- `GF_ACTION` 4 (Terminate) appears to be a live motor kill: the circuit breaker the safety page cites does not gate it. It is not used.
- Return mode's climb is not clamped to the fence, so `RTL_RETURN_ALT` sits below the ceiling and at the stage's height limit.
- With `GF_SOURCE` 1 the fence compares raw GPS with a Home that follows the estimator, so a wrong global origin moves its centre and ceiling without tripping anything: an origin 100 m too high would put the 30 m ceiling at 130 m. In VIO stages the origin is set from a checked GPS fix at the takeoff point, and the crew compares raw GPS with Home before arming (5 m horizontal, 10 m vertical; *estimated*).

**Sensing range does not set these limits yet.** No stage through D6 uses depth to avoid obstacles while moving, and routes are declared in advance. A stage that plans from depth must add this term.

## Failsafes and controls to configure and test in D1 (proposed values)
| Parameter | PX4 default [D23][D24][D57] | Proposed | Why |
|---|---|---|---|
| `GF_MAX_HOR_DIST`, `GF_MAX_VER_DIST` | 0, 0 (off) | 40 m; 14 m in D3, then the stage's height limit plus 4 m, never above 30 m | the fence is off by default |
| `GF_ACTION` | 2 Hold | 5 Land | Land works without a good position; Hold does not |
| `GF_SOURCE` | 0 estimator | 1 raw GPS | the fence uses GPS coordinates during VIO stages. It still needs a live receiver and a global position from the estimator, and code reads no staleness check, so it is not fully independent of the estimator |
| `EKF2_GPS_CTRL` | GPS aiding on | 0 in VIO stages, receiver left powered | turns off aiding only. Never `SYS_HAS_GPS` 0, which stops the receiver and with it the fence |
| `COM_ARM_WO_GPS` | 1 warning only | 0 deny arming | Home must be valid, or the fence passes silently |
| `RTL_RETURN_ALT`, `RTL_DESCEND_ALT` | 30, 10 m on this airframe | 10, 10 m in first flights; never above the stage's height limit | stays under the ceiling and inside the drift limit; confirm with a parameter dump, because the docs say 60 and 30 m |
| `NAV_RCL_ACT` | 2 Return | 2 Return | right outdoors on GPS; RC lost during VIO-only tests is a D1 case |
| `NAV_DLL_ACT` | 0 disabled; **2 Return on the SITL airframe `gz_x500`** | 0 disabled, set explicitly in D1 too | RC is the safety link; telemetry loss alone does not end a flight |
| `MPC_XY_VEL_MAX` | 12 m/s | 2.5 m/s on GPS; 1.0 m/s on VIO | holds in Position, Return and offboard, where full stick is otherwise up to 10 m/s. **PX4 also rewrites `MPC_XY_CRUISE` and `MPC_VEL_MANUAL` down to it, and raising it later does not restore them**, so reset them when moving between stages, and check them in the parameter dump. D1 confirms the speeds |
| `MPC_Z_VEL_MAX_UP`, `_DN` | 3, 1.5 m/s | 1.0, 0.7 m/s | vertical limit |
| `COM_OF_LOSS_T` | 1.0 s | 1.0 s until D1 measures it | used in the arithmetic |
| `COM_OBL_RC_ACT` | 0 Position | 5 Hold | works on GPS. Without GPS aiding it needs a global origin set with `SET_GPS_GLOBAL_ORIGIN` [D44]; arming is refused without one. If global position is lost after arming, PX4 falls through to Land, which is acceptable but must be known |
| `COM_RC_OVERRIDE` | 1, auto only | 3, auto and offboard | stick override is off in offboard by default |
| `RC_MAP_FLTMODE` | unassigned | assigned, with Position mode on it | takeover needs a switch |
| `RC_MAP_KILL_SW` | 0, unassigned | assigned | no kill switch otherwise; `COM_KILL_DISARM` restarts motors if reverted within 5 s |
| `RC_CRSF_PRT_CFG` | unset | the receiver's port | CRSF is built in on the 6X, but its port is not configured |
| `COM_LOW_BAT_ACT` | 0 Warning | 3 Return at critical, land at emergency | with the defaults, nothing enforces the reserve |
| `BAT_LOW_THR`, `BAT_CRIT_THR`, `BAT_EMERGEN_THR` | 0.15, 0.07, 0.05 | 0.40, 0.35, 0.15 | Return starts below critical and costs about 5–8 points of charge (*estimated*, no payload), so critical sits above the 25% reserve. Logs replace this |
| `EKF2_NOAID_TOUT` | 5 s | 1 s | a shorter time on drift; test for false triggers |
| `COM_POS_FS_EPH` | 5 m | 5 m on GPS; 0.5 m on vision until measured | position becomes valid below this value and is lost at 2.5 times it. D1 measures EPH |
| `COM_FAIL_ACT_T` | 5.0 s | test it | the aircraft waits in Hold first, and stick override is not available then |
| Wind limit | `COM_WIND_MAX` −1 (off) | the handheld reading before each flight | PX4's check needs `COM_WIND_MAX_ACT` and drag fusion, neither set here, and has no airspeed sensor to use, so it is not relied on |

## Energy (estimated)
Holybro states about 18 min hover with no added payload on 5000 mAh [D13]; 75% of that is 13.5 min. Added mass and up to 25 W for the Jetson reduce it by an amount not published. Plan flights of ≤ 8 min until logs measure it. Never charge unattended; carry and store in the fire-safe box.

## Compliance (rechecked 2026-10-31; recheck before D3 and before buying)
| Item | Plan | Source | Recheck |
|---|---|---|---|
| Part 107 path | Non-recreational flying is regulated by Part 107. Age 16 or over; FAA Tracking Number through IACRA; scheduled knowledge test; form 8710-13; recurrent training every 24 calendar months. **No Part 107 flight until the owner holds a certificate, or a certificated remote pilot directly supervises with immediate takeover** (107.12) | [S1][D29][D32] | before D3 |
| Knowledge test | About $175, paid to the test center | [S2] | before booking |
| Registration | $5 per drone, three years, on FAADroneZone, with the number marked on the aircraft. The 250 g exception applies only to recreational flying | [S3] | before D3 |
| Remote ID | Registered drones must comply. Route: a broadcast module with its serial on an FAA-accepted declaration, registered per device. A FRIA is also a legal route [S4], but it is not planned, because it ties testing to someone else's site. A module serial can be on only one registration at a time, which matters at the X650 swap [D55] | [S4][D29][D55] | before buying; check the FAA list directly [D28] |
| Line of sight and spotter | Unaided sight throughout. The owner's spotter is stricter than the rule (a visual observer is optional, 107.33), and does not replace the operator: with a broadcast module, the person on the controls must be able to see the aircraft at all times (89.115). Effective communication at all times | [D29][D56] | before D3 |
| Airspace | Prior authorization in Class B, C, D and surface Class E (107.41), through LAANC where available; manual requests can take up to eight weeks. Check NOTAMs and restrictions each time. Cannot be checked until a site is named | [D56] | each site |
| Preflight | Remote pilot assesses weather, airspace, people, property and ground hazards, and briefs participants (107.49). Remote pilot in command is designated and answers for no undue hazard on loss of control (107.19) | [D56] | each flight |
| Altitude, speed, visibility | 400 ft AGL, 100 mph, 3 statute miles, cloud clearance (107.51); this envelope sits inside them. Daylight only, so no anti-collision light (107.29) | [D29][D56] | before D3 |
| Operation over people | Prohibited without a stated basis (107.39); people are excluded | [D29] | before D3 |
| Indoor only | Part 107 does not apply indoors [S5]. Not relied on: all flight stages are outdoors (owner, 2026-10-31) | [S5] | if the site changes |
| Site permission | Project rule: written permission recorded before D2; the owner secures it | `AGENTS.md §13.7` | each site |
| 915 MHz radio | **Rule:** no individual licence is needed under 47 CFR 15.1(a) for a certified, compliant device, and 100 mW is under every 15.247 power limit for 902–928 MHz (1 W with at least 50 hopping channels, 0.25 W with 25–49), though hop-channel and occupancy rules still apply and only the authorized antenna may be used (15.204). **This unit:** Holybro publishes FCC ID 2AP22-HT03-V3, and archived filings show a unit labelled 915 MHz 100 mW. **Not settled:** the grant could not be read, so its date, rule part and antennas are unverified, and one seller still says a licence is required, giving no reason specific to this product. The finding supports the owner's expectation, but read the grant or the unit's label before relying on it | [D58] | before buying |
| mRo as a source | **Not supported.** Its store redirects to 3DR, whose kit is "for evaluation only; not FCC approved for resale", whose kits "do not possess an FCC ID", and whose pages state no US manufacture. Buy the Holybro unit, which has an FCC ID | [D59] | before buying |
| FCC Covered List | Planning check on every line, in `docs/BOM_WORKSHEET.md`. Not legal advice. Five lines are flagged, and grant dates need reading | [D50] | before buying |

## Budget status
Option A's planning total is above the owner's $1,900–2,300 range (`docs/BOM_WORKSHEET.md`). **No purchase is authorized (owner, 2026-10-31).**
