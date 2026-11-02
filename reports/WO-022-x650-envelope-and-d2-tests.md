# WO-022 — Envelope recomputed for the X650; D2 exit tests updated

**Status:** passed, with the position-lost margin at 0.9 m, a gate behaviour left unexplained, and all of it resting on a simulated proxy
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-022 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. "Measured" here means measured in simulation on the proxy, on PX4 commit d6f12ad1. Nothing ran on hardware. No result exists for a real X650.

## 1. Claim and scope
`evals/D3-standoffs-x650.json` freezes the values below, by the owner's decision of 2026-11-01, before D2 starts. `evals/D3-standoffs.json` stays as the X500's record. `docs/OPERATING_ENVELOPE.md`, ADR-0007, `config/phases.json`, `docs/PHASES.md` and `evals/D2-exit-tests.json` follow them. `evals/D2-exit-tests.json` is now sha256 `d72ce5a86096c6f87ed4c1742951673fbb3bb0da7eea0f4297fca7e1c852ac33`; it was `0ac32802c5691662abca0fe7f81c0df46e1151176ba88624e3fbff0a448b8131`.

| Value | X500 (frozen, kept as record) | X650 (frozen here) | Label |
|---|---:|---:|---|
| Standoff at 2.5 m/s | 8.6 m | **8.7 m** | reaction and error estimated; braking measured on the proxy |
| Standoff at 1.0 m/s | 3.35 m | **3.4 m** | same |
| Overrun margin | 9 m | **9 m** | 8.7 m rounded up |
| Exclusion radius | 150 m | **150 m** | 40 + 9 + 100 = 149 m, rounded up |
| Position loss alone, reach | 139.5–144.9 m | **143.7–149.1 m** | carried speed measured; drift estimated |
| Least margin under the owner's rule | 5 m | **0.9 m**; 6.3 m in D3 | |
| Crew from Home | 50 m | **85 m** | estimated |

**The owner's 150 m rule holds, by 0.9 m.** The stop condition did not fire. See §4 for what that margin depends on.

## 2. The proxy
PX4's x500 model, with mass 5 kg (and 4 kg), arm 0.23 m and 3.0 kg of thrust per motor. Published: 650 mm wheelbase, 2,000 g kit. Estimated: thrust per motor, inertia scaled as m·L², drag scaled to match the x500's deceleration per unit speed, motor time constants 0.10 and 0.15 s. A half-drag variant brackets the drag. It is a stand-in for how the terms move with mass, not a model of the X650.

**Not run:** a lower thrust margin. The proxy has about 2.4:1 at 5 kg. Holybro's 6,300 g limit at 70% throttle suggests nearer 1.8:1. Nor were the real motor response, prop aerodynamics, vibration or the frame's own drag modelled.

## 3. Measurements (simulation on the proxy; three usable runs per case)
| Term | Case | 5 kg | 4 kg | Half drag | X500 (WO-004) |
|---|---|---:|---:|---:|---:|
| Braking from 2.5 m/s, net of 0.2 s | H-02, K-01 | 3.01–3.15 m | 3.03–3.26 m | 3.01–3.05 m | 3.0–3.2 m |
| Braking from 1.0 m/s, net of 0.2 s | H-01, K-02 | 0.90–1.04 m | not run | not run | 0.93–1.02 m |
| Lost stream, travel at 2.5 m/s | C-02 | 5.81–5.90 m | not run | not run | 5.70–5.92 m |
| Lost stream, travel at 1.0 m/s | C-01 | 2.04–2.07 m | not run | not run | 2.03–2.26 m |
| Fence overrun, horizontal | G-01 | 3.28–3.48 m | 3.44–3.67 m | not run | 3.82–3.94 m |
| Fence overrun above 14 m | G-02 | 0.48–0.79 m | not run | not run | 0.53–0.68 m |
| Climb after takeoff-phase loss | C-05 | 1.50–1.57 m | not run | not run | 1.45–1.50 m |
| Carried after position loss | G-04 | 12.4–12.8 m | 12.3–12.5 m | 15.2–17.2 m | 12.5–13.1 m |
| Wind drift, 5.4 m/s, 10 m, with skid | W-01 | 41.3–60.9 m | not run | 25.0–26.5 m | 41.5–46.1 m |
| Skid after touchdown | W-01 | 4.5–17.7 m | not run | 2.0–2.2 m | 4.3 m, one recording |

**Mass barely moved these terms. Drag moved the carried and wind terms, in opposite directions.** That follows from PX4's limits being accelerations, given enough thrust. It is why the thrust margin matters and was not run.

One W-01 run tumbled on touchdown: 17.85 m/s peak and a 3.9 m rebound, at 0.7 m/s descending and about 5 m/s across the ground. The simulated ground contact is not validated, so read this as "a drifting landing may flip", and not as a distance.

## 4. The 150 m rule
Reach = 30 m flight box + 17.3 m carried + 96.4–101.8 m drift = 143.7–149.1 m. The drift formula is unchanged and *estimated*: wind × (height ÷ 0.7 + 5 s). Three things sit behind the 0.9 m:
- **17.3 m is the half-drag figure, and half drag also halves the wind drift** (W-01). Adding it to a drift that assumes the aircraft is at full wind speed from the start is conservative. At 5 kg the carried term is 12.8 m, and the margin is 5.4 m.
- **The skid was not in the X500's arithmetic, and it is not added here.** Airborne drift plus skid reached 60.9 m at most, against 75–77 m for the formula with no operator delay. That was checked at one wind and height only.
- **The 25 m at 2.5 m/s row sets the 101.8 m.** All of D3 stays at 10 m, which gives 96.4 m and a 6.3 m margin.

If a later measurement takes the margin below zero, the cheapest options are, in order: lower the height limits in the wind table, which keeps the field the same; shrink the flight box, at 1 m per metre; or raise the radius, which needs a larger field. Position loss at the fence's edge remains a second failure, and it now reaches up to 168.1 m.

## 5. The props and the crew (*estimated*, no test)
Ballistic with quadratic drag, 25 m release, best angle: 2–5 g tumbling fragments land within 48–55 m; a 15 g half blade within 27–31 m. So from fence plus overrun a fragment reaches about 104 m, and the radius does not move. From the flight box's edge it reaches 85 m, so **the crew moved from 50 m to 85 m from Home. This is my change, not one the owner named,** and it is the one value here that a D3 site plan will feel. A 5 g chip flying stably edge-on reaches 311–432 m in the same model; that is not credible for a tumbling piece, and nothing here excludes it. 100 m remains PX4's rule of thumb, which names no mass.

## 6. D2 exit tests
Thresholds carry over. Changes, before any result exists:
- **ET-D2-1** names the OAK-D Pro W and the Orin NX on the baseboard, and must report the unit's factory distortion model and whether the VIO candidate accepts it.
- **ET-D2-2** adds the ARK Flow MR's flow and range, reported, with no threshold.
- **ET-D2-4 changes method.** The link runs in board traces, so nothing can be unplugged. The cut is the interface taken down on the Jetson, named in the report. **This is a weaker cut than a physical one:** it does not test the wiring, which on this board is not a likely failure.
- **ET-D2-5** names the 6X on the baseboard, and adds the ARK Flow MR over DroneCAN to what must be recognised. The ARKV6X note is gone.
- **Required in the D2 report:** sunlight now reads OAK-D Pro W; power now reads the UBEC at 7.2 V on 6S; the gate finding below is added.

**Not changed:** the Jetson stack, which waits on the owner. Connecting the flight controller and the link cut each still need a dated owner approval.

## 7. Finding: the gate tripped early in 10 of the first 63 runs
In 10 runs the gate reported `estimator stale` before the fault, first at ages of 104–345 ms against the 100 ms bound: six before takeoff and four in flight. Nine latched Land. The tenth, G-04 `ca564dcf`, has the gate's response off by design; it armed, never lifted and disarmed after 11 s, and I did not separately explain it. D1 reported a `continue` verdict at every armed tick in 40 X500 missions. These runs measure nothing. A single stall of about 334 ms also appears in 24 of 62 exported proxy runs and in 63 of 191 earlier X500 exports, most of them with no effect on the run.

**Cause not established.** What is known:
- Age stayed high across the run in those read, while the gap between samples stayed near normal in most. That points at the mapping from PX4's clock to the host's, in which `src/banshee/offboard/mission.py` keeps the smallest offset seen, and not at late data. A pause that shifts the offset would raise every later age. This is a hypothesis, and was not tested.
- By recording: 7, 2, 1, then 0 in the last 19 proxy runs and 0 in the 12 control runs.
- **The control does not settle it.** N-01 alternated between x500 and the proxy, 6 each, with no trips on either. If the rate were still about 16%, 6 clean runs would happen by chance about a third of the time. Another project's process was using one core at the time I looked; I did not stop it, and I do not know whether it ran during the first recording.

**Effect on the numbers.** Excluded by a rule fixed before the further recordings: a run is usable if the trigger fired and no mode other than offboard came before it, and the first three usable runs in time order are used. Two usable runs, K-01-4KG and H-02-4KG in recording 2, tripped to Land after the fault, while or after braking. They count under that rule, and K-01-4KG's gives the 3.26 m that sets the braking term, so they raise it and do not lower it. The gate code and its bound did not change. Whether this reaches hardware is open, and it is now required in the D2 report.

## 8. Other disclosures
- The first proxy smoke run failed on an invalid inertia, from my replacing text in the model; that is fixed, tested, and the failed run stays in `runs/`.
- Expected values in `evals/X650-proxy-cases.json` are the X500's. G-01 and G-02 show the same 5 s hold deviation as in D1, which is a known error in those expected values.
- The 4 kg and half-drag variants cover only the cases in the table.
- Hover time is scaled, not published: Holybro's 30 min on 6S 10 Ah is with no added payload. The ≤ 8 min plan stays.

## 9. Verification
`make check` passes. Recordings: 94 proxy and control runs in this work order; none failed to execute. Independent review: see §11.

## 10. Runs used
```
N-01 | 20261102T031317_6fef89d0, 20261102T033409_8867388e, 20261102T043411_d95ac714
H-01 | 20261102T035705_c970b9ef, 20261102T043505_0afa2c5b, 20261102T044419_86580a3c
H-02 | 20261102T031500_d7929f04, 20261102T033539_9fd288a9, 20261102T035757_cc9820dd
K-01 | 20261102T031553_0d173bd4, 20261102T035849_c9a3c4d2, 20261102T043557_1289f578
K-02 | 20261102T031646_79c8cbfd, 20261102T033725_a1f418eb, 20261102T035942_d0fe6f25
C-01 | 20261102T031738_101b261c, 20261102T033816_fc8b779a, 20261102T040033_7ef1ab94
C-02 | 20261102T031832_60feab00, 20261102T033910_ed59eabf, 20261102T040126_63e79603
C-05 | 20261102T031928_3537858e, 20261102T034004_608b7594, 20261102T040221_f811c6db
C-06 | 20261102T034052_fd51ea46, 20261102T040309_c42623a7, 20261102T043649_857bd975
G-01 | 20261102T034202_46b9ec30, 20261102T040419_5ec2c341, 20261102T043759_068e516c
G-02 | 20261102T032212_0cec65a0, 20261102T034314_84236e71, 20261102T040531_db5e6ed4
G-04 | 20261102T034434_1318cb7a, 20261102T040651_a9cd581e, 20261102T043911_0c19b6e6
W-01 | 20261102T032408_96643728, 20261102T034553_daab5ed5, 20261102T040810_431b5bb2
T-01 | 20261102T032538_cc8937f6, 20261102T034723_48f9c5e6, 20261102T040939_a7a78ce0
H-02-4KG | 20261102T034836_99981da4, 20261102T041052_44dc29ba, 20261102T044030_6307e9d3
K-01-4KG | 20261102T034927_d50d783b, 20261102T041144_e7b6615b, 20261102T044122_1459d3c1
G-01-4KG | 20261102T035019_5e8362f8, 20261102T041236_659b61c8, 20261102T044213_5594ff85
G-04-4KG | 20261102T032907_ff522d98, 20261102T035130_6d9ed498, 20261102T041347_917770b8
K-01-LD | 20261102T033026_42971abc, 20261102T035249_64610a93, 20261102T041506_77738ae0
G-04-LD | 20261102T033119_fdd2a0c9, 20261102T035341_f17fb004, 20261102T041558_1bef3fa3
W-01-LD | 20261102T033239_16de1a49, 20261102T035501_5f779f96, 20261102T041718_4621ca45
```
Excluded: H-01 `de0daa39`, `e7e1d842`; C-06 `822ef3b3`; G-01 `2b3321e2`; G-04 `ca564dcf`; H-02-4KG `aac2b923`; K-01-4KG `54b0c263`; G-01-4KG `c873f232`; K-01 `aa3d9875`; N-01 `3547bf7b`.
Control: `929412af`, `24132759`, `54630a16`, `b0e27690`, `527dd9de`, `8247632f`, `fc183c36`, `24ae4488`, `8cc9caa0`, `89c00e7e`, `6fc76708`, `0a4620ff`.

