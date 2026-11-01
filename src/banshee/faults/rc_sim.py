"""Simulated manual control inside the VM: RC_CHANNELS_OVERRIDE over the PX4 MAVLink port.

This reaches PX4 as ``input_rc``, so the real RC path runs: mode switch, kill switch, sticks and RC
loss. Channels are PWM. Events are timed from the trigger. It stops sending at a ``stop`` event,
which is the RC loss, or at its time limit. Simulation only: it refuses any address not on loopback.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

CENTER = [1500, 1500, 1500, 1500, 1000, 1000, 1000, 1000]
ADDRESS = "udpout:127.0.0.1:18570"


def channels_at(
    base: list[int], events: list[dict[str, Any]], t_s: float | None
) -> list[int] | None:
    """The channels at ``t_s`` after the trigger, or None once a stop event has passed."""
    now = list(base)
    if t_s is None:
        return now
    for event in sorted(events, key=lambda e: float(e["t_s"])):
        if float(event["t_s"]) > t_s:
            break
        if event.get("stop"):
            return None
        for channel, value in event.get("set", {}).items():
            now[int(channel) - 1] = int(value)
    return now


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--limit-s", type=float, required=True)
    args = parser.parse_args()
    from pymavlink import mavutil

    case = json.loads((args.dir / "case.json").read_text(encoding="utf-8"))
    events = case.get("rc_events", [])
    link = mavutil.mavlink_connection(ADDRESS, source_system=255, source_component=190)
    start = time.monotonic()
    trigger_seen: float | None = None
    last_heartbeat = 0.0
    while time.monotonic() - start < args.limit_s:
        now = time.monotonic()
        if trigger_seen is None and (args.dir / "trigger.json").exists():
            trigger_seen = now
        since = None if trigger_seen is None else now - trigger_seen
        channels = channels_at(CENTER, events, since)
        if channels is None:
            print(f"rc stopped at {since}")
            return 0
        link.mav.rc_channels_override_send(1, 1, *channels)
        if now - last_heartbeat >= 1.0:
            link.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0
            )
            last_heartbeat = now
        time.sleep(0.05)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
