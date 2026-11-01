"""Send SET_GPS_GLOBAL_ORIGIN to SITL over the loopback MAVLink port. Usage: lat lon alt_m."""

from __future__ import annotations

import sys
import time

ADDRESS = "udpout:127.0.0.1:18570"


def main() -> int:
    from pymavlink import mavutil

    lat, lon, alt = (float(v) for v in sys.argv[1:4])
    link = mavutil.mavlink_connection(ADDRESS, source_system=255, source_component=190)
    # Each accepted origin resets the estimator's global frame, so wait for it to settle and send
    # a few, not a stream.
    time.sleep(15.0)
    for _ in range(3):
        link.mav.set_gps_global_origin_send(1, int(lat * 1e7), int(lon * 1e7), int(alt * 1000))
        time.sleep(0.2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
