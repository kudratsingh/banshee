# ADR-0007 — D0 airframe, flight controller, stack and compute

**Date:** 2026-10-31 · **Status:** accepted on the owner's decisions of 2026-10-31 (`ledgers/approvals.jsonl`); nothing here is purchased or tested · **Work order:** WO-001 · **Program link:** PROGRAM §5.1, §12

## Context
D0 must settle a platform and a software stack to test in D1, with no purchase and no hardware. Sources are in `docs/SOURCES.md` and `docs/SOURCES-D0.md`; nothing here has been installed, run or flown.

Findings that shaped this:
- PX4 v1.17's documentation states ROS 2 Humble on Ubuntu 22.04 [D2], not the Jazzy on 24.04 the kit assumed. Jazzy on 24.04 is stated only on the main-branch guide [D3].
- A camera on a flying aircraft cannot reach a laptop over USB, so flying VIO needs onboard compute.
- PX4's default `px4_fmu-v6c` build has no CRSF RC input, and the `px4_fmu-v6x` and `ark_fmu-v6x` defaults do [D49].

## Decision
Items 1, 4, 5 and the telemetry radio are the owner's decisions. The flight controller follows the owner's stated rule. The stack stays proposed until WO-002 tests it.

1. **Test space and airframe.** A large open field, outdoors, and a Holybro X500 V2. An X650-class 6S airframe is the planned D7+ mission platform, with the same autopilot and stack; the D7 list is a frame, motor, ESC and battery swap. No QAV250; Option B is not needed.
2. **Flight controller: Holybro Pixhawk 6X, target `px4_fmu-v6x_default`.** The comparison is below and in `docs/BOM_WORKSHEET.md`. The owner's lean is to standardize on FMUv6X and the Pixhawk Autopilot Bus, and to prefer ARKV6X if the total stays within about $300 of the 6C plan. ARKV6X with an ARK carrier is +$622.01 in parts against the 6C at Holybro and +$566.05 against the RMRC plan the owner reviewed, so the preference does not trigger.
3. **Stack.** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, PX4 v1.17.0, Micro-XRCE-DDS-Agent v2.4.3, `px4_msgs` at `release/1.17`, QGroundControl v5.1.5. Exact commits are in `config/stack-lock.proposed.json`. Humble on 22.04 is the fallback if WO-002 cannot run this. Jazzy comes first, though the v1.17 guide says Humble, because:
   - Humble's support ends in May 2027 [D11], inside the expected life of D1–D4.
   - Gazebo recommends Jazzy with Harmonic and marks Humble with Harmonic "use with caution" [D10].
   - QGroundControl's AppImage has no 22.04 build [D9].
   - PX4's agent table lists v2.4.3 for Jazzy [D6].

   The risk is that this pairing is assembled from separate pages, and that is exactly what WO-002's first test checks.
4. **Compute.** Jetson Orin Nano Super 8 GB from D2, bought after D1 passes. The owner specified $249 from a listed partner; **NVIDIA's list price is now $399** (`docs/BOM_WORKSHEET.md`), so the plan carries $399. NVMe drive, 12 V BEC, TELEM2 cable and printed mount are added; fit on the platform board is resolved in D2.
5. **Camera.** OAK-D Pro. Its behaviour in direct sun is unresolved and is tested in D2 [D54].
6. **VIO.** Isaac ROS Visual SLAM 4.6.0 for bench evaluation in D2, on the Jetson, which needs JetPack 7.2 and an NVMe drive [D46]. BasaltVIO on the OAK is the second candidate. Neither is chosen for flight until D2 measures it. PX4's frames and a global origin are handled as `docs/OPERATING_ENVELOPE.md` says [D43][D44].
7. **Companion link.** TELEM2 by UART first. A reported JetPack 7 fault on UART1 TX has no confirmed fix [D52]; the 6X's Ethernet is the alternative, and D2 tests whichever works.
8. **RC link.** RadioMaster TX16S with an ELRS receiver over CRSF, which is in the 6X's default build, so no custom firmware is needed. Its port must be configured. Takeover and the kill switch depend on this link, so D2 tests it props off. PX4's CRSF page still says no default firmware includes it, which the board files and release image contradict, so D2 confirms it on the bench. Both radio parts are flagged in the FCC check.
9. **Telemetry.** 915 MHz SiK, 100 mW, from Holybro, which publishes an FCC ID. The finding on licensing is in `docs/OPERATING_ENVELOPE.md`. mRo is not a suitable source [D59].

### Flight controller comparison
| | Pixhawk 6C | **Pixhawk 6X (chosen)** | ARKV6X + ARK carrier |
|---|---|---|---|
| With power module and M10 | $271.98 | $466.98 | $893.99 |
| Parts against the 6C at Holybro; against the RMRC plan | — | +$195.00; +$139.04 | +$622.01; +$566.05 |
| FCC Covered List | candidate: SDoC 2022-07-19 | candidate: SDoC 2022-07-19; may not cover Rev 8 | module exempt if still listed, until 2028-01-01; carrier and power module have no Framework row |
| PX4 target | `px4_fmu-v6c_default` | `px4_fmu-v6x_default` | `ark_fmu-v6x_default` |
| CRSF in the default build | no | yes; 6,160 bytes free | yes; 41,180 bytes free |
| IMUs | 2 | 3 | 3 |
| X500 mounting | sold as a kit | sold as a kit | none documented |
| 6S 650-class at D7 | documented | documented | in range; not documented |

A 6X and an ARKV6X are interchangeable at the hardware level (Pixhawk Autopilot Bus), but not in firmware: the board id, defaults and PWM channel count differ, so a swap means a reflash and recalibration. **An ARKV6X on a Holybro Mini baseboard, +$292.00 or +$236.04, is within the owner's $300.** It was not chosen, because the combination is undocumented and half of it stays Holybro. The owner can overrule this with one line, and it stays available later by swapping the module.

## Alternatives considered
| Option | Why not (or why not yet) |
|---|---|
| Humble on 22.04, the pairing the v1.17 guide states | kept as the fallback; support ends May 2027 and QGC needs a self-build |
| PX4 v1.18.0-rc1, or main | a pre-release; pins must not move with an unreleased branch |
| Agent v3.0.2, the repository's latest | PX4's docs say v3.x is not compatible [D6] |
| OpenVINS | GPL-3.0; Jazzy pull requests still open; last release 2023 [D27] |
| VINS-Fusion, ORB-SLAM3 | ROS 2 ports target Foxy or Humble; GPL; no Jazzy branch |
| RTAB-Map as VIO | maintained on Jazzy with a BSD license, but its stock odometry is not documented as tightly coupled VIO |
| Spectacular AI | its ROS node needs a commercial SDK |
| Pixhawk 6C | cheaper, but needs a custom build for CRSF, has two IMUs and no Ethernet, and is not the owner's lean |
| Laptop through D4 | no USB in flight |

## D1 verification plan (for WO-002)
| Pin | Test | Pass |
|---|---|---|
| Ubuntu 24.04 | build in a VM or container on the owner's Mac; record the image | builds from a clean start twice |
| PX4 v1.17.0 | check out `d6f12ad1`, `make px4_sitl gz_x500` | starts and reports that commit |
| Target | `make px4_fmu-v6x_default` at the same commit, compile only; no hardware | builds |
| Gazebo Harmonic | version reported at launch | Harmonic |
| Agent v2.4.3 | build from `73622810` | connects; topics appear |
| `px4_msgs` `86d8239e` | compare each `.msg` in `px4_msgs` with the same-named file under PX4's `msg/`; run with no translation node | every one byte-identical; PX4's nine extra `*V0.msg` files under `msg/px4_msgs_old/msg/` are expected; messages decode |
| Jazzy | `colcon build` of this project's workspace | builds; versions recorded in the package lock |
| Offboard velocity | stream `OffboardControlMode` with velocity true and `TrajectorySetpoint` with velocity set and position NaN, for at least 1 s before switching [D22] | enters offboard and follows velocity. PX4's example is position-only, tested on Foxy and v1.14, so this is new evidence |
| QGroundControl v5.1.5 | AppImage connects to SITL | connects |
| Logging | ULog retained; run exported through `contracts/v1/writer.py` | `validate.py` passes |
| Failsafes and takeover | each row in `docs/OPERATING_ENVELOPE.md`, run twice: with no manual control at arming, because v1.17 changed Offboard to Position without RC and RC loss is ignored then; and with simulated manual control present at arming, then removed, for `NAV_RCL_ACT`, kill, stick override and the mode switch | configured and tested behaviour both recorded |
| Geofence | Home invalid at arming; a breach at each limit, with overrun measured; GPS lost mid-flight; a moved takeoff point | the code reading in the envelope is confirmed or corrected |
| Return | against the 30 m ceiling, with a parameter dump of the SITL airframe | `RTL_RETURN_ALT` as set; no breach; speed obeys `MPC_XY_VEL_MAX` |
| Vision-only position | `EKF2_GPS_CTRL` 0 with a live receiver and a global origin; offboard loss. Wrong origins: under 40 m horizontally, and too high. No origin, and `SYS_HAS_GPS` 0: expected to be refused at arming | the mode entered and the fence's behaviour are recorded. `gz_x500` may have simulated GPS, so confirm aiding is really off |
| Speed limit and braking | Position mode at full stick with `MPC_XY_VEL_MAX` set; Hold braking from each limit | Position mode obeys the limit; measured distance replaces the estimate |
| Companion death | stop the node that streams setpoints | offboard loss fires as configured |

If the Jazzy pairing fails on a step that needs a change in PX4, stop, report it, and use the Humble fallback. The freshness bounds in `evals/D1-exit-tests.json` are frozen. WO-002 covers launch and mission, and WO-004 the fault matrix; the failsafe rows above belong to WO-004.

## Consequences
- The planning total, about $3,719, is above the owner's range (`docs/BOM_WORKSHEET.md`). No purchase is authorized.
- All flight stages are outdoors, so D3 is required, D4 now follows it, and **D3 is now the first armed flight**, with ET-D2-5, ET-D3-4 and ET-D3-5 added to cover what D4 used to, and with offboard loss tested in flight only from D4, since nothing streams offboard before then. `AGENTS.md §13.9` still ties the review to "D4 readiness"; this repository treats it as due before D3, and the wording is the owner's to change. No Part 107 flight can happen until the owner holds a certificate or a certificated pilot directly supervises.
- WO-002 starts on an assembled pairing. A failure costs some setup time, and the fallback is documented.
- Five parts-list lines are flagged in the FCC check, and grant dates need reading before any order.
- This number follows ADR-0004, which belongs to the program decision on shared material, built in `ironclad`.
- `PROGRAM.md` still calls D3 optional. It is a shared file, so this repository does not change it.

## Reversibility
High until something is bought. A different flight controller or stack changes these documents and the proposed lock, and SITL does not depend on the target. After purchase, the airframe and flight controller are the costly ones to reverse.
