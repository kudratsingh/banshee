# WO-028 — The two Humble differences are noise

**Status:** passed. Both differences sit inside the run-to-run spread on both stacks. One Jazzy run tripped the gate early.
**Date:** 2026-11-02 · **Author:** claude-code-banshee · **Work order:** WO-028 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. All measured in simulation on `gz_x500`, 5 new runs per case per stack plus the one earlier run each, so 6 per cell.

## 1. Results (measured)
| Case and quantity | Jazzy: min, median, max (sd) | Humble: min, median, max (sd) | Verdict |
|---|---|---|---|
| R-06, Altitude-mode drift, horizontal travel | 0.35, 0.77, 1.48 m (0.43), from 5 runs | 0.23, 0.62, 1.63 m (0.48), from 6 runs | **Noise.** The ranges overlap almost entirely; the Humble median is lower |
| R-06, largest radius | 0.40, 0.86, 1.66 m, from 5 runs | 0.23, 0.73, 1.87 m | Noise, as above |
| N-01, highest point on a 5 m climb | 4.63, 4.74, 5.11 m (0.17) | 4.72, 4.75, 5.55 m (0.31) | **Noise.** The 5.55 m is Humble's one high run of six; the medians differ by 0.01 m |
| N-01, horizontal travel | 0.05, 0.05, 0.07 m | 0.05, 0.07, 0.09 m | Noise; all well inside 0.5 m |

**WO-025's two differences were single runs at the ends of wide spreads.** R-06's drift spread is about 1.3 m on both stacks, so one run of 1.63 m against one of 0.35 m said nothing. With six runs a cell, I find no difference between Jazzy and Humble in either case. Six runs cannot rule out a small one: a difference in median drift under about 0.5 m would not show.

## 2. Finding: an early gate trip on Jazzy, on PX4's own x500
One Jazzy R-06 run, `20261102T120638Z_035f4549`, latched Land on `estimator stale` at 114 ms against the 100 ms bound, at 0.75 m, before the fault. So it is excluded from R-06's numbers above. **This is the first such trip on PX4's x500 model, not the X650 proxy,** so the early trips WO-022 reported are not specific to the proxy. Their cause is still not established. They remain blocking before the first arm (ET-D3-4), and they must be explained in the D2 report.

## 3. Verification
`make check` passes. Summaries: `runs/humble-differences/jazzy.jsonl` and `humble.jsonl`; every run is in `ledgers/runs.jsonl`. Both VMs are stopped.
