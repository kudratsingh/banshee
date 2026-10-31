# WO-001 — D0 operating envelope, platform proposal, stack matrix, compliance plan

**Status:** partial. ET-D0-1 to ET-D0-5 are claimed on the merged documents; ET-D0-6 waits for the owner.
**Date:** 2026-10-31 · **Author:** claude-code-banshee · **Work order:** WO-001 · **Phase:** D0 · **Protocol version:** thresholds in `config/phases.json`, frozen in `work_orders/STATUS.jsonl` before any result
**Program link:** PROGRAM §5.1, §9, §12 → banshee D0

> Four words with fixed meanings throughout this report: **measured** (ran here, evidence attached), **estimated** (arithmetic from stated assumptions), **mocked/fixture** (fabricated for tests), **not run**.

## 0. Owner decision request
Each default is reversible until something is bought.

| # | Decision | Reversible default | Why it matters |
|---|---|---|---|
| Q1 | **Test space:** room, garage, warehouse or field? Its floor size, ceiling height, whether doors close, who else uses it, and whose permission | none; both sets of limits are written | decides the airframe. A room needs about 4.25 m square with an X500 at 0.5 m/s |
| Q2 | **Airframe:** X500 V2, QAV250 build, or Starling 2 | X500 V2 if the space allows; otherwise QAV250, once a guard is verified | the costly one to reverse. No room-scale candidate fully qualifies |
| Q3 | **Companion computer:** Jetson from D2, or later | Jetson from D2, bought after D1 | the earlier plan said D7, but D4 cannot fly VIO without onboard compute |
| Q4 | **Depth camera:** OAK-D Pro or D435i | OAK-D Pro | the D435i is on backorder with an unstated tariff surcharge; OAK-D Pro's mass is unpublished |
| Q5 | **Outdoor work (optional D3):** wanted? | keep it possible, buy nothing for it yet | about $329 plus the exam study time; dropping it closes D3 |
| Q6 | **915 MHz radio:** one seller says the SiK radio needs an amateur licence in the US. Do you hold one, or drop the radio? | drop it and use Wi-Fi, unless you hold a licence | no FCC page was read, so this is a seller's statement; the sold-out kit includes one |
| Q7 | **Budget:** Option A plans at about $3,725 against your $1,900–2,300 | no purchase; options to cut it are in `docs/BOM_WORKSHEET.md` | the range did not hold once the net, tax and shipping were priced |

**Also for your review:**
- The freshness bounds in `evals/D1-exit-tests.json` freeze before WO-002 unless you object.
- The indoor speed and clearance limits are stricter than the starter kit's, because its limits fail the arithmetic.
- The 2 cm reference target may not be reachable with webcams. It stays as written and could make D2's VIO evaluation inconclusive.

## 1. Claim and scope
Desk work only. These documents give an operating envelope for both test-space answers, priced parts lists, a proposed software stack with evidence, a compliance plan, and reference and containment plans. Nothing was installed, connected, flown or bought, and no price is a quote. Code merged, simulation passed and flight-ready are all still false for this project's flight stack, because none of it exists yet.

## 2. Frozen method
The exit-test thresholds in `config/phases.json` are unchanged. `frozen` events for ET-D0-1 to ET-D0-6 were appended before these documents were written. Research ran in two passes: six agents read primary sources, then six others opened every cited URL and corrected or marked what they found. No threshold changed.

## 3. Reproduction
- Stack evidence: `config/stack-lock.proposed.json`. Sources: `docs/SOURCES.md`, `docs/SOURCES-D0.md`.
- The FAA pages returned 403 to the research tool and 200 to a plain download, so they were read directly on 2026-10-31.
- `docs/BOM_WORKSHEET.md` is generated from one table, so its totals are computed from its lines.
- Commands are in the work order's Verification section; section 8 gives their results.

## 4. Results
All *estimated* or read from documentation. Nothing about the aircraft is measured.

| Option | Planning total | Goods read today | Against the $2,300 top of the range |
|---|---:|---:|---:|
| A: X500 V2 | $3,725 | $2,928.84 | +$1,425 |
| B-1: QAV250 + 6C Mini | $2,414 | $1,986.94 | +$114 |
| B-2: Starling 2 | $4,501 | $3,740.10 | +$2,201 |

| Limit | Room | Garage or warehouse | Field |
|---|---:|---:|---:|
| Speed | 0.5 m/s | 1.0 m/s | 2.5 m/s |
| Clearance | 1.0 m | 1.8 m | 6 m |

## 5. Failure analysis
What the research contradicted in the starter kit:
- **Stack pairing:** PX4 v1.17's guide states Humble on 22.04, not Jazzy on 24.04. The proposal keeps Jazzy for stated reasons and makes this the first thing WO-002 tests (ADR-0007).
- **Speed and clearance:** ≤ 1.0 m/s with ≥ 0.5 m clearance fails the arithmetic, which needs 1.15–1.80 m.
- **Payload:** Holybro's documentation says about 1 kg, not the 1.5 kg recorded earlier.
- **Compute:** laptop-first does not work in flight.
- **Containment cost:** a usable net is $354–462, not $60–150.
- **Reference camera:** the cheap global-shutter camera needs a tag wider than the X500's body.

Gaps that stay open:
- No Option B candidate has verified guards at a build price.
- OAK-D Pro's mass is unpublished; weigh one.
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
| ET-D0-1 | zero empty fields; every unknown a named owner question | filled for each space; each unknown names Q1 | `docs/OPERATING_ENVELOPE.md` | claimed; passes on merge |
| ET-D0-2 | every line has a source and a date; totals per option; no purchase | three priced builds, two airframe classes; unpriced items listed under contingency | `docs/BOM_WORKSHEET.md` | claimed; passes on merge |
| ET-D0-3 | no latest-by-default pins; every entry labelled | all proposed, with evidence URLs; one null with its question | `config/stack-lock.proposed.json`, ADR-0007 | claimed; passes on merge |
| ET-D0-4 | complete and sourced; recheck dates recorded | [S1]–[S5] read 2026-10-31; recheck column filled | `docs/OPERATING_ENVELOPE.md` | claimed; passes on merge |
| ET-D0-5 | accuracy target numeric; containment per airframe | ≤ 2 cm static RMS; net per airframe | `docs/REFERENCE_AND_SENSING.md`, envelope | claimed; passes on merge |
| ET-D0-6 | one recorded decision or deferral | waiting | section 0 | not run |

Three things are outside the plain words of the thresholds, and the full review was asked to judge them:
- The "every line" rule for ET-D0-2 is met for priced lines; unpriced accessories have no line and sit under contingency.
- The Starling 2 price comes from a comparison table, and its payload from a staff forum post.
- `docs/SOURCES.md` was left unchanged on the owner's limit on shared files, so the additions are in `docs/SOURCES-D0.md`.

Not run: anything on a simulator or hardware. A document pass proves nothing about flight.

## 9. Limits
Supplier prices are one day's reading. Quotes passed through extraction tools in places; wording should be checked before legal use. Tax, shipping and contingency are assumptions. Published accuracy figures come from other cameras, tags and conditions. None of this shows that any of it works here.

## 10. Next bounded work order
WO-002 (SITL, software only), once the owner records a decision or deferral. It needs no purchase. WO-003 can run alongside it. A later work order of this repository's own migrates it to `ironclad` when `v1.0.0` is tagged. Rollback: revert these documents; nothing else depends on them.

## 11. Retro note
- Sized M. Most of the time went to verifying sources, and that pass changed several figures, so keep it.
- A blocked research tool is not a blocked page: the FAA pages looked unreadable until a plain download worked. Try that first.
- Price the whole option before anyone relies on a planning range.

## Errata (append-only)
