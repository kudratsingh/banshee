"""Run a command with hard bounds, so that no run can fill a disk (``AGENTS.md`` section 8.8).

``run_bounded`` gives the command no stdin, its own process group, a wall-clock limit and a log
with a byte cap. The log is created once and never overwritten. Reaching the cap or the limit stops
the whole group. On 2026-10-31 an uncapped log of a repeating PX4 prompt filled the owner's disk.

``main`` also refuses to start when a checked volume, on the host or in a VM, has too little free
space. Units: bytes and seconds.
"""

from __future__ import annotations

import argparse
import contextlib
import os
import select
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

COMPLETED = "completed"
LOG_CAP = "log_cap"
TIMEOUT = "timeout"

EXIT_REFUSED = 3
EXIT_LOG_CAP = 4
EXIT_TIMEOUT = 5

_READ_SIZE = 65536
_POLL_S = 0.2
_TERM_GRACE_S = 5.0


class BoundedError(ValueError):
    """Raised when a bound is invalid or a free-space reading cannot be parsed."""


@dataclass(frozen=True)
class BoundedResult:
    """How the run ended: ``outcome``, the command's exit code if it ended itself, log bytes."""

    outcome: str
    returncode: int | None
    log_bytes: int


def _stop_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate the command's process group, then kill it after a short grace."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=_TERM_GRACE_S)
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)
    process.wait()


def run_bounded(
    command: list[str], log_path: Path, *, max_log_bytes: int, timeout_s: float
) -> BoundedResult:
    """Run ``command``, writing at most ``max_log_bytes`` to a new log at ``log_path``.

    Raises ``FileExistsError`` if the log exists, because a log is never overwritten.
    """
    if max_log_bytes <= 0 or timeout_s <= 0:
        raise BoundedError("max_log_bytes and timeout_s must be positive")
    deadline = time.monotonic() + timeout_s
    written = 0
    with log_path.open("xb") as log:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        assert process.stdout is not None
        fd = process.stdout.fileno()
        outcome = COMPLETED
        while True:
            if time.monotonic() >= deadline:
                outcome = TIMEOUT
                break
            ready, _, _ = select.select([fd], [], [], _POLL_S)
            if not ready:
                continue
            chunk = os.read(fd, _READ_SIZE)
            if not chunk:
                break
            room = max_log_bytes - written
            log.write(chunk[:room])
            log.flush()
            written += min(len(chunk), room)
            if len(chunk) > room or written >= max_log_bytes:
                outcome = LOG_CAP
                break
        if outcome == COMPLETED:
            remaining = max(deadline - time.monotonic(), 0.1)
            try:
                process.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                outcome = TIMEOUT
        if outcome != COMPLETED:
            _stop_group(process)
        process.stdout.close()
    return BoundedResult(
        outcome=outcome,
        returncode=process.returncode if outcome == COMPLETED else None,
        log_bytes=written,
    )


def parse_df_free_bytes(df_output: str) -> int:
    """Free bytes from the last line of ``df -Pk`` output; raises ``BoundedError`` if unreadable."""
    lines = [line for line in df_output.strip().splitlines() if line.strip()]
    if len(lines) < 2:
        raise BoundedError(f"unexpected df output: {df_output!r}")
    fields = lines[-1].split()
    try:
        return int(fields[3]) * 1024
    except (IndexError, ValueError) as exc:
        raise BoundedError(f"unexpected df output: {df_output!r}") from exc


def vm_df_command(vm: str) -> list[str]:
    """``df`` of the VM's own root disk. Not ``.``: Lima starts in the host's working directory, so
    ``.`` can be a mount of the Mac's disk, which is the wrong volume to check."""
    return ["limactl", "shell", vm, "--", "df", "-Pk", "/"]


def vm_free_bytes(vm: str) -> int:
    """Free bytes on the root disk of a Lima VM."""
    out = subprocess.run(
        vm_df_command(vm),
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
        stdin=subprocess.DEVNULL,
    )
    return parse_df_free_bytes(out.stdout)


def free_space_problems(free_by_volume: dict[str, int], min_free_bytes: int) -> list[str]:
    """One message per volume with less than ``min_free_bytes`` free."""
    return [
        f"{name}: {free} bytes free, below the required {min_free_bytes}"
        for name, free in free_by_volume.items()
        if free < min_free_bytes
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--max-log-bytes", type=int, default=200_000_000)
    parser.add_argument("--timeout-s", type=float, default=3 * 3600.0)
    parser.add_argument("--min-free-bytes", type=int, default=20_000_000_000)
    parser.add_argument("--vm", help="also check free space inside this Lima VM")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("no command given")
    free = {f"host {args.log.parent}": shutil.disk_usage(args.log.parent).free}
    if args.vm:
        free[f"VM {args.vm}"] = vm_free_bytes(args.vm)
    problems = free_space_problems(free, args.min_free_bytes)
    if problems:
        for problem in problems:
            print(f"refused: {problem}", file=sys.stderr)
        return EXIT_REFUSED
    result = run_bounded(
        command, args.log, max_log_bytes=args.max_log_bytes, timeout_s=args.timeout_s
    )
    print(f"{result.outcome}: {result.log_bytes} bytes logged to {args.log}")
    if result.outcome == LOG_CAP:
        return EXIT_LOG_CAP
    if result.outcome == TIMEOUT:
        return EXIT_TIMEOUT
    return result.returncode if result.returncode is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
