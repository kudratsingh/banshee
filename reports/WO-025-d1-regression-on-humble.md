# WO-025 — D1 regression re-run on ROS 2 Humble

**Status:** passed. D1's results hold on Humble, in simulation.
**Date:** 2026-11-02 · **Author:** claude-code-banshee · **Work order:** WO-025 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Everything here is measured in simulation on `gz_x500`. Nothing ran on hardware or on the X650 proxy.

## 1. Why
The owner's decision of 2026-11-02: "If D1 ran on Jazzy, re-run the D1 regression on Humble and report it." D1 ran on Jazzy: `config/stack-lock.resolved.json` reads Ubuntu 24.04.5, `ros-jazzy-ros-base` 0.11.0.

## 2. The Humble stack
A second Lima VM, `banshee-sitl-humble`, so the Jazzy VM stays as the record. `config/stack-lock.humble.resolved.json`, read from the installed tools:

| Pin | Jazzy (D1 record) | Humble (here) |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS | Ubuntu 22.04.5 LTS |
| ROS 2 base | 0.11.0-1noble | 0.10.0-1jammy.20260916 |
| Gazebo Harmonic | 1.0.0-1~noble | 1.0.0-1~jammy; gz-sim 8.15.0 in both |
| PX4, agent, px4_msgs | d6f12ad1, 73622810, 86d8239e | the same commits |

`BANSHEE_STACK=humble` selects the VM and its lock (`src/banshee/sitl/stack.py`); unset, everything runs on Jazzy as before. Gazebo lists Harmonic with Humble as "use with caution" [D10]; nothing here showed a problem.

## 3. Results (measured, against the latest Jazzy record: `runs/regression-d1-wo016/`, `runs/fault-matrix-wo016-rec/`)
| D1 test | Threshold | Humble | Jazzy |
|---|---|---|---|
| ET-D1-1, versions | identical; no null pins | every run's manifest matches the Humble lock | match |
| ET-D1-2, nominal missions | 10/10 reach every waypoint within 0.5 m | **10/10;** worst miss 0.21 m by the estimate, 0.35 m by ground truth | 10/10; 0.21 m, 0.33 m |
| ET-D1-3, contract | 100% valid | **10/10** episodes valid (`ironclad-validate`) | 10/10 |
| ET-D1-4, fault matrix | all cases executed; deviations reported | **47/47 executed; the same 7 deviations** (L-02, R-04, G-01, G-02, V-01, V-02, V-03), on the same checks | the same |
| Mode sequence after each fault | — | identical in every case | — |

**Differences over 0.5 m and 15%, none against a threshold:**
- R-06, Altitude mode after position loss with no wind: 1.63 m of travel against 0.35 m. It measures drift, and its checks (mode within 4 s, held 15 s, operator latch) match.
- N-01, no fault: climbed to 5.55 m against 4.74 m on a 5 m route. Its horizontal check passed.

Each is one recording, so I cannot say whether they come from the distribution or from chance.

**Gate trips:** no armed `estimator stale` verdict before a fault in the 47 cases. This does not explain WO-022's trips, which are still required in the D2 report.

## 4. For the Jetson
The node ran on Python 3.10.12, Humble's Python, from source. `pyproject.toml` still reads `requires-python >= 3.12`, so installing the package on JetPack 6.2.2 will need that lowered, or the node run from source as here. Not changed in this work order.

## 5. Limits
One recording of each case, where D1 used four. X500 model only. The cause of the two differences is not established.

## 6. Verification
`make check` passes. Run IDs are in `runs/regression-d1-humble/campaign.log` and `runs/fault-matrix-humble/matrix.jsonl`; every run is in `ledgers/runs.jsonl`. The Humble VM is stopped.

## 7. Retro
Making the stack a switch, not a second copy of the scripts, kept the Jazzy record untouched and the change small.
