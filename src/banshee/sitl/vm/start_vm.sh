#!/usr/bin/env bash
# Create and start the SITL VM, mounting only this repository, read-only.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../.." && pwd)"
vm="${BANSHEE_VM:-banshee-sitl}"
yaml="${BANSHEE_VM_YAML:-banshee-sitl.yaml}"
limactl start --tty=false --name="$vm" \
  --set ".mounts=[{\"location\":\"$repo\",\"writable\":false}]" \
  "$here/$yaml"
