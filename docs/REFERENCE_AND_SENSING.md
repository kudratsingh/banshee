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

## Cost (planning)
Two USB webcams on wall mounts, printed tag array, a tape/laser measure: roughly $100–200; included in the BOM worksheet.
