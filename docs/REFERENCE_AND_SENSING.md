# REFERENCE_AND_SENSING.md — outside-in reference qualification

Fixed, calibrated external cameras observe a known-size rigid tag array mounted on the aircraft. AprilTag gives camera-relative tag pose [S11]; this is a *reference candidate*, not certified motion capture. It is an **evaluator**: in any test that claims unaided VIO performance it is never fed into the onboard estimator.

## Independence
Separate cameras, clocks/loggers and pose estimation from the onboard VIO. Record any shared calibration assumptions. "Independent sensor path" does not mean error-free ground truth; the reference carries its own measured uncertainty, which every position-error metric states.

## Qualification (ET-D2-3)
1. **Static survey.** Place the tag array at known positions across the full test volume (surveyed with a tape or laser measure); record residuals and uncertainty. *Proposed target:* static RMS ≤ 2 cm.
2. **Dynamic.** Move the array along known trajectories (hand-carried along a marked path or on a cart); measure latency and frame alignment; account for timestamp uncertainty in all error metrics.
3. **Coverage map.** Where in the volume both cameras see the array; *proposed target:* ≥ 90% of the planned flight volume. Inadequate coverage makes a VIO evaluation **inconclusive**, not a pass.
4. **Dropout policy.** Predefine how missing reference frames are handled; record them as missing; never interpolate silently.
5. Two cameras improve coverage but require measured extrinsics and time alignment between them.

## Session checks
Document mounts, tag size and rigid transform, focus/exposure and calibration versions. Perform a known-pose check at every session start and after any bump, camera setting change or tag replacement. "Calibrated once" is not permanent validity.

## Storage
Reference streams enter contract exports with `role: reference_only`; model inputs may not consume them by default. Raw reference video and logs are retained like all other data (`docs/DATA_POLICY.md`).

## Plan (WO-001, 2026-10-31; proposed, nothing measured)
**Accuracy target.** Static RMS ≤ 2 cm across the flight volume, coverage ≥ 90%, as ET-D2-3 proposes. **This target is unproven at this price.** Published figures: 2–9 mm at 2.8–8.9 m with a full-frame camera and several photos [D42]; a 48 cm tag at 4 m with 2-sigma height error of 4.5 cm static and 0.32 m in flight [D35]; 3–5.5% error at 3–7 m with a 184 mm tag on a small drone [D36]. Error along the camera's axis is the weak direction, so a single webcam will not meet it. If qualification misses the target, VIO evaluations are inconclusive (ET-D2-3); the target is not relaxed afterwards.

**Cameras.** Two Logitech C920s, $69.99 each, with autofocus off. Rolling shutter is inferred, not stated, so the dynamic test measures the skew. A global-shutter camera was the first choice, but the 120° Waveshare OV9281 cannot reach. The 70° Arducam B0332 could not be priced or confirmed in stock, and it reaches two-thirds as far with the same tag, so using it needs a larger tag or closer cameras.

**Tag size.** `tagStandard41h12` is recommended [D37]. Its *border width* t spans 5 modules and its *printed width* W spans 9, and the outer ring carries data, so W = 1.8 t and it cannot be cropped [D45]. Detection reach is `z = f·t/(p·r)`, with p = 5 pixels per module and r = 5 [D34]. Detection is not accuracy, so plans use two-thirds of that, and multiply by 0.71 for a tag turned 45° to the camera. The focal length comes from nominal field of view.

| Camera | f (px) | Tag | Printed W | Detection | Planning reach | Reach at 45° |
|---|---:|---:|---:|---:|---:|---:|
| C920s, 78° diagonal, 1920 × 1080 | 1360 | t = 15 cm | 27 cm | 8.2 m | 5.4 m | **3.9 m** |
| C920s | 1360 | t = 12 cm | 21.6 cm | 6.5 m | 4.4 m | 3.1 m |
| C920s | 1360 | t = 8 cm | 14.4 cm | 4.4 m | 2.9 m | **2.1 m** |
| Arducam B0332, 70° horizontal, 1280 wide | 914 | t = 15 cm | 27 cm | 5.5 m | 3.7 m | 2.6 m |
| Waveshare OV9281, 120°, axis unstated, taken as horizontal | 370 | t = 15 cm | 27 cm | 2.2 m | 1.5 m | 1.0 m |

**Tag box.** A flat plate on top of the aircraft is edge-on to cameras near flight height, so tags go on the four vertical faces of a light box, and at any yaw a camera sees a face at 45° or better. On the X500: 27 cm faces, on a standoff above the 144 mm top plate, about 90 g *estimated*. This is a large box: its fit, prop clearance and effect on flight are unverified and are checked at D2, and `14 CFR 107.49` requires checking that an attached object does not affect flight.

**Placement and coverage, in the field (owner decision, 2026-10-31).** The reference covers one small evaluation box, not the whole fence. The reach at 45° is 3.9 m, so the flight box for a reference run is 1.5 m square, with both cameras within 3.9 m of its far corner. Cameras are on low tripods, staked to the ground, with their axes crossing at 60–90° so one camera's weak axis is the other's strong one. They sit inside the safety standoff, and they are expendable: nobody stands near them during a flight. A bump invalidates calibration, and a field setup is rebuilt each session, so the survey and session check are repeated every time. Direct sun and glare are a new risk for tag detection, tested in D2. Map pixels per module and coverage on a 0.5 m grid, including the worst corner, before any evaluation.

**Synchronization.** No hardware trigger is available on these cameras. Timestamp frames on one logger's monotonic clock and measure the offset with an LED or a moving target. One published webcam result averaged about 13 ms [D38], which at 1 m/s is about 1.3 cm and already a large part of the 2 cm target. Report the measured figure with every error metric.

**Session check.** At every session start, and after any bump, camera setting change or tag replacement: place the box at a surveyed mark, compare to the recorded pose, and stop if the difference exceeds 2 cm. Record the calibration ids.

## Cost (planning)
Two webcams at $69.99 are priced in `docs/BOM_WORKSHEET.md`. Tripods, ground stakes, the tag box and a tape or laser measure are unpriced and fall under its contingency.
