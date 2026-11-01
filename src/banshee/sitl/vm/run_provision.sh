#!/usr/bin/env bash
# Run provision.sh in the VM with hard bounds (AGENTS.md 8.8), set by the owner after the disk filled
# on 2026-10-31. Usage: run_provision.sh <new log file on the host>
#   - refuses to start with under 20 GB free on the host or in the VM (banshee.sitl.bounded)
#   - the log is new, capped at 200 MB on the host, and reaching the cap stops the run
#   - a 3-hour limit, and no stdin
# The same cap and limit also run inside the VM, because stopping limactl here need not stop the VM's
# processes. provision.sh only builds; it never starts PX4.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../.." && pwd)"
PYTHONPATH="$repo/src" exec python3 -m banshee.sitl.bounded \
  --log "$1" --max-log-bytes 200000000 --timeout-s 10800 --min-free-bytes 20000000000 \
  --vm banshee-sitl -- \
  limactl shell banshee-sitl -- bash -c \
  "timeout 3h bash '$here/provision.sh' '$repo' </dev/null 2>&1 | head -c 200000000"
