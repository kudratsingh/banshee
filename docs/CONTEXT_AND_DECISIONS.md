# CONTEXT_AND_DECISIONS.md — Omni Drone

What an agent needs from the planning conversations (Oct 2026) to make the same choices the owner would. Program-level decisions: `PROGRAM.md §11–12`. Status words: *confirmed*, *proposed default*, *unknown*, *future option*.

## 1. Why this project exists
- The owner's goal is a **broadly capable autonomous drone built step by step**, not a single narrow demo; "omni" means broad mission capability. *Confirmed (Oct 30, 2026).*
- It is kept **separate** from the world model because the sim-to-real gap for a drone is large and the drone must make progress conventionally regardless of ML results. *Confirmed.*
- With the Microduck dropped, the drone is the natural home of the "brain" work: mission executive, success detection, recovery (program Stage 3). *Confirmed.*
- The owner's interest areas include autonomous and aerial systems and defense; Part 107 is treated as a credential worth having. *Confirmed.*

## 2. Decisions adopted from the two external reviews (Oct 30, 2026)
| # | Decision | Status |
|---|---|---|
| 1 | Conventional first; learned components only through evidence gates (held-out logs → shadow → controlled closed-loop) | confirmed |
| 2 | Ladder D0–D7+ with exit tests; D3 optional; props-off sensor/localization stage (D2) before any armed flight; indoor position hold needs a valid position estimate (VIO) and is a different milestone from outdoor GPS hold | confirmed |
| 3 | Operating envelope written before buying hardware; the test space decides the airframe class | confirmed |
| 4 | Pin and test the actual command path (PX4 version, bridge, offboard velocity interface); the archived PX4-Avoidance repo is not assumed; collision prevention in Position mode is not assumed to protect offboard commands | confirmed |
| 5 | Setpoint freshness checked independently of the heartbeat; no universal hover-on-error; loss handling independent of the laptop | confirmed |
| 6 | Outside-in reference (fixed cameras + tags on the aircraft, independent clocks) as evaluator, never as an operational input in unaided-VIO tests; qualified for accuracy, coverage, latency; session checks | confirmed |
| 7 | FAA: non-recreational development flights fall under Part 107; the 250 g threshold is not a blanket exemption; indoors-only is outside Part 107 but still needs permission and controls | confirmed (corrected from an earlier draft) |
| 8 | Safety checks live inside stage exit tests, not separate workstreams | confirmed |
| 9 | Code merged, SITL passed, flight-ready are separate states | confirmed |
| 10 | Exports to the world model through the contract only; the drone owns command authority and can reject proposals | confirmed |

## 3. Hardware context (from the owner's purchase plan, Oct 30, 2026)
- Candidate kit: Holybro X500 V2 PX4 Development Kit (Pixhawk 6C, M10 GPS, 915 MHz telemetry; $609 at Holybro, sold out there on Oct 30, 2026; dealers $540–950). 500 mm wheelbase, 1.5 kg payload, ~18 min hover on 5000 mAh [H5].
- Companion computer: Jetson Orin Nano Super 8 GB ($249 → $399 in July 2026) [H6]; depth camera OAK-D Pro or RealSense D435i; 3 × 4S 5000 mAh; RadioMaster TX16S; containment; Part 107 exam (~$175 [S2]).
- Total planning range $1.9–2.3k. **Nothing is purchased. The purchase decision follows D0 and D1, by the owner.**
- If D0 determines the test space is a room, a 3–5 inch guarded frame replaces the X500 and the BOM is re-priced.

## 4. Working style (owner)
Fast, autonomous iteration through bounded work orders; continue to the next ready WO without asking; exit tests frozen before work; append-only records; proactive cost diagnosis. Hardware motion, arming and flight always need a dated owner approval (`AGENTS.md §2.3`).

## 5. Open decisions (project level)
| # | Decision | Default until decided |
|---|---|---|
| 1 | Test space: room vs garage/warehouse vs field | unknown — D0 must resolve (ET-D0-6) |
| 2 | Airframe: X500 V2 class vs 3–5 inch frame | X500 V2 if the space allows; otherwise 3–5 inch |
| 3 | Companion computer and depth camera | Orin Nano Super 8 GB; OAK-D Pro |
| 4 | Stack pins (PX4, ROS 2, Gazebo, bridge, QGC) | proposed in WO-001, tested in WO-002 |
| 5 | Frame convention ADR | ROS ENU/FLU internally, convert at the PX4 boundary |
| 6 | Remote repository | none; local git only |

## 6. Contradictions found while consolidating
| Conflict | Resolution |
|---|---|
| Reference kit forbade branches/PRs and required a stop after every WO vs owner's autonomous-development instruction | Owner's instruction governs (`AGENTS.md §2–4`); remote ops wait for designation; hardware/flight gates unchanged |
| Reference drone `CLAUDE.md` contained world-model-only rules | Policy split into shared core + drone addendum |
| Reference used `WO-002` twice (budget and D1) | Renumbered: WO-002 D1 SITL, WO-003 budget enforcement |
| Earlier draft: "below 250 g needs nothing", "TRUST for outdoor" | Corrected per FAA sources [S1]–[S5] |
| Earlier draft: "tether for D4" as a universal rule | Containment decided per airframe/test configuration in D0 |
