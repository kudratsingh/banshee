# SOURCES-D0.md — sources added by WO-001

All read on 2026-10-31. These are banshee's own. `docs/SOURCES.md` is byte-identical with `vishwaroop` and is left unchanged until this repository migrates to `ironclad` (`ledgers/approvals.jsonl`), so WO-001's additions are here. They are documentation and supplier statements, not evidence that anything works in this project. Supplier links for prices are in `docs/BOM_WORKSHEET.md`.

## Recheck of [S1]–[S5], read directly on 2026-10-31
| Source | What the page says | Page's own date |
|---|---|---|
| [S1] Recreational flyers | "Almost all non-recreational drone flying is regulated by Part 107" | Oct 29, 2026 |
| [S2] Certificate cost | "approximately $175" for the initial knowledge test | none shown |
| [S3] Registration | "$5 per drone and is valid for three (3) years" for Part 107 | Mar 18, 2024 |
| [S4] Remote ID | three routes: Standard, broadcast module, FRIA | Mar 19, 2025 |
| [S5] Indoors only | "No, Part 107 would not apply to operations conducted indoors." | none shown |

## Flight stack
- [D1] PX4 v1.17.0 release, marked stable and latest, published 2026-05-13. https://github.com/PX4/PX4-Autopilot/releases/tag/v1.17.0
- [D2] PX4 v1.17 ROS 2 guide: states ROS 2 Humble on Ubuntu 22.04 with Gazebo Harmonic; no Jazzy install steps. https://docs.px4.io/v1.17/en/ros2/user_guide.html
- [D3] PX4 main ROS 2 guide, not v1.17: states Jazzy on Ubuntu 24.04. https://docs.px4.io/main/en/ros2/user_guide.html
- [D4] PX4 v1.17 Ubuntu setup: Ubuntu 24.04 and 22.04. https://docs.px4.io/v1.17/en/dev_setup/dev_env_linux_ubuntu.html
- [D5] PX4 v1.17 Gazebo: Harmonic, Ionic and Jetty on 24.04; release notes call Harmonic "the supported, CI-tested version". https://docs.px4.io/v1.17/en/sim_gazebo_gz/ and https://docs.px4.io/v1.17/en/releases/1.17.html
- [D6] PX4 v1.17 uXRCE-DDS: agent v2.4.3 for a Jazzy workspace; v3.x is not compatible. https://docs.px4.io/v1.17/en/middleware/uxrce_dds.html
- [D7] Pixhawk 6C target `px4_fmu-v6c_default`. https://docs.px4.io/v1.17/en/flight_controller/pixhawk6c.html
- [D8] `px4_msgs` branch `release/1.17`, commit `86d8239e`. https://api.github.com/repos/PX4/px4_msgs/branches/release/1.17
- [D9] QGroundControl v5.1.5 stable; AppImage for Ubuntu 24.04 and 26.04. https://docs.qgroundcontrol.com/Stable_V5.1/en/qgc-user-guide/getting_started/download_and_install.html
- [D10] Gazebo's ROS pairing table: Jazzy with Harmonic recommended; Humble with Harmonic "use with caution". https://gazebosim.org/docs/harmonic/ros_installation/
- [D11] REP-2000: Jazzy on 24.04, end of life May 2029; Humble on 22.04, end of life May 2027. https://raw.githubusercontent.com/ros-infrastructure/rep/master/rep-2000.rst
- [D22] PX4 v1.17 Offboard: stream at least 1 s before switching; over 2 Hz; `COM_OF_LOSS_T`; velocity setpoints for copters. https://docs.px4.io/v1.17/en/flight_modes/offboard.html
- [D23] PX4 parameter source at v1.17.0: `COM_OF_LOSS_T` default 1.0 s; `COM_OBL_RC_ACT` values. https://raw.githubusercontent.com/PX4/PX4-Autopilot/v1.17.0/src/modules/commander/commander_params.c
- [D24] PX4 v1.17 parameter reference: velocity, acceleration, jerk, geofence, failsafe defaults. https://docs.px4.io/v1.17/en/advanced_config/parameter_reference.html
- [D25] PX4 v1.17 Safety: geofence, kill switch, position loss. https://docs.px4.io/v1.17/en/config/safety.html
- [D43] PX4 v1.17 external vision: `vehicle_visual_odometry`, 30–50 Hz, `EKF2_EV_CTRL`, `EKF2_EV_DELAY`, `SET_GPS_GLOBAL_ORIGIN`. https://docs.px4.io/v1.17/en/ros/external_position_estimation.html
- [D44] PX4 v1.17 Hold: flying vehicles need global position. https://docs.px4.io/v1.17/en/flight_modes_mc/hold.html

## Airframes and parts
- [D12] Holybro X500 V2 kit, contents and price. https://holybro.com/products/px4-development-kit-x500-v2
- [D13] Holybro X500 V2 documentation: about 1 kg payload, about 18 min hover, 4S, platform board. https://docs.holybro.com/drone-development-kit/px4-development-kit-x500v2
- [D14] ModalAI Starling 2 datasheet. https://docs.modalai.com/starling-2-datasheet/
- [D15] NVIDIA Orin Nano dev kit carrier board specification, v1.3: 0.175 kg, DC jack 9–20 V. The document does not name the Super. https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/orin_nano/docs/jetson_orin_nano_devkit_carrier_board_specification_sp.pdf
- [D18] PX4 RC receivers: ExpressLRS with CRSF validated. https://docs.px4.io/main/en/getting_started/rc_transmitter_receiver.html
- [D19] PX4 CRSF: not in default firmware; a custom build must include `crsf_rc`. https://docs.px4.io/v1.17/en/telemetry/crsf_telemetry.html

## VIO and sensors
- [D16] Isaac ROS Visual SLAM, release 4.6: Jazzy; Jetson Orin or x86 with an NVIDIA GPU; 30 Hz minimum; stereo offset ±100 µs. https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_visual_slam/index.html
- [D46] Isaac ROS 4.6 getting started: Jetson Orin on JetPack 7.2 with a 128 GB or larger NVMe drive. https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html
- [D17] cuVSLAM licence: NVIDIA Community License, NVIDIA systems only. https://raw.githubusercontent.com/nvidia-isaac/cuVSLAM/main/LICENSE
- [D20] ROS 2 Jazzy package index and status: `depthai_ros_v3` 3.2.1-1; `realsense2_camera` 4.58.4-1 in the main apt repository. https://raw.githubusercontent.com/ros/rosdistro/master/jazzy/distribution.yaml and http://repo.ros2.org/status_page/ros_jazzy_default.html
- [D21] Luxonis OAK-D Pro: 91 g; OV9282 global-shutter stereo; BNO086; ideal depth about 0.8–12 m; up to 15 W. https://docs.luxonis.com/hardware/products/OAK-D%20Pro
- [D26] RealSense D400 datasheet, March 2026: D435i 75 g, IMU BMI055 or BMI085, 50 µs IMU timestamp accuracy. https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf
- [D27] OpenVINS: GPL-3.0; last release v2.7 in 2023; Jazzy pull requests still open. https://github.com/rpng/open_vins and https://github.com/rpng/open_vins/pull/558
- [D47] Luxonis ROS driver install: Humble and Jazzy add the testing apt source. https://docs.luxonis.com/software-v3/depthai/ros/driver
- [D30] Luxonis BasaltVIO: stereo with IMU, early access. https://docs.luxonis.com/software-v3/depthai/examples/vslam/basalt_vio_rtab.md

## Compliance
- [D28] Third-party mirror of the FAA Declaration of Compliance list, dated 2026-09-26. "The FAA list controls." The FAA's own list did not render for an automated read. https://droneauthority.org/tools/remote-id-lookup and https://uasdoc.faa.gov/listDocs
- [D29] 14 CFR 107.31, 107.39, 107.51, 107.61, 107.65; 14 CFR 89.1, 89.110, 89.115, 89.205. https://www.law.cornell.edu/cfr/text/14/107.31 and https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-14?part=89
- [D31] Part 108 (BVLOS): Final Rule at OIRA, received 07/10/2026, pending review; not in the eCFR on this date. https://www.reginfo.gov/public/do/eoReviewSearch?rin=2120-AL82
- [D32] FAA, Become a Certificated Remote Pilot: steps; recurrent training every 24 calendar months. Page dated June 9, 2026. https://www.faa.gov/uas/commercial_operators/become_a_drone_pilot
- [D33] FAA 2016 Part 107 preamble: no regulation of operations inside an enclosed structure. https://www.federalregister.gov/documents/full_text/text/2016/06/28/2016-15079.txt

## Reference and containment
- [D34] AprilTag sizing formula and position tables (Basler). https://docs.baslerweb.com/stereovisard/rc_cube/en/tagdetect
- [D35] Long-duration UAV paper: 48 cm tag at 4 m, 2-sigma height error 4.5 cm static, 0.32 m in flight. https://arxiv.org/pdf/1908.06381
- [D36] Tello AprilTag study: 184 mm tag, 3–5.5% error at 3–7 m. https://arxiv.org/pdf/2305.05673v1
- [D37] AprilTag user guide: recommends `tagStandard41h12`. https://github.com/AprilRobotics/apriltag/wiki/AprilTag-User-Guide
- [D38] Webcam sync by timestamps, about 13.3 ms average; a bachelor's thesis poster, not peer reviewed. https://lup.lub.lu.se/student-papers/record/9236101/file/9236107.pdf
- [D39] US Netting drone netting article and panels. https://www.usnetting.com/articles/2026/03/16/drone-containment-netting-solutions/ and https://www.usnetting.com/drone-netting/
- [D40] PX4 First Flight Guidelines: open space, no people within 100 m, as a rule of thumb. https://docs.px4.io/main/en/flying/first_flight_guidelines.html
- [D41] Tether review naming entanglement and impulsive forces; no procedures. https://scholarcommons.sc.edu/emec_facpub/968
- [D42] Iturralde et al., ISARC 2023: 200 mm tags, full-frame camera, several photos; 2–9 mm at 2.8–8.9 m. https://www.iaarc.org/publications/fulltext/077_ISARC%202023_Paper_175.pdf
- [D45] AprilTag generated images: `tagStandard41h12` is 9 × 9 modules. https://github.com/AprilRobotics/apriltag-imgs

## Added for the owner's decisions of 2026-10-31
- [D48] FCC Covered List page, Wayback snapshot of 2026-10-26 (www.fcc.gov returned 403). http://web.archive.org/web/20261026113846/https://www.fcc.gov/supplychain/coveredlist
- [D49] PX4 at v1.17.0: boards `px4/fmu-v6x` and `ark/fmu-v6x`, CRSF through `CONFIG_COMMON_RC`; Pixhawk 6X page; Holybro 6X store and PM02D. https://raw.githubusercontent.com/PX4/PX4-Autopilot/v1.17.0/boards/px4/fmu-v6x/default.px4board and https://docs.px4.io/main/en/flight_controller/pixhawk6x and https://holybro.com/products/pm02d-power-module
- [D50] FCC action and FAQ: DA 25-1086; fact sheet; FAQ snapshot of 2026-10-19; DA 26-761. https://docs.fcc.gov/public/attachments/DA-25-1086A1.pdf and https://docs.fcc.gov/public/attachments/DOC-417528A1.pdf and http://web.archive.org/web/20261019153404/https://www.fcc.gov/covered-list-faqs-uas-and-uas-critical-components and https://docs.fcc.gov/public/attachments/DA-26-761A1.pdf
- [D51] NVIDIA Orin Nano dev kit layout: M.2 slots. https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/hardware_layout.html
- [D52] NVIDIA forum: UART1 TX reported not driving on JetPack 7, no confirmed fix. The 6X's Ethernet is the alternative. https://forums.developer.nvidia.com/t/ttyths1-uart1-40-pin-header-pins-8-10-tx-pad-does-not-drive-on-jetpack-7-l4t-r39-2-orin-nano-super-devkit/373290
- [D53] Holybro X500 V2 assembly guide, hosted by a reseller: platform holes. https://robu.in/wp-content/uploads/2024/02/Holybro_X500_V2_Frame_Kit_Assembly_Guide_en.pdf and mount threads https://forums.developer.nvidia.com/t/how-to-mount-the-orin-nano-dev-kit/278706
- [D54] Luxonis forum: unresolved OAK-D Pro report of washed-out depth in direct sunlight; an admin's reply on outdoor depth, about a non-Pro camera. No Luxonis documentation addresses sunlight. https://discuss.luxonis.com/d/2019 and https://discuss.luxonis.com/d/5743
- [D55] 14 CFR 48.100, 48.110(a)(7), 48.115: one serial, one certificate; $5 per aircraft; updates within 14 days. https://www.ecfr.gov/api/versioner/v1/full/2026-10-28/title-14.xml?part=48
- [D56] 14 CFR Part 107 (107.12, .19, .29, .31, .33, .39, .41, .49, .51), eCFR current to 2026-10-29; FAA AC 107-2A: "does not impose a specific stand-off distance"; LAANC; manual authorization. https://www.ecfr.gov/api/versioner/v1/full/2026-10-28/title-14.xml?part=107 and https://www.faa.gov/documentlibrary/media/advisory_circular/ac_107-2a.pdf and https://www.faa.gov/uas/getting_started/laanc and https://www.faa.gov/uas/commercial_operators/part_107_airspace_authorizations
- [D57] PX4 at v1.17.0: parameter reference; multicopter defaults; geofence and navigator source, read and not run. https://raw.githubusercontent.com/PX4/PX4-Autopilot/v1.17.0/docs/en/advanced_config/parameter_reference.md and https://raw.githubusercontent.com/PX4/PX4-Autopilot/v1.17.0/ROMFS/px4fmu_common/init.d/rc.mc_defaults and https://raw.githubusercontent.com/PX4/PX4-Autopilot/v1.17.0/src/modules/navigator/geofence.cpp
- [D58] 47 CFR 15.1, 15.204, 15.247; Holybro store page with the FCC ID; FCC grantee record; one seller's statement. The grant itself was not readable. https://www.ecfr.gov/api/versioner/v1/full/2026-10-29/title-47.xml?part=15&section=15.247 and https://holybro.com/products/sik-telemetry-radio-v3 and https://opendata.fcc.gov/resource/3b3k-34jp.json?$limit=3&$where=upper(grantee_code)%3D%272AP22%27 and https://www.readymaderc.com/products/details/86245-holybro-sik-telemetry-radio-v3-100mw-915mhz-2-pcs
- [D59] 3DR, the redirect target of store.mrobotics.io: kit page and FCC ID statement. https://store.3dr.com/3dr-sik-telemetry-radio-915mhz-kit/ and https://docs.3dr.com/irc/fcc-id-dev/
- [D60] Blue UAS Framework data, Wayback copy of 2026-05-25, the newest readable: ARKV6X and ARK SAM GPS listed, added 2025-02-15 and 2026-03-03. The live list returned no rows to an automated read. https://web.archive.org/web/20260525131432id_/https://bluelist.appsplatformportals.us/getFrameworkPublic/?search=&sort=CriticalComponent.mad_componentname&order=asc
- [D61] Owner's reading of FCC records, 2026-11-01: FCC ID 2AP22-HT03-V3, 15.249, test report SZAWW180522002-01; FCC ID 2ADLE-900X, 15.247. Automated reads return 403. https://fccid.io/2AP22-HT03-V3
- [D62] Read 2026-11-01. Luxonis OAK-D Pro W specifications: stereo OV9282, global shutter, DFOV 150°. https://docs.luxonis.com/hardware/products/OAK-D%20Pro%20W
- [D63] Read 2026-11-01. Holybro baseboard flashing guide: JetPack 5.1.2 to 6.0 and 6.2.2 only; PX4's page: tested with JetPack 6.0, Ubuntu 22.04, Humble; Holybro's bundle package list. https://docs.holybro.com/autopilot/pixhawk-baseboards/pixhawk-jetson-baseboard/flashing-guide.md and https://docs.px4.io/main/en/companion_computer/holybro_pixhawk_jetson_baseboard
- [D64] Read 2026-11-01. Holybro X650 kits: 650 mm wheelbase, 2,000 g kit, payload 3.1 kg with 10,000 mAh, takeoff limit 6,300 g at 70% throttle, 30 min hover on 6S 10,000 mAh with no added payload. https://holybro.com/products/x650-kits
