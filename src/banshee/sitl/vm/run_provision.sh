#!/usr/bin/env bash
# Run provision.sh in the VM with hard bounds (AGENTS.md 8.8): no stdin, a 3-hour limit, and output cut
# off at 200 MB, which also ends the run. Usage: run_provision.sh <log file on the host>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../.." && pwd)"
limactl shell banshee-sitl -- bash -c \
  "timeout 3h bash '$here/provision.sh' '$repo' </dev/null 2>&1 | head -c 209715200" >"$1"
