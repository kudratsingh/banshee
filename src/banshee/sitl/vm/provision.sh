#!/usr/bin/env bash
# Install the pinned flight stack inside the SITL VM, from config/stack-lock.proposed.json.
# Usage, inside the VM: bash provision.sh <repository path>. Simulation only: no hardware.
set -euo pipefail
repo="$1"
lock="$repo/config/stack-lock.proposed.json"
pin() { python3 -c "import json,sys; print(json.load(open('$lock'))['flight_stack'][sys.argv[1]][sys.argv[2]])" "$1" "$2"; }
PX4_COMMIT="$(pin px4_release_or_commit commit)"
AGENT_COMMIT="$(pin px4_ros2_bridge_commit agent_commit)"
MSGS_COMMIT="$(pin px4_ros2_bridge_commit px4_msgs_commit)"
DISTRO="$(pin ros2_distribution value)"
WORK="$HOME/sitl"
mkdir -p "$WORK"

echo "== base packages"
export DEBIAN_FRONTEND=noninteractive
sudo -E apt-get update -qq
sudo -E apt-get install -y -qq git curl cmake build-essential python3-pip ca-certificates lsb-release

echo "== ROS 2 $DISTRO"
sudo curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list >/dev/null
sudo -E apt-get update -qq
sudo -E apt-get install -y -qq "ros-$DISTRO-ros-base" ros-dev-tools

echo "== PX4 at $PX4_COMMIT"
if [ ! -d "$WORK/PX4-Autopilot/.git" ]; then
  git clone --quiet https://github.com/PX4/PX4-Autopilot.git "$WORK/PX4-Autopilot"
fi
cd "$WORK/PX4-Autopilot"
git fetch --quiet --tags origin
git checkout --quiet "$PX4_COMMIT"
# Simulators this project does not use are skipped: their model repositories are large and are not
# needed for Gazebo SITL. Clones retry, because a single dropped connection otherwise ends the run.
for skip in Tools/simulation/flightgear/flightgear_bridge Tools/simulation/jsbsim/jsbsim_bridge \
  Tools/simulation/gazebo-classic/sitl_gazebo-classic Tools/simulation/jmavsim/jMAVSim; do
  git config "submodule.$skip.update" none
done
for attempt in 1 2 3 4 5; do
  if git submodule update --init --recursive --quiet --depth 1; then break; fi
  if [ "$attempt" = 5 ]; then echo "submodules failed after 5 attempts"; exit 1; fi
  sleep 30
done
test "$(git rev-parse HEAD)" = "$PX4_COMMIT"
bash ./Tools/setup/ubuntu.sh --no-nuttx
export PATH="$HOME/.local/bin:$PATH"

echo "== build SITL"
# Build only. "make px4_sitl gz_x500" starts PX4, even with DONT_RUN set, and with no terminal its
# prompt repeats without end: that filled the disk and likely crashed the host on 2026-10-31.
make px4_sitl_default </dev/null

echo "== Micro-XRCE-DDS-Agent at $AGENT_COMMIT"
if [ ! -d "$WORK/Micro-XRCE-DDS-Agent/.git" ]; then
  git clone --quiet https://github.com/eProsima/Micro-XRCE-DDS-Agent.git "$WORK/Micro-XRCE-DDS-Agent"
fi
cd "$WORK/Micro-XRCE-DDS-Agent"
git fetch --quiet --tags origin
git checkout --quiet "$AGENT_COMMIT"
test "$(git rev-parse HEAD)" = "$AGENT_COMMIT"
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release >/dev/null
cmake --build build -j"$(nproc)"
sudo cmake --install build >/dev/null
sudo ldconfig

echo "== px4_msgs at $MSGS_COMMIT"
mkdir -p "$WORK/ws/src"
if [ ! -d "$WORK/ws/src/px4_msgs/.git" ]; then
  git clone --quiet https://github.com/PX4/px4_msgs.git "$WORK/ws/src/px4_msgs"
fi
cd "$WORK/ws/src/px4_msgs"
git fetch --quiet --tags origin
git checkout --quiet "$MSGS_COMMIT"
test "$(git rev-parse HEAD)" = "$MSGS_COMMIT"
cd "$WORK/ws"
set +u
# shellcheck disable=SC1090
source "/opt/ros/$DISTRO/setup.bash"
set -u
colcon build --packages-select px4_msgs --event-handlers console_direct-

echo "== versions"
lsb_release -ds
dpkg-query -W -f='${Package} ${Version}\n' "ros-$DISTRO-ros-base" gz-harmonic 2>/dev/null || true
git -C "$WORK/PX4-Autopilot" rev-parse HEAD
git -C "$WORK/Micro-XRCE-DDS-Agent" rev-parse HEAD
git -C "$WORK/ws/src/px4_msgs" rev-parse HEAD
echo "provision complete"
