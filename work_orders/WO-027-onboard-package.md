# WO-027 | Split the onboard nodes into a Python 3.10 package with no ironclad imports
**Phase:** D2 (not started)
**Exit tests advanced:** none
**Size:** M
**Prerequisites:** WO-025 accepted.
**Authorization:** the owner's decision of 2026-11-02. Repository only.
**Files:** `onboard/`, `src/banshee/offboard/`, `src/banshee/faults/case_env.py`, `src/banshee/sitl/vm/common.sh`, `tests/`, `pyproject.toml`, `Makefile`, `.github/workflows/ci.yml`, `docs/ARCHITECTURE.md`, `docs/TEST_PROTOCOL.md`, `src/banshee/__init__.py`, `reports/WO-027-onboard-package.md`, `CHANGES.md`.

Serves `PROGRAM §5.1`.

## Objective
The onboard ROS 2 nodes (freshness gate, command path, offboard bridge) target Python 3.10 and import nothing from ironclad; contract export and all tooling run off-board on 3.12. The project requirement stays at 3.12.

## Scope
Move the modules to `onboard/src/banshee_onboard/`, with their tests, a boundary test and a CI job on 3.10. Keep the launcher path the frozen cases use.

## Out of scope
Changing what the nodes do. Packaging for the Jetson.

## Verification
```bash
make check
make onboard-py310
```

## Stop conditions
An onboard module cannot drop an ironclad import without a change in behaviour: report it, and do not change the behaviour.

## Report
`reports/WO-027-onboard-package.md`
