# Shared by run_mission.sh and run_case.sh: the frozen environment, and starting and stopping the
# stack. Simulation only. Sourced with "repo", "out" and "WORK" set. Every process has a time limit,
# capped output and no stdin. Set extra PX4_PARAM_ values and the model before start_stack.
export ROS_DOMAIN_ID=42 HEADLESS=1 PX4_SIM_MODEL=gz_x500 PX4_GZ_WORLD=default
export PYTHONPATH="$repo/src:$repo/onboard/src" PYTHONDONTWRITEBYTECODE=1
# The frozen values in evals/D1-exit-tests.json px4_parameters_under_test.
export PX4_PARAM_MPC_XY_VEL_MAX=2.5 PX4_PARAM_MPC_Z_VEL_MAX_UP=1.0 PX4_PARAM_MPC_Z_VEL_MAX_DN=0.7
export PX4_PARAM_COM_OF_LOSS_T=1.0 PX4_PARAM_COM_OBL_RC_ACT=5 PX4_PARAM_NAV_RCL_ACT=2
export PX4_PARAM_GF_MAX_HOR_DIST=40 PX4_PARAM_GF_MAX_VER_DIST=14 PX4_PARAM_GF_ACTION=5 PX4_PARAM_GF_SOURCE=1
export PX4_PARAM_COM_ARM_WO_GPS=0 PX4_PARAM_RTL_RETURN_ALT=10 PX4_PARAM_COM_POS_FS_EPH=5.0
export PX4_PARAM_BAT_LOW_THR=0.4 PX4_PARAM_BAT_CRIT_THR=0.35 PX4_PARAM_BAT_EMERGEN_THR=0.15
export PX4_PARAM_RTL_DESCEND_ALT=10 PX4_PARAM_COM_LOW_BAT_ACT=3 PX4_PARAM_COM_RC_OVERRIDE=3
export PX4_PARAM_EKF2_NOAID_TOUT=1000000 PX4_PARAM_NAV_DLL_ACT=0  # Applied below; see the note.
# Only for a simulator with no RC or ground station: stick input off, and an
# offboard exception to RC loss. These are SITL settings, not values for the aircraft.
export PX4_PARAM_COM_RC_IN_MODE=4 PX4_PARAM_COM_RCL_EXCEPT=4
set +u
# shellcheck disable=SC1091
# One ROS distribution per VM: Jazzy in banshee-sitl, Humble in banshee-sitl-humble (WO-025).
ros_setup="$(ls /opt/ros/*/setup.bash | head -1)"
if [ "$(basename "$(dirname "$ros_setup")")" = humble ]; then stack_lock=config/stack-lock.humble.resolved.json; else stack_lock=config/stack-lock.resolved.json; fi
# shellcheck disable=SC1090
source "$ros_setup"
# shellcheck disable=SC1091
source "$WORK/ws/install/setup.bash"
set -u
rootfs="$WORK/PX4-Autopilot/build/px4_sitl_default/rootfs"

cleanup() {
  pkill -f banshee-sitl-watchdog || true
  pkill -f banshee.faults.rc_sim || true
  pkill -f banshee.offboard.mission || true
  pkill -x px4 || true
  pkill -f 'gz sim' || true
  pkill -x MicroXRCEAgent || true
  sleep 2
}

param() { timeout 10 ../bin/px4-param "$@" </dev/null; }

check_versions() {
  python3 -m banshee.sitl.launch --check-versions --lock "$repo/$stack_lock" >"$out/versions.json" 2>"$out/versions.err"
}

# Usage: start_stack <limit seconds>. Leaves the working directory in the PX4 rootfs.
start_stack() {
  local limit="$1"
  # Gazebo is started by PX4, outside any time limit here, and a killed caller would skip the trap.
  setsid nohup bash -c "sleep $((limit + 15)); pkill -x px4; pkill -x MicroXRCEAgent; pkill -f 'gz sim'" banshee-sitl-watchdog </dev/null >/dev/null 2>&1 &
  rm -f "$rootfs"/parameters*.bson
  timeout "$limit" MicroXRCEAgent udp4 -p 8888 </dev/null 2>&1 | head -c 5000000 >"$out/agent.log" &
  cd "$rootfs" || exit 2
  ulog_marker="$out/.started"
  touch "$ulog_marker"
  timeout "$limit" ../bin/px4 -d </dev/null 2>&1 | head -c 20000000 >"$out/px4.log" &
  # gz_x500 raises the default of NAV_DLL_ACT to 2 after the PX4_PARAM_ overrides. Setting 0 there is
  # a no-op, because 0 is then still the default, so wait for the airframe to run and set it after.
  local tries=0
  until param compare NAV_DLL_ACT 2 >/dev/null 2>&1; do
    tries=$((tries + 1))
    [ "$tries" -le 60 ] || { echo "the airframe did not run in time"; exit 4; }
    sleep 1
  done
  param set NAV_DLL_ACT 0 >/dev/null 2>&1
}

# Read back what PX4 actually holds, as the evidence for the configured values.
read_back() {
  local name
  for name in $(env | sed -n 's/^PX4_PARAM_\([^=]*\)=.*/\1/p' | sort); do
    param show "$name" 2>&1 | grep -E "^[ x+*]* *$name" | head -n 1
  done >"$out/params-readback.txt"
}

copy_ulog() {
  sleep 2
  mkdir -p "$out/ulog"
  find log -name '*.ulg' -newer "$ulog_marker" -exec cp {} "$out/ulog/" \;
  rm -f "$ulog_marker"
}
