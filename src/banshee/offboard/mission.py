"""Launcher for the offboard node, kept at this path so that frozen fault cases which stop the node
by its process name (``pkill -f banshee.offboard.mission``) still match it. The node is
``banshee_onboard.mission``.
"""

from __future__ import annotations

from banshee_onboard.mission import main

if __name__ == "__main__":
    raise SystemExit(main())
