#!/usr/bin/env bash
# Create and start the SITL VM, mounting only this repository, read-only.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../.." && pwd)"
limactl start --tty=false --name=banshee-sitl \
  --set ".mounts=[{\"location\":\"$repo\",\"writable\":false}]" \
  "$here/banshee-sitl.yaml"
