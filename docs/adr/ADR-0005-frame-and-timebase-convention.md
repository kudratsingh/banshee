# ADR-0005 — Frame and timebase convention

**Date:** 2026-10-31 · **Status:** accepted · **Work order:** WO-002 · **Program link:** PROGRAM §5.1

## Context
PX4 works in NED and FRD. ROS 2 and this project's contract records use ENU and FLU. A swapped axis or sign at that boundary is a classic and dangerous error, so one place must own the conversion.

## Decision
- **Internal:** ENU world frame (`enu_local`, origin at the EKF start point) and FLU body frame, in m, m/s, rad and rad/s.
- **The boundary:** `src/banshee/offboard/frames.py` is the only conversion. To NED: north = ENU y, east = ENU x, down = −ENU z. It is its own inverse. Yaw rate changes sign between FLU and FRD. NED heading converts to ENU yaw as π/2 − heading.
- **Clock:** decisions and receipts use the VM's monotonic clock, in ns. A PX4 sample time is mapped by adding the smallest offset to receipt seen in the run, so a capture time never falls after its receipt. That mapping hides any fixed latency in the offset, so capture-to-receipt time here is a lower bound. The method is stored in each episode as its alignment artifact. Unavailable times are null, never guessed.
- **Tests:** `tests/test_offboard.py` checks each axis and sign, so a swapped axis fails.

## Alternatives considered
| Option | Why not |
|---|---|
| Work in NED throughout | the contract and ROS 2 use ENU and FLU, so conversions would scatter |
| PX4's offboard frame-transform helpers | an extra dependency, for a few lines this project must be able to test |

## Consequences
Any new interface to PX4 goes through `frames.py`. Measured latency needs a better clock mapping than this, which D2 must supply on hardware.

## Reversibility
Cheap before real episodes accumulate. Afterwards, records keep their declared frame, so a change would be a new export version.
