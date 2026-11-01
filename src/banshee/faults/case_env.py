"""Turn one case into the files ``run_case.sh`` sources: environment and timed VM commands."""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path
from typing import Any

from .injection import load_case


def env_lines(case: dict[str, Any]) -> list[str]:
    """``export`` lines for the case's environment, on top of the shared SITL settings."""
    env = dict(case.get("env", {}))
    if case.get("rc"):
        env.update(RC_ENV)
    return [f"export {k}={shlex.quote(str(v))}" for k, v in sorted(env.items())]


RC_ENV = {
    "PX4_PARAM_COM_RC_IN_MODE": 0,
    "PX4_PARAM_COM_RCL_EXCEPT": 0,
    "PX4_PARAM_RC_MAP_ROLL": 1,
    "PX4_PARAM_RC_MAP_PITCH": 2,
    "PX4_PARAM_RC_MAP_THROTTLE": 3,
    "PX4_PARAM_RC_MAP_YAW": 4,
    "PX4_PARAM_RC_MAP_FLTMODE": 5,
    "PX4_PARAM_RC_MAP_KILL_SW": 6,
    "PX4_PARAM_COM_FLTMODE6": 2,
    # PX4 treats RC as calibrated, and its input as valid, only with a channel count set.
    "PX4_PARAM_RC_CHAN_CNT": 8,
}


def timeline_lines(commands: list[list[Any]]) -> list[str]:
    """Shell lines that run ``[delay_s, command]`` pairs at those times after the trigger."""
    lines: list[str] = []
    clock = 0.0
    for delay, command in sorted(commands, key=lambda c: float(c[0])):
        if float(delay) > clock:
            lines.append(f"sleep {float(delay) - clock:.3f}")
            clock = float(delay)
        lines.append(str(command))
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args(argv)
    case = load_case(args.matrix, args.case)
    files = {
        "case-env.sh": env_lines(case),
        "case-after-start.sh": [str(c) for c in case.get("after_start", [])],
        "case-timeline.sh": timeline_lines(case.get("vm", [])),
    }
    for name, lines in files.items():
        (args.dir / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.dir / "case.json").write_text(json.dumps(case, indent=1) + "\n", encoding="utf-8")
    (args.dir / "case-limits.sh").write_text(
        f"CASE_TIMEOUT_S={int(case.get('timeout_s', 120))}\n"
        f"CASE_RC={'1' if case.get('rc') else '0'}\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
