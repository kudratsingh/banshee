"""Omni Drone — a general-purpose aerial autonomy platform built conventionally first.

Implemented in this starter: ``core`` (append-only record helpers), ``freshness`` (the
setpoint-freshness and estimator-validity gate, pure logic), ``interfaces`` (typed Protocols for the
modules the work orders will implement). SITL, offboard bridge, export, fault harness, reference
pipeline and mission executive are specified in docs/ and work_orders/ and are NOT implemented yet.
Nothing here can command an aircraft.
"""

from __future__ import annotations

__version__ = "0.0.1"
