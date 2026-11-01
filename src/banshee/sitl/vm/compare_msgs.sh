#!/usr/bin/env bash
# Compare each px4_msgs definition with the same-named file in the locked PX4 tree (ADR-0007).
set -uo pipefail
WORK="$HOME/sitl"
same=0
different=0
for file in "$WORK"/ws/src/px4_msgs/msg/*.msg; do
  name=$(basename "$file")
  other="$WORK/PX4-Autopilot/msg/$name"
  [ -f "$other" ] || other="$WORK/PX4-Autopilot/msg/versioned/$name"
  if cmp -s "$file" "$other"; then
    same=$((same + 1))
  else
    different=$((different + 1))
    echo "differs or missing: $name"
  fi
done
echo "identical=$same different=$different"
[ "$different" -eq 0 ]
