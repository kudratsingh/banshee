#!/usr/bin/env bash
# Compile check of the chosen flight controller target at the locked PX4 commit, inside the VM.
# Compile only: this never uploads firmware or connects to hardware. Bounded by the caller.
set -euo pipefail
TARGET="px4_fmu-v6x_default"
PX4="$HOME/sitl/PX4-Autopilot"
sudo -n DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib </dev/null >/dev/null
echo "toolchain: $(arm-none-eabi-gcc --version | head -n 1)"
echo "commit: $(git -C "$PX4" rev-parse HEAD)"
rm -rf "$PX4/build/$TARGET"  # A failed configure left only this folder; the build is this script's own.
make -C "$PX4" "$TARGET" </dev/null
ls -l "$PX4/build/$TARGET/"*.px4
sha256sum "$PX4/build/$TARGET/"*.px4
echo "compile check complete"
