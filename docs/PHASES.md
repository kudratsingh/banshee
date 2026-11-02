# PHASES.md — Omni Drone: the mission ladder, exit tests, and how to track it

Machine-readable twin: `config/phases.json` (a test keeps the two in sync). Live state: `docs/STATUS_BOARD.md` (generated from `work_orders/STATUS.jsonl`). Rules: `AGENTS.md §5`. Program context: `PROGRAM.md §5.1, §6`.

**How to read this file.** Each stage lists its deliverable, prerequisites, work orders, and exit tests (`ET-<stage>-<n>`). A stage is `passed` only when every exit test has run with evidence in a report. Thresholds marked *proposed default* are frozen in `evals/<stage>-exit-tests.json` before the stage becomes `ready`. **Safety and failure-mode checks are exit tests of the stage they belong to**, not a separate workstream. Three different states are always reported separately: *code merged*, *simulation passed*, *flight-ready*.

## The ladder

```
D0 envelope ──► D1 SITL ──► D2 props-off ──► D3 outdoor GPS ──► D4 VIO hold ──► D5 GPS-denied route ──► D6 inspection ──► D7+ missions & learned gates
```
All flight stages are outdoors (owner decision, 2026-10-31), so D3 is required, and no stage skips manual commissioning. "Omni" means broad mission capability added one mission at a time; a mechanically omnidirectional airframe would be an explicit owner decision.

Stage states: `not_started → ready → in_progress → (blocked ↔) → passed | failed`.

---

## D0 — Operating envelope, platform proposal, compliance plan (no purchase)

**Deliverable.** One-page operating envelope; priced BOM with dated sources for the chosen airframe (the owner dropped the second option on 2026-10-31; ET-D0-2's wording stands, and it closes on that decision); proposed stack version matrix with a D1 verification plan; compliance plan; reference and containment plan; owner decision on test space and airframe candidate. **Work orders.** WO-001.

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D0-1 | Operating envelope complete (mission/site, airframe class, speed/height/clearance with justification, sensors, compute, energy, reference, containment, human control, compliance, data/privacy) | zero empty fields; unknowns are named owner questions |
| ET-D0-2 | Priced BOM, ≥ 2 airframe options, landed cost incl. shipping/tax/spares/batteries/compliance/reference/compute | every line sourced and dated; totals per option; no purchase |
| ET-D0-3 | Stack version matrix (PX4, ROS 2, Gazebo, bridge, QGC, drivers), each pin proposed/tested, D1 verification plan | no latest-by-default; every entry labelled |
| ET-D0-4 | Compliance plan: Part 107 path, registration, Remote ID, indoor-only applicability, site permission, VLOS, with sources | complete and sourced |
| ET-D0-5 | Outside-in reference qualification plan with numeric accuracy target; containment chosen per airframe/test configuration | stated numerically |
| ET-D0-6 | Owner decision (or explicit deferral) on test space and airframe | one recorded decision or deferral |

**Decision on the airframe (owner, 2026-10-31; airframe superseded 2026-11-01).** The test space is an open field, outdoors. The airframe was an X500 V2, with an X650-class 6S airframe planned for D7+; the owner's decision of 2026-11-01 replaced it with the Holybro X650 ARF from the start (ADR-0007). Option B is not needed.

## D1 — SITL, offboard velocity interface, logging, fault matrix

**Deliverable.** Reproducible PX4 + Gazebo software-in-the-loop with pinned versions; waypoint mission through the bounded velocity/yaw-rate offboard interface; exports validating against contract v1; the simulated fault matrix executed; a tested setpoint-freshness gate in the command path. **Work orders.** WO-002 (SITL + mission + export), WO-004 (fault matrix + freshness gate in the loop).

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D1-1 | SITL launches reproducibly with a version manifest | 2/2 clean launches identical versions; zero null pins |
| ET-D1-2 | Waypoint mission completes via offboard velocity/yaw-rate; outcome checked by independent code from logged state | *proposed default:* 10/10 runs reach every waypoint within 0.5 m |
| ET-D1-3 | Each run exported via `contracts/v1/writer.py` with correct frames/timebase, validates | 100% `contract_valid`; frame-convention ADR |
| ET-D1-4 | Fault matrix executed: stale setpoint with live heartbeat, lost command stream, stale sensor, missing depth, localization reset/loss, delayed planner, low energy, operator takeover — behaviour as specified, configured vs tested distinguished | all cases executed; deviations reported |
| ET-D1-5 | Setpoint-freshness + estimator-validity gate with frozen bounds in the command path, unit-tested; heartbeat ≠ freshness | tests green; bounds justified |

**Notes.** PX4's ROS 2 offboard heartbeat and the setpoint stream are separate: a continuing heartbeat does not prove fresh setpoints [S6]. Offboard needs a valid position/velocity estimate [S6]. The response to a fault depends on which estimates remain valid; there is no universal hover-on-error rule.

## D2 — Props-off sensor and localization walkthrough

**Deliverable.** Propellers removed: the intended camera/IMU setup carried through the test volume; timestamps, frames, latency, estimator resets and tracking loss measured; outside-in reference qualified; real connection-loss behaviour exercised on the actual command path. **Requires hardware** (after D0's purchase decision; purchase itself is an owner action). **Work orders.** WO-005 (stub).

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D2-1 | Camera/IMU offsets, frame consistency, end-to-end latency measured hand-carried, on the OAK-D Pro W and the Orin NX on the Holybro Pixhawk Jetson Baseboard; the report states the distortion model of the unit's factory calibration and whether the VIO candidate accepts it | offset CI; frame check passes; latency distribution |
| ET-D2-2 | VIO tracks the volume on the OAK-D Pro W; dropouts/resets counted; drift vs reference; ARK Flow MR flow and range logged on the same routes | *proposed default:* end-of-route drift ≤ 0.2 m; flow and range reported |
| ET-D2-3 | Outside-in reference qualified: static residuals, dynamic latency, coverage, session check | *proposed default:* static RMS ≤ 2 cm; coverage ≥ 90%; inadequate coverage = inconclusive |
| ET-D2-4 | Motors disarmed, actual Jetson-to-6X link cut on the Jetson, because it runs in board traces: Ethernet interface down, or XRCE-DDS agent stopped for the UART. The report names the path carrying offboard and shows the other carries no setpoints. PX4's offboard-loss flag sets no later than `COM_OF_LOSS_T` + 200 ms after the cut, logged, and the freshness gate stops sending, laptop-independent. PX4 selects no action while disarmed; the action is tested in ET-D4-4 | 3/3 trials match |
| ET-D2-5 | Props off, disarmed: RC link over CRSF, kill switch, mode switch and ARK Flow MR over DroneCAN recognised on the actual Pixhawk 6X on the Holybro Pixhawk Jetson Baseboard; needs a dated owner approval to connect | each control and the ARK Flow MR recognised; 3/3 power cycles |

A hand-carried pass is **not** flight qualification; vibration changes VIO behaviour (revalidated in D4).

## D3 — Outdoor GPS-assisted checkout

**Deliverable.** First armed flights: manual and GPS position-hold checkout at a permitted site under the applicable compliance path (Part 107 by default; development flights are not assumed recreational [S1]). **Requires §2.3 owner approval for arming/flight.**

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D3-1 | Compliance in place: certificate if applicable, registration, Remote ID route, airspace, site permission | all applicable items recorded with dates |
| ET-D3-2 | Manual checkout in Position mode and GPS position hold | *proposed default:* RMS ≤ 1.0 m over 60 s, 3/3 flights |
| ET-D3-3 | Emergency procedures (RTL, land, kill) rehearsed | each exercised once |
| ET-D3-4 | Before the first arm: distance and geofence containment, exclusion, checklists, roles and emergency procedures signed off; parameter dump from the real aircraft matches the frozen values | complete before first arm |
| ET-D3-5 | At low height on GPS: takeover, geofence breach and RC loss behave as specified on the real aircraft | each 3/3; any deviation reported |

## D4 — VIO position hold in a controlled setup

**Deliverable.** First VIO flights inside the field's containment of distance and geofence: VIO position hold, operator takeover and offboard-loss behaviour tested in flight, VIO revalidated under vibration. **Requires §2.3 owner approval for arming/flight.**

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D4-1 | Containment, checklists, roles, emergency procedures in place and signed off | complete before first arm |
| ET-D4-2 | VIO hold error vs outside-in reference | *proposed default:* RMS ≤ 0.3 m over 60 s, 5/5 flights |
| ET-D4-3 | Operator takeover in flight | 3/3 |
| ET-D4-4 | Offboard loss in flight, first with GPS aiding on → specified behaviour (hold or land by estimator validity) | 3/3 |
| ET-D4-5 | VIO health under flight vibration revalidated | loss/recovery counts and drift reported in flight |

## D5 — GPS-denied known route

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D5-1 | Route completion and path error vs reference | *proposed default:* ≥ 8/10; RMS ≤ 0.5 m |
| ET-D5-2 | Degraded modes in flight (stale planner → hold; localization loss → land) | each executed; matches spec |
| ET-D5-3 | Minimum clearance, excluding the staked reference equipment | *proposed default:* ≥ 0.5 m |
| ET-D5-4 | Latency quantiles, deadline misses, command expiries | reported; frozen p95 and expiry bounds |
| ET-D5-5 | Energy reserve at landing | *proposed default:* ≥ 25% |

A known-route demonstration does not establish unknown-space navigation; unknown space is not free space.

## D6 — Fixed-target inspection from N declared viewpoints and return

**Deliverable.** The first complete mission under a full rubric (Stage 3 of the program: planner + skills + success detector + recovery).

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D6-1 | Rubric declared before flight (N viewpoints, coverage/visibility, dwell/image quality, target identity, start/return region, route, timeout, reserve); completion requires every component | *proposed default:* ≥ 7/10 complete |
| ET-D6-2 | Independent review of reference/log/video evidence; a waypoint list alone is not success | reviewer agrees on 100% of claimed completions |
| ET-D6-3 | Failure cases (occluded target, localization loss mid-mission, low energy) handled per spec | each executed |
| ET-D6-4 | Cost per mission attempt and per flight hour | reported |

## D7+ — Further missions one at a time; learned-component integration gates

Each new mission (object search, mapping an unknown room, adding capability on the onboard computer) gets its own rubric, frozen thresholds and degradation tests before flight. Learned components — first candidate: the world model's uncertainty-gated residual dynamics (`PROGRAM.md §8.2`) — enter only through: held-out log evaluation → shadow mode (logged, never commanding) → controlled closed-loop comparison against the conventional baseline, with a kill switch and drone-owned acceptance. Prediction improvements are not mission gains until the closed-loop comparison shows them.

| Exit test | Statement | Threshold |
|---|---|---|
| ET-D7-1 | Each mission defined with rubric, frozen thresholds and degradation tests before flight | frozen per mission when next |
| ET-D7-2 | Learned component integrated only via held-out → shadow → controlled closed-loop, kill switch, drone-owned acceptance | frozen when a component is proposed |

## Every exit report
Uses `docs/REPORT_TEMPLATE.md` and includes nominal runs, invalid-data behaviour, connection loss, takeover, estimator health, latency, energy, costs, configuration, and unresolved limitations. Thresholds are frozen before testing; a bad run is never removed from the record (intervention, timeout and abort counts stay).
