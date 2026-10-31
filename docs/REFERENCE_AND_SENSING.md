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
**Accuracy target.** Static RMS ≤ 2 cm across the flight volume, coverage ≥ 90%, as ET-D2-3 proposes. **This target is unproven at this price.** Published figures: 2–9 mm at 2.8–8.9 m with a full-frame camera and several photos; a 48 cm tag at 4 m with 2-sigma height error of 4.5 cm static and 0.32 m in flight [D35]; 3–5.5% error at 3–7 m with a 184 mm tag on a small drone [D36]. Error along the camera's axis is the weak direction, so a single webcam will not meet it. If qualification misses the target, VIO evaluations are inconclusive (ET-D2-3); the target is not relaxed afterwards.

**Cameras.** Two Logitech C920s, $69.99 each, fixed focus set and autofocus off. Rolling shutter is inferred, not stated, so the dynamic test measures the skew. The first choice was a global-shutter camera, but the sizing below rules out the 120° Waveshare OV9281, and the 70° Arducam B0332 could not be priced or confirmed in stock. Swap to it if stock is confirmed.

**Tag size.** Smallest tag that can be detected, `t = z·p·r/f`, with p = 5 pixels per module [D34] and r = 5 modules for `tagStandard41h12` [D37]. The pinhole focal length comes from nominal field of view, and detection is not accuracy, so real tags must be larger.

| Camera | f (px) | t at 3 m | t at 4 m | t at 6 m |
|---|---:|---:|---:|---:|
| C920s, 78° diagonal, 1920 × 1080 | 1360 | 5.5 cm | 7.4 cm | 11 cm |
| Arducam B0332, 70° horizontal, 1280 wide | 914 | 8.2 cm | 11 cm | 16 cm |
| Waveshare OV9281, 120°, axis unstated, taken as horizontal | 370 | 20 cm | 27 cm | 41 cm |

The Waveshare would need a tag wider than the X500's 144 mm body at any of these distances, which is why it is out.

**Tag array, per airframe.** Tags are at known rigid offsets, placed symmetrically about the aircraft's centre to avoid a lever-arm error [D35]; three tags did as well as five or nine in simulation there.
| Airframe | Array |
|---|---|
| X500 V2 | three 12 cm tags on a rigid plate above the top plate, for a garage reach near 6 m; about 40 g *estimated* |
| Option B-1 (QAV250) | three 8 cm tags, for a room reach near 4 m; mass counts against the same payload as the guards |
| Starling 2 | no margin confirmed: about 85 g is available, and guards draw on it too |

**Placement and coverage.** Mount both cameras rigidly to walls, at about 2 m, with their axes crossing at 60–90° over the middle of the volume, so one camera's weak axis is the other's strong one. Tripods are not used, because a bump invalidates calibration. Map coverage on a 0.5 m grid before any evaluation.

**Synchronization.** No hardware trigger is available on these cameras. Timestamp frames on one logger's monotonic clock and measure the offset with an LED or a moving target. One published webcam result averaged about 13 ms [D38], which at 1 m/s is about 1.3 cm and already a large part of the 2 cm target. Report the measured figure with every error metric.

**Session check.** At every session start, and after any bump, camera setting change or tag replacement: place the array at a surveyed mark, compare to the recorded pose, and stop if the difference exceeds 2 cm. Record the calibration ids.

## Cost (planning)
Two webcams at $69.99 are priced in `docs/BOM_WORKSHEET.md`. Wall mounts, the printed tag array, a backing plate and a tape or laser measure are unpriced and fall under its contingency.
