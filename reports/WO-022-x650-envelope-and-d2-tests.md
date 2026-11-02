# WO-022 — Envelope recomputed for the X650; D2 exit tests updated

**Status:** stop condition fired. On a simulated proxy of the X650, the owner's 150 m position-lost rule is not met above 10 m. Reported with options; nothing was adjusted to fit. The standoffs and D2 tests are done. No result exists for a real X650.
**Date:** 2026-11-01 · **Author:** claude-code-banshee · **Work order:** WO-022 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. "Measured" here means measured in simulation on the proxy, on PX4 commit d6f12ad1. Nothing ran on hardware.

## 1. Result
| Value | X500 (kept as record) | X650 | Label |
|---|---:|---:|---|
| Standoff at 2.5 m/s | 8.6 m | **8.7 m, frozen** | reaction and error estimated; braking measured on the proxy |
| Standoff at 1.0 m/s | 3.35 m | **3.4 m, frozen** | same |
| Overrun margin | 9 m | **9 m, frozen** | 8.7 m rounded up |
| Exclusion radius | 150 m | **150 m, frozen** | 40 + 9 + 100 = 149 m, rounded up |
| Position loss alone, reach at the table's limits | 139.5–144.9 m, estimated | **up to 169.6 m; rule not met above 10 m** | measured, plus an estimated 5 s delay |
| Crew from Home | 50 m | **85 m and upwind, proposed** | estimated; the owner has not named it |

`evals/D3-standoffs-x650.json` holds these. `evals/D3-standoffs.json` stays as the X500's record. `evals/D2-exit-tests.json` is now sha256 `f543c93eb3ee6c6d059781141baee6b21578d41c9128e29b97239245c41ada0c`; it was `0ac32802c5691662abca0fe7f81c0df46e1151176ba88624e3fbff0a448b8131`.

## 2. The 150 m rule: not met above 10 m
**This corrects my first draft, which said the rule held by 0.9 m.** The independent review showed that the draft used a carried-speed term from a 5 m flight, where the ground cuts it short with the aircraft still moving, and applied it at up to 25 m. So I measured each row directly: position lost about 32 m out (the 30 m flight box plus the 2 m position error), flying downwind at 2.5 m/s, three usable runs per row and drag. Reach is ground truth from Home to the end of the ground slide. The two right-hand columns add 5 s of operator delay, *estimated* as wind × 5 s.

| Wind, height | Nominal drag | Half drag | Double drag | Nominal, with delay | Worst, with delay |
|---|---:|---:|---:|---:|---:|
| 5 m/s, 10 m | 89.3–99.8 m | 82.4–90.2 m | 102.2–113.9 m | 124.8 m | **138.9 m, inside** |
| 4 m/s, 14 m | 106.2–108.7 m | 97.6–112.7 m | 108.2–149.6 m | 128.7 m | **169.6 m, past** |
| 3 m/s, 20 m | 117.6–131.6 m | 116.0–123.7 m | 121.6–135.7 m | 146.6 m | **150.7 m, past** |
| 2.5 m/s, 25 m | 132.1–143.4 m | 127.5–144.2 m | 128.6–137.6 m | 155.9 m | **156.7 m, past** |

- **Only the 25 m row breaks at nominal drag.** The 14 m and 20 m rows break only at double drag, and the 14 m row through one 35 m slide after a tumble. The X650's drag is not known, and simulated ground contact is not validated.
- **The drift formula is not a bound.** The proxy exceeded the wind speed at the lower winds: up to 3.9 m/s in 2.5 m/s of wind. Cause not established. Not run on the x500, so I do not know whether the X500's arithmetic had the same gap.
- **Wind shear is not in these numbers.** The limit is read near the ground. A 1/7 power law from 1.5 m gives 1.15–1.31 times that wind averaged over the descent (*estimated*), which could take the 10 m row to about 143 m at nominal drag and 159 m at double drag.
- **Position loss at the fence's edge** starts about 17 m further out, and is a second failure.

### Options for the owner
| Option | What changes | Reach (worst measured, with delay) | Cost |
|---|---|---:|---|
| **A, recommended:** cap at 10 m and lower the wind limit | ≤ 10 m at every stage until flight logs replace this; handheld wind ≤ 4 m/s, not 5 | **138.9 m, 11 m inside;** 4 m/s on the handheld is about 4.6 m/s averaged over the descent with shear, so the 5 m/s row covers it (*estimated*) | Fewer flying days; D4+ viewpoints stay at or below 10 m |
| B: raise the radius | Keep the table; radius 170 m | 169.6 m, not counting shear, which could reach about 197 m at 25 m (*estimated*) | Field about 340 m across |
| C: shrink the flight box | Keep the table and 150 m; box 23 m, or 10 m to cover the tumble | 150 m | Much less room to fly, and shear not covered |

D2 flies nothing, so this does not hold up D2. It must be settled before D3, and D3 is already ≤ 10 m. **The envelope's table is unchanged, with the rows above 10 m marked,** until the owner decides.

## 3. The proxy
PX4's x500 model, with mass 5 kg (and 4 kg), arm 0.23 m and 3.0 kg of thrust per motor. Published: 650 mm wheelbase, 2,000 g kit. Estimated: thrust per motor, inertia scaled as m·L², motor time constants 0.10 and 0.15 s. **Drag is set so that deceleration per unit speed equals the x500's at every mass,** then varied by half and double. It is a stand-in, not a model of the X650. Not modelled: real motor response, prop aerodynamics, vibration, the frame's own drag.

## 4. Other measurements (simulation on the proxy; three usable runs per case)
| Term | Case | 5 kg | 4 kg | Half drag | X500 (WO-004) |
|---|---|---:|---:|---:|---:|
| Braking from 2.5 m/s, net of 0.2 s | H-02, K-01 | 3.01–3.15 m | 3.03–3.26 m | 3.01–3.05 m | 3.0–3.2 m |
| Braking from 1.0 m/s, net of 0.2 s | H-01, K-02 | 0.90–1.04 m | not run | not run | 0.93–1.02 m |
| Lost stream, travel at 2.5 m/s | C-02 | 5.81–5.90 m | not run | not run | 5.70–5.92 m |
| Lost stream, travel at 1.0 m/s | C-01 | 2.04–2.07 m | not run | not run | 2.03–2.26 m, four cases |
| Fence overrun, horizontal | G-01 | 3.28–3.48 m | 3.44–3.67 m | not run | 3.82–3.94 m |
| Fence overrun above 14 m | G-02 | 0.48–0.79 m | not run | not run | 0.53–0.68 m |
| Climb, C-05 | C-05 | 1.50–1.57 m | not run | not run | 1.45–1.50 m |
| Vertical travel, C-06 | C-06 | 0.70–0.75 m | not run | not run | 0.70–0.71 m |
| Return, peak speed | T-01 | 2.67–2.69 m/s | not run | not run | 2.67–2.69 m/s |
| Carried from 5 m, no wind | G-04 | 12.4–12.8 m | 12.3–12.5 m | 15.2–17.2 m | 12.5–13.1 m |
| Wind drift, 5.4 m/s, 10 m, with slide | W-01 | 41.3–60.9 m | not run | 25.0–26.5 m | 40.9–46.1 m |

**Braking did not move with mass, as expected:** PX4's limit is an acceleration, and 3 m/s² needs a thrust-to-weight of only about 1.05. **The agreement between masses on G-04 and W-01 is built into the proxy** by how drag is set, so it is not a finding. A further usable G-01 run at 5 kg reached 3.64 m, outside the first three. At the proxy's measured 2.5–2.63 m/s the reaction term would make the 8.7 m standoff about 8.8 m, still under the 9 m margin; I kept the nominal speed, as on the X500.

One W-01 run tumbled on touchdown: 17.85 m/s peak and a 3.9 m rebound. Read this as "a drifting landing may flip", and not as a distance.

## 5. The props and the crew (*estimated*, no test)
Ballistic with quadratic drag and an assumed area, 25 m release, best angle: 2–5 g tumbling fragments land within 48–55 m in still air and about 72 m downwind at 5 m/s; a 15 g half blade within 27–31 m. **That supports "tens of metres". It is not a bound:** halving the area gives about 95 m in still air and 114 m in wind, and a chip flying stably edge-on reaches 311–432 m in the same model, which is not credible for a tumbling piece but is not excluded. I found no basis to move the 100 m bystander distance, which is PX4's rule of thumb and names no mass. **I propose moving the crew from 50 m to 85 m from Home, upwind of the box. The owner has not named this.**

## 6. D2 exit tests
Thresholds carry over. Changes, before any result exists:
- **ET-D2-1** names the OAK-D Pro W and the Orin NX on the baseboard, and must report the unit's factory distortion model and whether the VIO candidate accepts it.
- **ET-D2-2** adds the ARK Flow MR's flow and range, reported, with no threshold.
- **ET-D2-4 changes method, which the owner's instruction did not name, so the owner is asked to accept it.** The link runs in board traces, so nothing can be unplugged. The cut is made on the Jetson: Ethernet interface down, or the XRCE-DDS agent stopped for the UART. The report must name the path carrying offboard and show that the other carries no setpoints. This is weaker than a physical cut.
- **ET-D2-5** names the 6X on the baseboard, and adds the ARK Flow MR over DroneCAN. The ARKV6X note is gone.
- **Required in the D2 report:** sunlight now reads OAK-D Pro W; power now reads the UBEC at 7.2 V on 6S; the gate finding below is added.

**Not changed:** the Jetson stack, which waits on the owner. Connecting the flight controller and the link cut each still need a dated owner approval.

## 7. Finding: the gate tripped before the fault in 11 of 131 runs
Each saw `estimator stale` at an armed tick, first at 102–157 ms against the 100 ms bound, and one tick can latch Land. In the first 63 runs there were 10 (95% interval 8.9–26.8%): six in flight and four at or near the ground. Then 0 in 31 (0–11.0%: 19 proxy runs and the 12 control runs), then 1 in the 37 position-lost runs. D1 reported a `continue` verdict at every armed tick in 40 X500 missions. Spurious in-flight Lands are the part that matters.

**Cause not established.** What is known:
- Two hypotheses remain. Most tripped runs kept a high age, which fits the clock mapping in `src/banshee/offboard/mission.py`, which keeps the smallest offset seen. But `c873f232` tripped on one tick at 104 ms and `3547bf7b` on two, which fits jitter at least as well. `ca564dcf` also has one mapped capture time near −1.79e18 ns, which bears on the mapping.
- A stall over 300 ms appears in 24 of 63, 10 of 19, 7 of 12 and 12 of 37 runs, so it did not fall when the trips did. It alone does not explain them. Run `9c250368`, in the clean group, had a median age of 70 ms.
- **The control does not settle whether the proxy matters.** N-01 alternated between x500 and the proxy, 6 each, with no trips on either. Another project's process was using one core when I looked; I did not stop it, and I do not know whether it ran during the first recording.
- Two tripped runs, G-04 `ca564dcf` and PL-3 `041219ff`, had the gate's response off by design. PL-3 still entered Land. I did not explain that.

**Effect on the numbers.** The rule: a run is usable if the trigger fired and no mode other than offboard came before it, and the first three usable runs in time order are used. **I fixed that rule after seeing the first 63 runs,** and before the further recordings. The independent review checked that no later usable run exceeds a frozen term, so exclusion biases none low. Two usable runs, K-01-4KG and H-02-4KG in recording 2, tripped to Land after the fault; K-01-4KG's sets the 3.26 m, so they raise the braking term. The gate code and its bound did not change.

## 8. Other disclosures
- The first proxy smoke run failed on an invalid inertia, from my replacing text in the model; that is fixed, tested, and the failed run stays in `runs/`.
- Expected values in the proxy case files are the X500's. G-01 and G-02 show the same 5 s hold deviation as in D1, a known error in those expected values.
- Hover time is scaled, not published: Holybro's 30 min on 6S 10 Ah is with no added payload. The ≤ 8 min plan stays.
- The generated model files were not read back in the review, because the VM was stopped; hover thrust and parameter dumps from the runs support them.

## 9. Verification and review
`make check` passes. 131 runs recorded across three sets, plus one smoke run of PL-2p5, `20261102T051639Z_ee248af2`, not used; none failed to execute.

**Independent review (read-only, recomputed from the raw data).** It found: the carried term cut short, so the 0.9 m margin was unsound (high, fixed by §2's direct measurement); terms the margin left out, such as shear and position error (high, §2); "mass did not matter" being built in for carried and wind, with a wrong reason (high, §4); the gate split wrong, and my claim that age stayed high false for two runs (medium, §7); the fragment estimate overused (medium, §5); ET-D2-4 under-specified (medium, §6); and smaller items, all fixed. A second pass on the changes: see §12.

## 10. To reproduce
```bash
limactl shell banshee-sitl -- bash -c "PYTHONPATH=$PWD/src python3 $PWD/src/banshee/sitl/x650_proxy.py --px4 ~/sitl/PX4-Autopilot"
PYTHONPATH=src python -m banshee.faults.run_matrix --matrix evals/X650-proxy-cases.json
PYTHONPATH=src python -m banshee.faults.run_matrix --matrix evals/X650-proxy-control-cases.json
PYTHONPATH=src python -m banshee.faults.run_matrix --matrix evals/X650-position-lost-cases.json
```

## 11. Runs used
```
N-01 | 20261102T031317Z_6fef89d0, 20261102T033409Z_8867388e, 20261102T043411Z_d95ac714
H-01 | 20261102T035705Z_c970b9ef, 20261102T043505Z_0afa2c5b, 20261102T044419Z_86580a3c
H-02 | 20261102T031500Z_d7929f04, 20261102T033539Z_9fd288a9, 20261102T035757Z_cc9820dd
K-01 | 20261102T031553Z_0d173bd4, 20261102T035849Z_c9a3c4d2, 20261102T043557Z_1289f578
K-02 | 20261102T031646Z_79c8cbfd, 20261102T033725Z_a1f418eb, 20261102T035942Z_d0fe6f25
C-01 | 20261102T031738Z_101b261c, 20261102T033816Z_fc8b779a, 20261102T040033Z_7ef1ab94
C-02 | 20261102T031832Z_60feab00, 20261102T033910Z_ed59eabf, 20261102T040126Z_63e79603
C-05 | 20261102T031928Z_3537858e, 20261102T034004Z_608b7594, 20261102T040221Z_f811c6db
C-06 | 20261102T034052Z_fd51ea46, 20261102T040309Z_c42623a7, 20261102T043649Z_857bd975
G-01 | 20261102T034202Z_46b9ec30, 20261102T040419Z_5ec2c341, 20261102T043759Z_068e516c
G-02 | 20261102T032212Z_0cec65a0, 20261102T034314Z_84236e71, 20261102T040531Z_db5e6ed4
G-04 | 20261102T034434Z_1318cb7a, 20261102T040651Z_a9cd581e, 20261102T043911Z_0c19b6e6
W-01 | 20261102T032408Z_96643728, 20261102T034553Z_daab5ed5, 20261102T040810Z_431b5bb2
T-01 | 20261102T032538Z_cc8937f6, 20261102T034723Z_48f9c5e6, 20261102T040939Z_a7a78ce0
H-02-4KG | 20261102T034836Z_99981da4, 20261102T041052Z_44dc29ba, 20261102T044030Z_6307e9d3
K-01-4KG | 20261102T034927Z_d50d783b, 20261102T041144Z_e7b6615b, 20261102T044122Z_1459d3c1
G-01-4KG | 20261102T035019Z_5e8362f8, 20261102T041236Z_659b61c8, 20261102T044213Z_5594ff85
G-04-4KG | 20261102T032907Z_ff522d98, 20261102T035130Z_6d9ed498, 20261102T041347Z_917770b8
K-01-LD | 20261102T033026Z_42971abc, 20261102T035249Z_64610a93, 20261102T041506Z_77738ae0
G-04-LD | 20261102T033119Z_fdd2a0c9, 20261102T035341Z_f17fb004, 20261102T041558Z_1bef3fa3
W-01-LD | 20261102T033239Z_16de1a49, 20261102T035501Z_5f779f96, 20261102T041718Z_4621ca45
PL-5 | 20261102T051905Z_53b69a7c, 20261102T054125Z_89bdb3a7, 20261102T060346Z_ceaf8736
PL-5-LD | 20261102T052038Z_03520a03, 20261102T054259Z_86b1da18, 20261102T060520Z_82fdea44
PL-5-HD | 20261102T052212Z_84c3a60d, 20261102T054433Z_7608bc9f, 20261102T060653Z_8ec2705d
PL-4 | 20261102T052346Z_8c66cb40, 20261102T054606Z_5daf2e2c, 20261102T060827Z_2cad5bab
PL-4-LD | 20261102T052529Z_9d7ea239, 20261102T054750Z_8e5366bb, 20261102T061011Z_18e0f42f
PL-4-HD | 20261102T052713Z_db785b7f, 20261102T054934Z_bbe1c569, 20261102T061154Z_fb473da5
PL-3 | 20261102T055118Z_6a3cb559, 20261102T061338Z_0f3957b6, 20261102T062728Z_d465ba1d
PL-3-LD | 20261102T053055Z_2653d260, 20261102T055316Z_f8db1978, 20261102T061537Z_131108c1
PL-3-HD | 20261102T053254Z_12c5859f, 20261102T055515Z_6292b387, 20261102T061735Z_5d91b5e4
PL-2p5 | 20261102T053453Z_a2148dd9, 20261102T055714Z_ca4bece3, 20261102T061934Z_4a9c12ca
PL-2p5-LD | 20261102T053703Z_1080fbf7, 20261102T055925Z_b0696948, 20261102T062145Z_18d9479d
PL-2p5-HD | 20261102T053915Z_69e9ebba, 20261102T060135Z_466ae735, 20261102T062356Z_d8315637
```
Excluded: H-01 `de0daa39`, `e7e1d842`; C-06 `822ef3b3`; G-01 `2b3321e2`; G-04 `ca564dcf`; H-02-4KG `aac2b923`; K-01-4KG `54b0c263`; G-01-4KG `c873f232`; K-01 `aa3d9875`; N-01 `3547bf7b`; PL-3 `041219ff`.
Control: `929412af`, `24132759`, `54630a16`, `b0e27690`, `527dd9de`, `8247632f`, `fc183c36`, `24ae4488`, `8cc9caa0`, `89c00e7e`, `6fc76708`, `0a4620ff`.

