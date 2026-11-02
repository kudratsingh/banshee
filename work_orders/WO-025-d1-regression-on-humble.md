# WO-025 | Re-run the D1 regression on ROS 2 Humble
**Phase:** D2 (not started); simulation only
**Exit tests advanced:** none; it reports whether D1's evidence holds on Humble
**Size:** M
**Prerequisites:** WO-023 accepted.
**Authorization:** the owner's decision of 2026-11-02: "If D1 ran on Jazzy, re-run the D1 regression on Humble and report it." D1 ran on Jazzy (`config/stack-lock.resolved.json`: Ubuntu 24.04). Simulation only; no hardware.
**Files:** reads `evals/D1-route.json`, `evals/D1-fault-matrix.json` and the thresholds in `evals/D1-exit-tests.json`; writes a new Lima VM and its setup scripts under `src/banshee/sitl/vm/`, a Humble stack lock under `config/`, `reports/WO-025-d1-regression-on-humble.md`, `ledgers/runs.jsonl`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
Run the D1 regression missions and the fault matrix on Ubuntu 22.04 and ROS 2 Humble, with PX4 at the same commit, and report any difference from the Jazzy record.

## Scope
A second VM, so the Jazzy VM stays as the record. The same cases and recordings as D1's regression. A case holds on Humble if it meets its frozen D1 threshold. Gazebo lists Harmonic with Humble only as "use with caution" [D10], which is part of what this tests. **Every long command runs under a time limit, with no stdin and a capped log, and the new VM gets a disk budget,** because an uncapped log once filled the disk. The project's `requires-python >= 3.12` must be checked against Humble's Python 3.10: the source parses as 3.10, which is not a run. The node, unchanged, unless Humble needs a change, which is then reported.

## Out of scope
The X650 proxy, unless asked. Hardware.

## Verification
```bash
make check
```
The recordings on Humble, compared case by case with D1's.

## Stop conditions
The stack does not install on arm64 Ubuntu 22.04, or a D1 case that passed on Jazzy fails on Humble: report, do not change the case to fit.

## Report
`reports/WO-025-d1-regression-on-humble.md`
