# WO-015 — The owner's decisions after D1

**Status:** passed
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-015 · **Phase:** D3 (standoffs), D1 (records)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**.

## 1. Claim and scope
Three owner decisions of 2026-11-01 are recorded where the repository acts on them. No purchase, no hardware, and no code changed.

## 2. What changed
| Decision | Where | Label |
|---|---|---|
| ADR-0010 accepted | `docs/adr/ADR-0010-vision-cases-carried-to-d4.md` | owner decision. V-04 stays with V-01 to V-03, as the ADR states; the owner's words name only those three |
| D3 standoffs frozen: 8.6 m at 2.5 m/s, 3.35 m at 1.0 m/s | `evals/D3-standoffs.json`, sha256 `2fd7132ca38f9add751291fe7dfb58dcbba2ced7e3a996d4aa68e941e0337953`; `docs/OPERATING_ENVELOPE.md` | braking measured in SITL; reaction and position error estimated. Not flight measurements |
| Overrun margin 7.5 m to 9 m; exclusion arithmetic 149 m, rounded to 150 m; a smaller field keeps R + 109 m | `docs/OPERATING_ENVELOPE.md` | estimated |
| The 150 m exclusion radius covers position-lost cases on its own | `docs/OPERATING_ENVELOPE.md` | owner's rule; arithmetic estimated |
| VM disk cap and free-space check done | `ledgers/corrections.jsonl` | measured: read back on 2026-11-01 |

## 3. Finding on the exclusion rule
The rule holds for position loss alone: from the flight box edge, 30 m out, with 13.1 m of carried speed and the table's worst drift of 101.8 m, the aircraft reaches 144.9 m. From fence plus overrun, 49 m out, it reaches 158.5–163.9 m. That needs position loss on top of a fence breach, so it is a second failure, but the rule as worded does not cover it. The envelope states both. These are estimates, and the drift term has only been measured in simulation.

The old table's limit was built on 47.5 m out and a 102.5 m drift budget. Those no longer apply, so the height and wind table now rests on the flight-box case. Its numbers did not change.

## 4. Verification
`make check` passes. Nothing was run in the simulator.

## 5. Retro
`ledgers/approvals.jsonl` holds the owner's words, so the scope of each later work order can be checked against them.

## 6. Limits
Standoffs are from simulation, with no wind. `MPC_XY_VEL_MAX` overshoot in Return, measured at up to 18% in WO-004, is not a term in the table. Next: WO-016.
