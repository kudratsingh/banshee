#!/usr/bin/env bash
# One SITL mission inside the VM: a fresh PX4 and Gazebo, the agent, the mission node, and the ULog
# copied out. Simulation only. Bounded: time limits, capped logs, no stdin. Stops what it started.
# Usage: run_mission.sh <repository path> <output directory in the VM> [route file] [world] [seed]
set -uo pipefail
repo="$1"
out="$2"
route="${3:-$1/evals/D1-route.json}"
world="${4:-default}"
seed="${5:-}"
WORK="$HOME/sitl"
mkdir -p "$out"
# shellcheck disable=SC1091
source "$repo/src/banshee/sitl/vm/common.sh"
export PX4_GZ_WORLD="$world"
# PX4 passes this variable into the gz sim command line; it is the only way to give Gazebo a seed.
if [ -n "$seed" ]; then export PX4_GZ_SIM_RENDER_ENGINE="ogre2 --seed $seed"; fi
trap cleanup EXIT
cleanup
check_versions || exit 3
start_stack 280
read_back
pgrep -af "gz sim" >"$out/gz-cmdline.txt" 2>&1 || true
timeout 240 python3 -m banshee.offboard.mission --route "$route" \
  --evals "$repo/evals/D1-exit-tests.json" --out "$out" --timeout-s 200 </dev/null 2>&1 | head -c 2000000 >"$out/mission.log"
code=${PIPESTATUS[0]}
copy_ulog
echo "mission exit $code"
exit "$code"
