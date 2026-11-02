"""Banshee (Omni Drone) — a general-purpose aerial autonomy platform built conventionally first.

The off-board package: contract export, analysis and SITL tooling, on Python 3.12. Record helpers
and the contract come from the ``ironclad`` package. The onboard nodes (freshness gate, command
path, offboard bridge) are ``banshee_onboard``, in ``onboard/``, on Python 3.10. ``interfaces``
holds typed Protocols for the modules the work orders implement. Nothing here commands an aircraft
outside the simulator.
"""

from __future__ import annotations

__version__ = "0.0.1"
