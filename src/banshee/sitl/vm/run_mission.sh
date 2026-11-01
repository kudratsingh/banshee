#!/usr/bin/env bash
# One SITL mission inside the VM: a fresh PX4 and Gazebo, the agent, the mission node, and the ULog
# copied out. Simulation only. Bounded: time limits, capped logs, no stdin. Stops what it started.
# Usage: run_mission.sh <repository path> <output directory in the VM>
set -uo pipefail
repo="$1"
out="$2"
WORK="$HOME/sitl"
mkdir -p "$out"
# shellcheck disable=SC1091
source "$repo/src/banshee/sitl/vm/common.sh"
trap cleanup EXIT
cleanup
check_versions || exit 3
start_stack 280
read_back
timeout 240 python3 -m banshee.offboard.mission --route "$repo/evals/D1-route.json" \
  --evals "$repo/evals/D1-exit-tests.json" --out "$out" --timeout-s 200 </dev/null 2>&1 | head -c 2000000 >"$out/mission.log"
code=${PIPESTATUS[0]}
copy_ulog
echo "mission exit $code"
exit "$code"
