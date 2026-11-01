#!/usr/bin/env bash
# First SITL check inside the VM: PX4 and Gazebo headless, the agent, and a ROS 2 topic read.
# Simulation only. Every process has a time limit and a capped log; it stops what it started.
set -uo pipefail
WORK="$HOME/sitl"
OUT="$(mktemp -d)"
DISTRO=jazzy
export ROS_DOMAIN_ID=42 HEADLESS=1 PX4_SIM_MODEL=gz_x500 PX4_GZ_WORLD=default
set +u
# shellcheck disable=SC1090
source "/opt/ros/$DISTRO/setup.bash"
# shellcheck disable=SC1091
source "$WORK/ws/install/setup.bash"
set -u
timeout 170 MicroXRCEAgent udp4 -p 8888 </dev/null 2>&1 | head -c 5000000 >"$OUT/agent.log" &
cd "$WORK/PX4-Autopilot/build/px4_sitl_default/rootfs" || exit 2
timeout 170 ../bin/px4 -d </dev/null 2>&1 | head -c 20000000 >"$OUT/px4.log" &
result=1
for _ in $(seq 1 12); do
  sleep 10
  if timeout 15 ros2 topic list 2>/dev/null | grep -q '^/fmu/out/vehicle_status'; then
    result=0
    break
  fi
done
echo "== topics"
timeout 15 ros2 topic list 2>/dev/null | grep -c '^/fmu/' || true
timeout 15 ros2 topic list 2>/dev/null | grep -E 'vehicle_status|vehicle_odometry|offboard_control_mode|trajectory_setpoint' || true
echo "== vehicle_status"
timeout 25 ros2 topic echo --once --field arming_state /fmu/out/vehicle_status_v1 </dev/null 2>/dev/null | head -3 || true
timeout 25 ros2 topic echo --once --field arming_state /fmu/out/vehicle_status </dev/null 2>/dev/null | head -3 || true
echo "== gazebo"
gz sim --versions 2>/dev/null | head -2 || true
pgrep -a 'gz|ruby' | cut -c1-90 | head -3 || true
echo "== px4 log tail"
tr -d '\033' <"$OUT/px4.log" | grep -vE '^\s*$' | tail -18 | cut -c1-120
echo "== px4 errors"
grep -aiE 'error|fail|panic' "$OUT/px4.log" | tr -d '\033' | sort -u | head -15 | cut -c1-130
pkill -x px4 || true
pkill -f '^gz sim' || true
pkill -f 'gz sim' || true
pkill -x MicroXRCEAgent || true
sleep 2
echo "== left running"
pgrep -a 'px4|MicroXRCE' | cut -c1-80 || true
echo "result=$result"
exit "$result"
