# ADR-0007 — D0 airframe, stack and compute proposal

**Date:** 2026-10-31 · **Status:** proposed · **Work order:** WO-001 · **Program link:** PROGRAM §5.1, §12

## Context
D0 must give the owner a platform choice and a software stack to test in D1, with no purchase and no hardware. The test space is undecided. Sources are in `docs/SOURCES.md` and `docs/SOURCES-D0.md`; nothing here has been installed, run or flown.

Three findings change the starter kit's assumptions:
- PX4 v1.17's documentation states ROS 2 Humble on Ubuntu 22.04 [D2], not the Jazzy on 24.04 the kit assumed. Jazzy on 24.04 is stated only on the main-branch guide [D3].
- A camera on a flying aircraft cannot reach a laptop over USB, so "laptop over Wi-Fi for D1–D4" does not work at D4 unless images are streamed. Streaming adds latency to VIO, and no source read supports it.
- No 3–5 inch candidate read has full guards, a current PX4 target, a published payload for camera and computer, and stock together (`docs/BOM_WORKSHEET.md`).

## Decision
All of this is proposed. The owner decides the test space and airframe (ET-D0-6), and WO-002 tests the stack.

1. **Airframe.** If the space is a garage, warehouse or field: Holybro X500 V2 with Pixhawk 6C (Option A). If it is a room: no candidate qualifies yet. The default is B-1 (QAV250 with Pixhawk 6C Mini) once a guard is verified, and the room's limits are in `docs/OPERATING_ENVELOPE.md`. The airframe stays a conventional multirotor.
2. **Stack.** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, PX4 v1.17.0, Micro-XRCE-DDS-Agent v2.4.3, `px4_msgs` at `release/1.17`, QGroundControl v5.1.5. Exact commits are in `config/stack-lock.proposed.json`. Humble on 22.04 is the fallback if WO-002 cannot run this.
3. **Why Jazzy, though the v1.17 guide says Humble.** Humble's support ends in May 2027 [D11], inside the expected life of D1–D4. Gazebo recommends Jazzy with Harmonic and marks Humble with Harmonic "use with caution" [D10]. QGroundControl's AppImage has no 22.04 build [D9]. PX4's agent table lists v2.4.3 for Jazzy [D6], and PX4 main has already moved [D3]. The risk is that this pairing is assembled from separate pages, and that is exactly what WO-002's first test checks.
4. **Compute.** Jetson Orin Nano Super from D2, not D7, on Option A. D2 can be hand-carried with a laptop; D4 cannot fly VIO without onboard compute.
5. **Camera.** OAK-D Pro stays the default, as `docs/CONTEXT_AND_DECISIONS.md` has it. The D435i is on backorder with an unstated tariff surcharge, though its IMU timing is better documented [D26]. Its stereo sensors are the same global-shutter OV9282 class.
6. **VIO.** Isaac ROS Visual SLAM 4.6.0 for bench evaluation in D2, on the Jetson. BasaltVIO on the OAK is the second candidate. Neither is chosen for flight until D2 measures it.

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
| Starling 2 as the default | onboard VIO out of the box, but about $4,500 planned, price and stock unconfirmed, little payload left for guards and tags |
| Kopis CineWhoop or CineLog35 | see `docs/BOM_WORKSHEET.md` |
| Laptop through D4 | no USB in flight; see Context |

## D1 verification plan (for WO-002)
| Pin | Test | Pass |
|---|---|---|
| Ubuntu 24.04 | build in a VM or container on the owner's Mac; record the image | builds from a clean start twice |
| PX4 v1.17.0 | check out `d6f12ad1`, `make px4_sitl gz_x500` | starts and reports that commit |
| Gazebo Harmonic | version reported at launch | Harmonic |
| Agent v2.4.3 | build from `73622810` | connects; topics appear |
| `px4_msgs` `86d8239e` | diff `msg/` against PX4 v1.17.0; run with no translation node | no difference; messages decode |
| Jazzy | `colcon build` of this project's workspace | builds; versions recorded in the package lock |
| Offboard velocity | stream `OffboardControlMode` with velocity true and `TrajectorySetpoint` with velocity set and position NaN, for at least 1 s before switching [D22] | enters offboard and follows velocity. PX4's example is position-only, tested on Foxy and v1.14, so this is new evidence |
| QGroundControl v5.1.5 | AppImage connects to SITL | connects |
| Logging | ULog retained; run exported through `contracts/v1/writer.py` | `validate.py` passes |
| Failsafes | each row in `docs/OPERATING_ENVELOPE.md`, with no RC in SITL, because v1.17 changed Offboard to Position without RC | configured and tested behaviour both recorded |

If the Jazzy pairing fails on a step that needs a change in PX4, stop, report it, and use the Humble fallback. The freshness bounds are drafted in `evals/D1-exit-tests.json`.

## Consequences
- Option A's planning total, about $3,725, is above the owner's range (`docs/BOM_WORKSHEET.md`).
- The Jetson moves earlier than the owner's plan, and the owner decides that (Q3).
- WO-002 starts on an assembled pairing. A failure costs some setup time, and the fallback is documented.
- The reference's 2 cm target is unproven at webcam cost (`docs/REFERENCE_AND_SENSING.md`).
- This number follows ADR-0004, which the owner assigned to the program decision on shared material. WO-001's references were moved to 0007 on the owner's confirmation.

## Reversibility
High. Nothing is bought or installed. A different airframe or stack changes these documents and the proposed lock. After purchase, the X500 and the 3–5 inch class do not substitute for each other, so the owner's airframe decision is the costly one to reverse.
