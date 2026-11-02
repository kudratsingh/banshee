# WO-027 — Onboard nodes split into a Python 3.10 package

**Status:** passed
**Date:** 2026-11-02 · **Author:** claude-code-banshee · **Work order:** WO-027 · **Phase:** D2 (not started)
**Program link:** PROGRAM §5.1

> Results are labelled **measured**, **estimated**, **mocked/fixture** or **not run**. Unit tests only; nothing ran in the simulator.

## 1. What changed
- **`onboard/src/banshee_onboard/`:** `freshness`, `gate`, `response`, `guidance`, `frames`, `mission` (the ROS 2 node) and `injection`, which the node uses for simulator faults. Its own `onboard/pyproject.toml` requires Python ≥ 3.10 and has no dependencies; ROS 2 provides `rclpy` and `px4_msgs`.
- **None of these modules imported ironclad before the move,** so nothing changed in behaviour. The move only changed relative imports.
- **`banshee.offboard.mission` stays as a launcher.** The frozen fault matrix stops the node with `pkill -f banshee.offboard.mission`, and the D1 commands use that name.
- **Off-board code may import onboard code, and never the reverse.** `banshee.faults.case_env` now imports `banshee_onboard.injection`.
- **Tests:** onboard-only tests moved to `onboard/tests/` (45, with a boundary test that bans `ironclad` and `banshee` imports and standard-library modules newer than 3.10). The rest stay in `tests/`.
- **CI:** a job `onboard (python 3.10)` installs only pytest and runs the onboard tests. `make type` also runs mypy on `onboard/src` as 3.10. `make onboard-py310` runs the same tests locally on 3.10 with uv.
- **The project's `requires-python >= 3.12` is unchanged,** as the owner said.

## 2. Results (measured, on the CPU tier)
| Check | Result |
|---|---|
| `make check` on 3.13 | passes |
| Onboard tests on Python 3.10.22 (uv) | 45 passed |
| mypy, `--python-version 3.10`, onboard | no issues in 8 files |

## 3. Limits
- The node itself was not run on 3.10 here; WO-025 ran it in the Humble VM before the move, from the same source.
- **The new CI job is not a required check** until the owner adds it to the branch rules.
- `evals/D1-exit-tests.json` still names `src/banshee/freshness.py` as its consumer. The file is frozen; `docs/ARCHITECTURE.md` records the move.

## 4. Verification
`make check` and `make onboard-py310` pass. CI only, under the owner's rule.
