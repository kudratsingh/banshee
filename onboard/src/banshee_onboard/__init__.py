"""The onboard subset: the freshness gate, the command path and the offboard bridge.

Runs on the Jetson's Python 3.10 with ROS 2 Humble, so it imports nothing from ``ironclad`` or from
the off-board ``banshee`` package (owner, 2026-11-02). Contract export and all tooling run off-board
on 3.12, from the flight logs.
"""
