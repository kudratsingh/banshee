# WO-001 — D0 operating envelope, platform proposal, stack matrix, compliance plan

**Status:** partial. ET-D0-1, ET-D0-3, ET-D0-4 and ET-D0-5 are claimed on the merged documents. ET-D0-2 is partial until Option B has verified guards or the owner accepts the exception. ET-D0-6 waits for the owner.
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-001 · **Phase:** D0 · **Protocol version:** thresholds in `config/phases.json`, frozen in `work_orders/STATUS.jsonl`
**Program link:** PROGRAM §5.1, §9, §12 → banshee D0

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 0. Owner decision request
Each default is reversible until something is bought.

| # | Decision | Reversible default | Why it matters |
|---|---|---|---|
| Q1 | **Test space:** room, garage, warehouse or field? Floor size, ceiling height, solid walls or not, doors and windows, who else uses it, and whose permission. Will it be fully enclosed with doors closed? If doors must stay open, does it count as outdoors? | none; each set of limits is written. An open space counts as outdoors | decides the airframe. An X500 at 0.5 m/s needs 5.25 m square to hold and 6.05 m to move, plus about 1 m for the operator, with a 2.7 m ceiling. Many rooms and garages are too small; a typical 2.44 m garage ceiling is too low unless D1 supports a shorter `COM_OF_LOSS_T` |
| Q2 | **Airframe:** X500 V2, or the QAV250 build. Who verifies a guard for the QAV250, or do you accept it unguarded behind the net as a named exception? | X500 V2 if the space allows; otherwise QAV250 once a guard is verified | the costly one to reverse. No room-scale candidate fully qualifies, and ET-D0-2 stays partial until this is answered |
| Q3 | **Companion computer:** Jetson from D2, or later | Jetson from D2, bought after D1 | the earlier plan said D7, but D4 cannot fly VIO without onboard compute. Later also rules out the first VIO candidate in D2 |
| Q4 | **Depth camera:** OAK-D Pro or D435i on an X500; OAK-D Lite on the QAV250 | OAK-D Pro; OAK-D Lite on the QAV250 | the D435i is [on backorder with a tariff surcharge of unstated size](https://store.realsenseai.com/buy-realsense-depth-camera-d435i.html) |
| Q5 | **Outdoor work (optional D3):** wanted? | keep it possible, buy nothing for it yet | about $357 on the planning basis ($329 before tax and contingency), plus study time; dropping it closes D3 |
| Q6 | **915 MHz radio:** one seller says the SiK radio needs an amateur licence in the US. Do you hold one, or drop the radio? | drop it and use Wi-Fi, unless you hold a licence | no FCC page was read, so this is a seller's statement; the sold-out kit includes one |
| Q7 | **Budget:** Option A plans at about $4,018 and B-1 at about $2,836, against your $1,900–2,300 | no purchase; ways to cut it are in `docs/BOM_WORKSHEET.md` | the range did not hold once the net, tax and shipping were priced |

**Also for your review:**
- The freshness bounds in `evals/D1-exit-tests.json` freeze before WO-002 unless you object.
- The indoor limits are much stricter than the starter kit's, because its limits fail the arithmetic.
- The 2 cm reference target may not be reachable with webcams. It stays as written and could make D2's VIO evaluation inconclusive. The X500 needs a 27 cm tag box to reach the far corner, whose fit is unverified. The QAV250's smaller box reaches only about 2.1 m against 3.3–3.7 m.
- ET-D5-3's proposed ≥ 0.5 m clearance is below these limits. Re-propose it when D5 is frozen.

## 1. Claim and scope
Desk work only. These documents give an operating envelope for each test-space answer, priced parts lists, a proposed software stack with evidence, a compliance plan, and reference and containment plans. Nothing was installed, connected, flown or bought, and no price is a quote. Code merged, simulation passed and flight-ready are all still false for this project's flight stack, because none of it exists yet.

## 2. Frozen method
The exit-test thresholds in `config/phases.json` are unchanged. Research ran in two passes: six agents read primary sources, then six others opened every cited URL and corrected or marked what they found. A full review (`AGENTS.md §13.9`) then ran on a clean clone, with each finding checked by a second agent, and its confirmed findings were fixed before merge.

**Order of events, disclosed.** Phase D0 went to `ready` and `in_progress` at 22:44 UTC, and the `frozen` events for ET-D0-1 to ET-D0-6 were appended at 23:11 UTC. `AGENTS.md §5.3` reads `ready` as having frozen exit tests, so the order was wrong. By 23:11 the research was in and read, but none of these documents had been written. No threshold moved, and the ledger is left as it is.

## 3. Reproduction
- Stack evidence: `config/stack-lock.proposed.json`. Sources: `docs/SOURCES.md`, `docs/SOURCES-D0.md`.
- The FAA pages returned 403 to the research tool and 200 to a plain download, so they were read directly on 2026-10-31.
- `docs/BOM_WORKSHEET.md` is generated from one table, so its totals are computed from its lines.
- Commands are in the work order's Verification section; section 8 gives their results.

## 4. Results
All *estimated* or read from documentation. Nothing about the aircraft is measured.

| Option | Planning total | Goods read today | Against the $2,300 top of the range |
|---|---:|---:|---:|
| A: X500 V2 | $4,018 | $3,174.81 | +$1,718 |
| B-1: QAV250 + 6C Mini (no verified guards) | $2,836 | $2,340.94 | +$536 |

| Limit | Floor under 8.05 m | Garage or warehouse, floor ≥ 8.05 m | Field |
|---|---:|---:|---:|
| Horizontal speed | 0.5 m/s | 1.0 m/s | 2.5 m/s |
| Clearance, hold / moving | 1.5 m / 1.9 m | 2.5 m / 2.9 m | 7.5 m |
| Height | ≥ 1.2 m; ceiling − 1.5 m (X500), − 1.4 m (small frame); ≤ 2.5 m | same | ≤ 30 m AGL |
| Minimum ceiling | 2.7 m (X500), 2.6 m (small frame) | same | none |

## 5. Failure analysis
What the research and the review contradicted in the starter kit, and in this work order's first draft:
- **Stack pairing:** PX4 v1.17's guide states Humble on 22.04, not Jazzy on 24.04. The proposal keeps Jazzy for stated reasons and makes this the first thing WO-002 tests (ADR-0007).
- **Speed and clearance:** ≤ 1.0 m/s with ≥ 0.5 m clearance fails the arithmetic, which needs 2.45–2.85 m at that speed. The first draft also understated this, by leaving out the age bounds and treating an RMS bound as a peak.
- **Takeover:** three defaults would have failed. Stick override is off in offboard, no mode switch is assigned, and the default build has no CRSF input for an ELRS receiver.
- **Hold on VIO:** Hold needs global position, so without a set origin offboard loss falls through to Land. The gaps are covered by new D1 cases.
- **Speed under RC:** at defaults, full stick commands up to 10 m/s in a room whose limit is 0.5 m/s.
- **Battery reserve:** nothing in PX4's defaults enforces the 25% reserve.
- **Payload:** Holybro's documentation says about 1 kg, not the 1.5 kg recorded earlier.
- **Compute:** laptop-first does not work in flight.
- **Containment:** one panel cannot form an enclosure. The plan relies on solid walls plus nets at open sides and the operator bay, at $707.94, against $60–150 planned. A taller ceiling or no solid walls costs more, from about $276 to $1,685 (`docs/BOM_WORKSHEET.md`).
- **Reference:** tag sizes must count the printed ring, and a top plate is edge-on to the cameras. The X500 needs a 27 cm tag box to reach its far corner, and the cheap global-shutter camera cannot reach.
- **Vertical:** a stale descent needs a 1.2 m hover, and aircraft height counts toward the ceiling, so the minimum ceiling is 2.7 m on an X500.
- **Option B:** the Starling 2 is not listed in ModalAI's store, so it was removed from the priced options.

Gaps that stay open:
- No Option B candidate has verified guards. The one guard read is out of stock, with fit, mass and thrust effect unverified.
- The FAA's own declaration list did not render for an automated read, so the Remote ID module's listing comes from a third-party mirror.
- Spare props and arms are sold out at the sources read.
- Whether the geofence works on vision-only position, and what governs Hold braking, are unverified and go to D1.
- Whether a kit-built, non-recreational aircraft counts as home-built is unresolved. The plan does not rely on it, because a broadcast module is the route either way.

## 6. Cost and latency
$0 spent on hardware, compute rental or services by this work order. Latency is not measured; the arithmetic uses the proposed bounds.

## 7. Sealed access
None.

## 8. Exit tests and acceptance
| Exit test | Threshold (frozen) | Result | Evidence | Pass? |
|---|---|---|---|---|
| ET-D0-1 | zero empty fields; every unknown a named owner question | filled for each space; site unknowns go to Q1 | `docs/OPERATING_ENVELOPE.md` | claimed; passes on merge |
| ET-D0-2 | every line has a source and a date; totals per option; no purchase | Option A met. Option B-1 is priced, but lacks verified guards, so it is not yet a compatible guarded option, and its spares are covered only by contingency | `docs/BOM_WORKSHEET.md` | **partial**; needs Q2 |
| ET-D0-3 | no latest-by-default pins; every entry labelled | all proposed, with evidence URLs; two nulls, each with its question | `config/stack-lock.proposed.json`, ADR-0007 | claimed; passes on merge |
| ET-D0-4 | complete and sourced; recheck dates recorded | [S1]–[S5] read 2026-10-31; recheck column filled; site permission is a project rule, labelled as such | `docs/OPERATING_ENVELOPE.md` | claimed; passes on merge |
| ET-D0-5 | accuracy target numeric; containment per airframe | ≤ 2 cm static RMS; nets, tag box per airframe | `docs/REFERENCE_AND_SENSING.md`, envelope | claimed; passes on merge |
| ET-D0-6 | one recorded decision or deferral | waiting | section 0 | not run |

**How the thresholds were read:**
- Under ET-D0-1, measurement unknowns go to later stages, not owner questions: Hold braking, the geofence on vision, flight time with payload (D1, D4), and net strength (after D4's first hold). The owner cannot answer these; testing can.
- Under ET-D0-2, unpriced accessories sit under contingency, listed by name, and tax and shipping are labelled estimates.
- `docs/SOURCES.md` was left unchanged on the owner's limit on shared files, so WO-001's additions are in `docs/SOURCES-D0.md`.

**Verification, measured on the final tree before commit** (CI reruns the same checks on the pull request): `make check` passed; `tools/check_links.py` passed; the stack-lock assertion passed, with every entry `proposed` and an evidence URL; `grep -c unknown docs/OPERATING_ENVELOPE.md` returned 1, on the mission row, naming Q1. `evals/D1-exit-tests.json`'s bounds construct `FreshnessBounds`.

Not run: anything on a simulator or hardware. A document pass proves nothing about flight.

## 9. Limits
Supplier prices are one day's reading. Quotes passed through extraction tools in places; wording should be checked before legal use. Tax, shipping and contingency are assumptions. Published accuracy figures come from other cameras, tags and conditions. PX4 behaviour was read from documentation and source, not run. None of this shows that any of it works here.

## 10. Next bounded work order
WO-002 (SITL, software only), once the owner records a decision or deferral. It needs no purchase. WO-003 can run alongside it. A later work order of this repository's own migrates it to `ironclad` when `v1.0.0` is tagged. Rollback: revert these documents; nothing else depends on them.

## 11. Retro note
- Sized M. Most of the time went to verifying sources and to the full review, and the review changed the safety limits and the takeover plan. Keep both passes.
- A blocked research tool is not a blocked page: the FAA pages looked unreadable until a plain download worked. Try that first.
- Freeze exit tests before the `ready` event, not after.
- Price the whole option before anyone relies on a planning range.

## Errata (append-only)
