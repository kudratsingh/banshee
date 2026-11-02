# WO-026 — The owner's second set of decisions of 2026-11-02

**Status:** passed, pending review
**Date:** 2026-11-02 · **Author:** claude-code-banshee · **Work order:** WO-026 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Nothing ran; this records decisions and drafts tests. Prices in the D3 package are search results, except the RFD900x-US, read on 2026-11-01.

## 1. Recorded
| Decision | Where |
|---|---|
| ET-D2-4: no setpoint older than 200 ms after SIGCONT or restart, 3/3, pass/fail | `config/phases.json`, `docs/PHASES.md`, `evals/D2-exit-tests.json` |
| Lines 1, 2, 4, 11, 12, 13, 14, 15, 16, 17, 18, 23, 28, 29 approved; line 31 held | one ledger record per line; `docs/BUY_LIST-FINAL-2026-11-02.md` |
| Line 2 FCC cleared, by the owner's reading of Holybro's SDoC | the list, and source [D66] |
| Package split, CI on 3.10 | done in WO-027 |
| Humble repeats before D2 | WO-028, running |
| SiK 1 W check at D3; RTK options; M10 as backup | `docs/D3_APPROVAL_PACKAGE.md` |
| D3 measurements to raise the limits | ET-D3-6 and ET-D3-7 |
| Connecting the flight controller and starting D2 need dated approvals | ledger; not approved |

## 2. My choices inside the decisions
- **ET-D3-6's grid** (3, 6 and 10 m; three wind bands up to 4 m/s; 3 trials per cell; a 5 s takeover delay; a flow-off comparison at 3 m) and **ET-D3-7's criteria** (10 m to spare at p99 reach with p95 shear; held-out error ≤ 15% and never under by more than 5 m; ≥ 25% thrust in reserve) are mine. The owner can change them before D3 is frozen.
- **D3 cannot measure 6–8 m/s,** because it flies at 4 m/s or less. Going to 8 m/s doubles the highest measured wind, so most of that claim rests on the model. That is why ET-D3-7 makes the first flights at a raised limit a separate approved test.
- **The SiK 1 W's FCC ID** reads 2BNF8-HT051WRF915 on Holybro's page, but the same line says 100 mW. Its rule part is left unconfirmed, as the owner asked, until D3.

## 3. Verification
`make check` passes.

## 4. Independent review
Read-only, from the diff and the owner's words. It found: ET-D3-6's GPS-off trials put the aircraft in Altitude mode, where the D3 speed limit does not hold and the fence does not act, yet read as settled; the outside-in reference cannot be the truth at this scale; ET-D3-7 covered only the flow-aided case, left reach undefined, could not fail, and had criteria that could not be computed; missing gust, non-flying-day, airspeed and mast items; an overstatement of what held-out checks show; missing correction-link, deferred-line and anemometer items in the package; the SiK entry not plain enough; ET-D2-4's age undefined; stale envelope text; and smaller items. All are fixed. **The GPS-off trials (b) and (d) now need their own dated owner approval and an ADR**, and both D3 thresholds are labelled as the agent's proposal. The ledger is append-only, so a new record adds that limit. There was no second pass on these fixes.
