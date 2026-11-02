# OPERATING_ENVELOPE.md — D0 deliverable

**Status: decided by the owner on 2026-10-31 for an open outdoor field (`ledgers/approvals.jsonl`); the limits are proposed and *estimated* until D1 to D4 measure them. Recomputed for the X650 by the owner's decision of 2026-11-01 (WO-022), on a simulated proxy. Not a flight authorization:** each arming and flight stage still needs its own dated owner approval (`AGENTS.md §13.2`).

| Decision | Record |
|---|---|
| Mission and site | First mission (D6): fixed-target inspection from N viewpoints and return. A large open field or open space, outdoors. The owner secures access and permission before D2. All flight stages are outdoors |
| Airframe | Holybro X650 ARF: 650 mm, T-Motor MN4014 330KV, Tekko32 F4 45A, Gemfan 1555 carbon props, 6S, about 4–5 kg at takeoff [D64]; Pixhawk 6X on the Holybro Pixhawk Jetson Baseboard, `px4_fmu-v6x_default` (ADR-0007). The X500 V2 is superseded, and no frame swap is planned |
| Horizontal speed | ≤ 2.5 m/s on GPS (D3); ≤ 1.0 m/s on VIO (D4–D6) until measured. `MPC_XY_VEL_MAX` is set per stage, so the limit holds in Position, Hold, Return and offboard. It does not hold in Altitude or Stabilized, so neither is on the mode switch |
| Vertical speed | ≤ 1.0 m/s up; ≤ 0.5 m/s commanded down, enforced by the command gate; landing at PX4's 0.7 m/s |
| Height and wind | ≥ 1.2 m hover. **D3, frozen as a temporary rule by the owner on 2026-11-02 (`evals/D3-temporary-rule-2026-11-02.json`): ≤ 10 m, and handheld wind ≤ 4 m/s.** No later stage raises the cap until the limits are re-derived from measured D3 data, with the ARK Flow MR modelled as the backup velocity source when position is lost. ET-D3-6 and ET-D3-7 collect the data and set the criteria for raising them (`docs/D3_APPROVAL_PACKAGE.md` section 4). The earlier proposal, kept as input to that re-derivation, was, by wind: ≤ 10 m at 5 m/s, 14 m at 4 m/s, 20 m at 3 m/s, 25 m at 2.5 m/s or less. Wind ≤ 5 m/s steady (D3: ≤ 4 m/s), read on a handheld meter at about 1.5 m before each flight: *estimated*, because no published X650 limit was found. Fence ceiling is the stage's height limit plus 4 m: 14 m in D3, never above 30 m. **On the X650 proxy these limits do not meet the 150 m rule at 20 m and 25 m, at 14 m through one tumble, or at 10 m and 5 m/s with shear or a large tumble; the owner chose the D3 rule above** |
| Standoff from obstacles | **Frozen for the X650, 2026-11-01 (`evals/D3-standoffs-x650.json`, replacing `evals/D3-standoffs.json`):** ≥ 8.7 m from the flight box at 2.5 m/s, ≥ 3.4 m at 1.0 m/s, and outside fence plus overrun for anything not expendable. Staked reference cameras are the one exception: they are expendable, and nobody is near them during a run |
| Geofence | Cylinder of 40 m radius, centred on Home, with the ceiling above. Flight box stays within 30 m of Home |
| Crew | Operator and spotter ≥ 85 m from Home and upwind of the flight box, which is outside fence plus overrun and beyond the *estimated* still-air throw of a tumbling prop fragment from the flight box's edge, with the takeoff point in view. Accepted by the owner, 2026-11-02 (was 50 m). Protection rests on that distance and the kill switch |
| Bystander exclusion | **D3: no uninvolved person, road, building or vehicle within 160 m of Home, so the field must be about 320 m across** (owner, 2026-11-02, `evals/D3-temporary-rule-2026-11-02.json`). The derived radius below is 150 m. Part 107 sets no number, so this is the project's rule |
| Containment | Distance plus geofence. No netting. **Distance carries the failures the fence cannot** (below) |
| Sensors | OAK-D Pro W, global-shutter stereo, 150° diagonal, IMU [D62]; ARK Flow MR, downward optical flow and a rangefinder to about 50 m; M10 GPS. **Sunlight behaviour is unresolved; test it in D2** [D54] |
| Compute | Jetson Orin NX 16 GB on the baseboard from D2; JetPack 6.2.2, Ubuntu 22.04, ROS 2 Humble and Isaac ROS 3.2 (owner, 2026-11-02; ADR-0007); hand-carried in D2, flown from D4, so nothing streams offboard before D4 |
| Telemetry | 915 MHz RFD900x-US from D3, by the owner's decision of 2026-11-01, replacing the SiK V3; Wi-Fi will not reach in a field |
| Energy | 6S 10,000 mAh × 3; land at ≥ 25% |
| Human control | Operator on an independent RC link, with kill switch and mode switch assigned, must be able to see the aircraft; a spotter in voice contact. Link and switches tested props off, on the baseboard (ET-D2-5). Takeover, fence and RC loss tested at low height on GPS (ET-D3-5). Takeover and offboard loss tested in D4 (ET-D4-3, ET-D4-4). The fence with GPS aiding off is tested only in SITL |
| Reference (evaluation only) | Two fixed cameras, tag box on the aircraft, independent clock; static RMS target ≤ 2 cm (`docs/REFERENCE_AND_SENSING.md`) |
| Weather | Daylight only; visibility ≥ 3 statute miles; ≥ 500 ft below and 2,000 ft from clouds [D29] |
| Data and privacy | Test volume only; faces excluded or blurred; retention per `docs/DATA_POLICY.md`; GPS stripped from anything shared |

## How the limits were derived
The standoff's braking term, the overrun and the position-lost reach are measured in SITL: on the X500 in WO-004, and on a proxy of the X650 in WO-022. Everything else here is estimated until flight logs replace it. **The proxy is PX4's x500 model with mass, arm length and thrust set from published figures, and drag, inertia and motor lag scaled or estimated** (`src/banshee/sitl/x650_proxy.py`).

Standoff = reaction distance + braking distance + peak position error.
- **Braking, as first estimated:** jerk-limited, `d = v·√(v/j)` for v ≤ a²/j = 2.25 m/s, otherwise `d = v·(v/a + a/j)/2`, with PX4 defaults a = 3 m/s² (`MPC_ACC_HOR`) and j = 4 m/s³ (`MPC_JERK_AUTO`) [D24]. No page read said these govern Hold braking, and D1 measured more: 3.0–3.2 m from 2.5 m/s against 1.98 m, and 0.93–1.02 m from 1.0 m/s against 0.50 m, net of 0.2 s of reaction (H-01, H-02, K-01, K-02). On the X650 proxy, net of the same 0.2 s: 3.01–3.26 m from 2.5 m/s (5 kg, 4 kg and half drag) and 0.90–1.04 m from 1.0 m/s (5 kg). So mass barely moved it, which is expected: PX4's limit is an acceleration, and 3 m/s² needs a thrust-to-weight of only about 1.05. The proxy has about 2.4:1, which is estimated; a lower margin was not run. The table uses the proxy's values, rounded up.
- **Reaction, worst case:** 1.35 s. That is 1.0 s for PX4's default `COM_OF_LOSS_T` [D23], plus the frozen setpoint (200 ms) and sensor (150 ms) age bounds that can run before the link is lost. The last setpoint may be applied throughout, which D1 tests.
- **Peak position error:** twice the RMS bound, an assumption that flight logs replace. GPS: 2 × 1.0 m (ET-D3-2). VIO moving: 2 × 0.5 m (ET-D5-1).

| Speed | Reaction | Braking | Error | Standoff |
|---:|---:|---:|---:|---:|
| 1.0 m/s (VIO) | 1.35 m | 1.05 m | 1.0 m | **3.4 m** |
| 2.5 m/s (GPS) | 3.38 m | 3.3 m | 2.0 m | **8.7 m** |

The 8.7 m case sets the standoff, and rounded up to 9 m it sets the fence's overrun margin, as on the X500 (8.6 m and 3.35 m, `evals/D3-standoffs.json`). The measured fence overrun at 2.5 m/s is 3.28–3.67 m on the proxy and 3.82–3.94 m on the X500 (G-01). ET-D5-3's ≥ 0.5 m clearance must be re-proposed at no less than this, excluding the staked reference cameras, when D5 is frozen (`AGENTS.md §13.5`).

**Exclusion radius** = fence radius + overrun margin + a bystander distance = 40 + 9 + 100 m = 149 m, rounded up to 150 m. **Part 107 sets no stand-off** [D56], so the owner sets this number. The 100 m is PX4's first-flight rule of thumb [D40], which names no mass.

**What the 15-inch carbon props and the mass change, *estimated*, with no test.** A tumbling 2–15 g fragment thrown at up to 140 m/s from 25 m lands within about 55 m in still air and 79 m downwind at 5 m/s (quadratic drag, with an assumed area; 330 KV on 6S gives about 8,300 rpm unloaded, 140 m/s at the tip being a loaded figure). **This supports "tens of metres", and it is not a bound:** halving the assumed area gives about 95 m in still air and 121 m in wind, and a chip flying stably edge-on could go 300 m or more in the same model, which is not credible for a tumbling piece but is not excluded. From the flight box's edge the still-air figure reaches 85 m, which is why the crew is at 85 m and upwind, accepted by the owner on 2026-11-02. The aircraft carries about twice the X500's energy: 687 J falling from the 14 m ceiling at 5 kg. No rule read scales a distance by this, so the distances rest on keeping people out, and not on surviving an impact. For comparison, the EU's A3 category uses 150 m and Canada uses 30 m (foreign rules, for reference only). If the field is smaller, shrink the fence by the same amount; keep R + 109 m; in D3, R + 120 m. **In D3 the radius is 160 m by the owner's temporary rule,** which covers the position-lost cases measured in WO-022 at 10 m.

**Why distance has to carry the failure cases.** Read from v1.17.0 source, not run, so D1 tests each:
- The cylinder is centred on Home, not on the field, so moving the takeoff point moves the fence. It **passes silently if Home is invalid**, so `COM_ARM_WO_GPS` is set to deny arming, which also requires a valid global position.
- It has no check that the position is fresh, so it can pass on stale data. On GPS loss, Position mode falls back to Altitude mode, which does not hold position, and the aircraft holds altitude until the operator commands a descent, then drifts while it comes down: wind × (height ÷ 0.7 m/s + 5 s of operator reaction) (*estimated*). WO-004 measured a further term with no wind, for speed carried into the loss: 12.5–13.1 m from 2.5 m/s (G-04). It also measured that the fence does not act once position is lost (G-04, W-01), so nothing but distance contains this case. On the X650 proxy G-04 gives 12.4–12.8 m at 5 kg, 12.3–12.5 m at 4 kg and 15.2–17.2 m at half drag, but at 5 m the ground cuts it short with the aircraft still moving, and the proxy's drag is scaled to match the x500 at every mass, so the agreement between masses is built in. The table below measures it at each height instead.

**The owner's rule, 2026-11-01: the 150 m exclusion radius covers position-lost cases on its own. On the proxy the rule is not met at 20 m and 25 m at nominal drag, nor at 14 m through one tumble at double drag. At 10 m and 5 m/s it is met only in uniform wind with no large tumble. The owner chose option A+ for D3 on 2026-11-02: 10 m, 4 m/s and 160 m (`evals/D3-temporary-rule-2026-11-02.json`).** Measured directly at each row of the height and wind table: position lost about 32 m out (the 30 m flight box plus 2 m of position error), flying downwind at 2.5 m/s. Reach is from Home to the end of the ground slide, in simulation, in uniform wind from one direction. The last two columns add 5 s of operator delay, *estimated* per run as 5 s × the larger of the wind and the speed at touchdown.

| Wind, height | Nominal drag | Half drag | Double drag | Nominal, with delay | Worst, with delay |
|---|---:|---:|---:|---:|---:|
| 5 m/s, 10 m | 89.3–99.8 m | 82.4–90.2 m | 102.2–113.9 m | 125.2 m | **140.3 m, inside** |
| 4 m/s, 14 m | 106.2–108.7 m | 97.6–112.7 m | 108.2–149.6 m | 131.0 m | **172.7 m, past 150 m** |
| 3 m/s, 20 m | 117.6–131.6 m | 116.0–123.7 m | 121.6–135.7 m | **151.6 m, past** | **154.8 m, past 150 m** |
| 2.5 m/s, 25 m | 132.1–143.4 m | 127.5–144.2 m | 128.6–137.6 m | **162.9 m, past** | **162.9 m, past 150 m** |

The 172.7 m comes from one 35 m slide after a tumble; simulated ground contact is not validated. **The formula `wind × (height ÷ 0.7 + 5 s)` is not a bound.** The proxy outran the wind at the lower winds, up to 3.9 m/s in 2.5 m/s of wind, mostly across the wind: true tilt grew to 1.3° late in the descent in the run checked, while the estimator read about 0.02°. The cause of the tilt is not established. So "downwind" is not the worst case: other wind directions were not run, and if the side drift lined up with the wind, the estimate adds about 24 m at 25 m, 11 m at 20 m and 1–2 m at 10 m. **Wind shear and a large tumble are not in the 10 m row either:** the limit is read near the ground, and a 1/7 power law gives 1.15–1.31 times that wind averaged over the descent (*estimated*), which takes that row to about 143 m at nominal drag and 161 m at double drag; a 35 m slide there gives about 160 m (*estimated*). Position loss at the fence's edge starts about 17 m further out, and it is a second failure. The options are in `reports/WO-022-x650-envelope-and-d2-tests.md`. D2 flies nothing, so this does not hold up D2. The owner settled it for D3 on 2026-11-02: option A+, 10 m, 4 m/s and 160 m (`evals/D3-temporary-rule-2026-11-02.json`). The stage's height and wind limits are part of the rule, because the drift scales with both. A height excursion to the fence ceiling on top of GPS loss is a second failure and can go further, and the operator's kill switch is the last control.
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
Holybro states 30 min hover on 6S 10,000 mAh with no added payload, a 2,000 g kit and a 1,200 g pack [D64]. Scaling hover power with mass to the power 1.5, 5 kg gives about 15 min, and 75% of that is about 11.5 min, before up to 25 W for the Jetson. Plan flights of ≤ 8 min until logs measure it. Never charge unattended; carry and store in the fire-safe box, for which the final list proposes the BAT-SAFE XXL, 777 Wh combined, line 16 of `docs/BUY_LIST-FINAL-2026-11-02.md`, approved 2026-11-02.

## Compliance (rechecked 2026-10-31; recheck before D3 and before buying)
| Item | Plan | Source | Recheck |
|---|---|---|---|
| Part 107 path | Non-recreational flying is regulated by Part 107. Age 16 or over; FAA Tracking Number through IACRA; scheduled knowledge test; form 8710-13; recurrent training every 24 calendar months. **No Part 107 flight until the owner holds a certificate, or a certificated remote pilot directly supervises with immediate takeover** (107.12) | [S1][D29][D32] | before D3 |
| Knowledge test | About $175, paid to the test center | [S2] | before booking |
| Registration | $5 per drone, three years, on FAADroneZone, with the number marked on the aircraft. The 250 g exception applies only to recreational flying | [S3] | before D3 |
| Remote ID | Registered drones must comply. Route: a broadcast module with its serial on an FAA-accepted declaration, registered per device. A FRIA is also a legal route [S4], but it is not planned, because it ties testing to someone else's site. A module serial can be on only one registration at a time, which would matter at a frame swap [D55] | [S4][D29][D55] | before buying; check the FAA list directly [D28] |
| Line of sight and spotter | Unaided sight throughout. The owner's spotter is stricter than the rule (a visual observer is optional, 107.33), and does not replace the operator: with a broadcast module, the person on the controls must be able to see the aircraft at all times (89.115). Effective communication at all times | [D29][D56] | before D3 |
| Airspace | Prior authorization in Class B, C, D and surface Class E (107.41), through LAANC where available; manual requests can take up to eight weeks. Check NOTAMs and restrictions each time. Cannot be checked until a site is named | [D56] | each site |
| Preflight | Remote pilot assesses weather, airspace, people, property and ground hazards, and briefs participants (107.49). Remote pilot in command is designated and answers for no undue hazard on loss of control (107.19) | [D56] | each flight |
| Altitude, speed, visibility | 400 ft AGL, 100 mph, 3 statute miles, cloud clearance (107.51); this envelope sits inside them. Daylight only, so no anti-collision light (107.29) | [D29][D56] | before D3 |
| Operation over people | Prohibited without a stated basis (107.39); people are excluded | [D29] | before D3 |
| Indoor only | Part 107 does not apply indoors [S5]. Not relied on: all flight stages are outdoors (owner, 2026-10-31) | [S5] | if the site changes |
| Site permission | Project rule: written permission recorded before D2; the owner secures it | `AGENTS.md §13.7` | each site |
| 915 MHz radio | **Rule:** no individual licence is needed under 47 CFR 15.1(a) for a certified, compliant device, and 100 mW is under every 15.247 power limit for 902–928 MHz (1 W with at least 50 hopping channels, 0.25 W with 25–49), though hop-channel and occupancy rules still apply and only the authorized antenna may be used (15.204). **This unit:** Holybro publishes FCC ID 2AP22-HT03-V3, and archived filings show a unit labelled 915 MHz 100 mW. **Corrected by the owner, 2026-11-01:** their closure earlier that day was wrong. FCC ID 2AP22-HT03-V3 was certified under 15.249, the low-power rule, not 15.247; test report SZAWW180522002-01 measured about 82 dBµV/m at 3 m. At 100 mW this radio operates outside its grant, so RMRC's licence note stands, and line 5 is withdrawn. The rule above does not cover it. **Substitute at D3:** RFDesign RFD900x-US bundle, FCC ID 2ADLE-900X, 15.247. All of this is the owner's reading ([fccid.io/2AP22-HT03-V3](https://fccid.io/2AP22-HT03-V3) returns 403 to automated reads). The substitute's grant date is not on record, so check it against the 2025-12-22 cutoff at the D3 approval | [D58] [D61] | D3 approval |
| mRo as a source | **Not supported.** Its store redirects to 3DR, whose kit is "for evaluation only; not FCC approved for resale", whose kits "do not possess an FCC ID", and whose pages state no US manufacture. Buy the Holybro unit, which has an FCC ID | [D59] | before buying |
| FCC Covered List | Planning check on every line, in `docs/BOM_WORKSHEET.md`. Not legal advice. Flags are per line in `docs/BUY_LIST-FINAL-2026-11-02.md`; line 2 was cleared by the owner on 2026-11-02. | [D50] | before buying |

## Budget status
The final list is `docs/BUY_LIST-FINAL-2026-11-02.md`. **Lines 1, 2, 4, 11–18, 23, 28 and 29 approved by the owner, 2026-11-02; line 31 on hold.**
