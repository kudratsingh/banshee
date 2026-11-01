# ENVIRONMENT.md — what runs where, bootstrap, and unresolved pins

## 1. Two environments, kept apart

| Environment | Purpose | Platform | Pinned by |
|---|---|---|---|
| **Tooling env** (`requirements-dev.txt`) | CPU-tier checks: lint, types, unit and contract tests, hash/secret/link checks, status board | any OS with Python ≥ 3.12 (tested: Python 3.13.18 on Linux at packaging time; the owner's Macs qualify) | `requirements-dev.txt` |
| **Flight-stack env** | PX4 SITL + Gazebo + ROS 2 + the ROS 2/PX4 bridge + QGroundControl; later the sensor drivers and VIO | **Ubuntu (22.04 or 24.04) — native, a VM on the Mac (UTM/Parallels), or a container.** ROS 2 + Gazebo + PX4 together are Ubuntu-only in practice. No GPU needed for SITL | `config/stack-lock.resolved.json` (does not exist yet; WO-001 proposes, WO-002 tests) |

Never install the flight stack into the tooling env. Never force the tooling pins onto ROS 2's Python.

## 2. Bootstrap (tooling env)
```bash
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check && make board
```

## 3. Bootstrap (flight-stack env) — proposed, unverified
WO-001 proposes and WO-002 tests. Proposed starting point (**proposed, not tested** here; record the exact versions you install):
- Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + a PX4 release documented as supporting that pairing (the reference bundle cites PX4 v1.17 docs [S6]; confirm the release notes), the matching `px4_msgs`/uXRCE-DDS bridge, QGroundControl.
- A VM on the MacBook is enough for SITL; a Linux laptop or the owner's future workstation is better for latency measurements.
- Pin PX4 by commit, ROS 2 by distribution + package lock, Gazebo by version, bridge by commit, QGC by version; record the OS image digest if a container is used.

## 3a. The SITL VM and its bounds (owner, 2026-10-31)
SITL runs in a dedicated Lima VM, `banshee-sitl`, set up by `src/banshee/sitl/vm/`, so no shared Docker daemon is started and only this repository is mounted, read-only.
- **VM disk:** a fixed maximum of 60 GiB (`disk: 60GiB` in `banshee-sitl.yaml`), so a runaway inside the VM cannot fill the Mac. This does not bound a file written on the host, which is what the next two bounds are for.
- **Long runs:** `run_provision.sh`, through `banshee.sitl.bounded`, gives no stdin, a 3-hour limit and a 200 MB log cap, and reaching either stops the run.
- **Free space:** it refuses to start with under 20 GB free on the host or in the VM.
- **PX4:** setup builds with `make px4_sitl_default`. `make px4_sitl gz_x500` starts PX4, even with `DONT_RUN` set.

If neither Jazzy nor Humble runs on arm64, stop and report; the owner's fallback is an x86 Linux machine.

## 4. The owner's machines
- MacBook Pro (M3 Pro, 36 GB) and iMac (16 GB): tooling env, docs, CAD, an Ubuntu VM for SITL.
- Future Linux workstation (`PROGRAM.md §9`): native SITL, VIO development, world-model work; not required for D0–D1.

## 5. Stack lock discipline
`config/stack-lock.pending.json` lists required pins; `null` is a blocker, not "use latest". WO-001 writes `config/stack-lock.proposed.json` (every entry *proposed* with evidence URL and date); WO-002 writes `config/stack-lock.resolved.json` with entries marked *tested* after SITL runs. A changed pin is a new lock version; old versions stay.

## 6. Isolation
Own ROS 2 domain id (`ROS_DOMAIN_ID`) and uXRCE-DDS/MAVLink ports per instance; own `runs/`; never kill processes you did not start (`AGENTS.md §1.3`). Never connect to a physical flight controller during D0–D1 (`AGENTS.md §13`).

## 7. Unverified at packaging time (2026-10-31)
WO-001 proposes these with dates and evidence in `config/stack-lock.proposed.json` and ADR-0007. None is tested. PX4 v1.17's guide states Humble on Ubuntu 22.04, so the Jazzy pairing in section 3 is what WO-002 tests first.
