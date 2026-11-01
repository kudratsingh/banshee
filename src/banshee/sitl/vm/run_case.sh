#!/usr/bin/env bash
# One fault case inside the VM, on the mission's own path. Simulation only. Bounded like a mission.
# A mission that misbehaves is the point of the case, so only setup failures change the exit code.
# Usage: run_case.sh <repository path> <output directory in the VM> <matrix path> <case id>
set -uo pipefail
repo="$1"
out="$2"
matrix="$3"
case_id="$4"
WORK="$HOME/sitl"
mkdir -p "$out"
# shellcheck disable=SC1091
source "$repo/src/banshee/sitl/vm/common.sh"
trap cleanup EXIT
cleanup
check_versions || exit 3
python3 -m banshee.faults.case_env --matrix "$matrix" --case "$case_id" --dir "$out" || exit 5
# shellcheck disable=SC1091
source "$out/case-limits.sh"
# shellcheck disable=SC1091
source "$out/case-env.sh"
limit=$((CASE_TIMEOUT_S + 60))
start_stack "$limit"
# shellcheck disable=SC1091
source "$out/case-after-start.sh" >"$out/after-start.log" 2>&1
read_back
if [ "$CASE_RC" = "1" ]; then
  timeout "$limit" python3 -m banshee.faults.rc_sim --dir "$out" --limit-s "$limit" </dev/null 2>&1 | head -c 200000 >"$out/rc.log" &
fi
timeout "$CASE_TIMEOUT_S" python3 -m banshee.offboard.mission --route "$repo/evals/D1-route.json" \
  --evals "$repo/evals/D1-exit-tests.json" --out "$out" --timeout-s "$((CASE_TIMEOUT_S - 5))" \
  --matrix "$matrix" --case "$case_id" </dev/null 2>&1 | head -c 2000000 >"$out/mission.log" &
node=$!
while kill -0 "$node" 2>/dev/null && [ ! -f "$out/trigger.json" ]; do
  sleep 0.2
done
if [ -f "$out/trigger.json" ]; then
  # shellcheck disable=SC1091
  source "$out/case-timeline.sh" >"$out/timeline.log" 2>&1 &
fi
observe=$(python3 -c "import json,sys; print(int(json.load(open(sys.argv[1])).get('observe_s', 20)))" "$out/case.json")
# The node ends itself; a killed node leaves the rest of the observation to this wait.
if [ -f "$out/trigger.json" ]; then
  sleep "$observe"
fi
wait "$node"
copy_ulog
echo "case $case_id finished"
exit 0
