"""Fault cases for the bounded runner: a runaway process must not be able to fill a disk."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from banshee.sitl.bounded import (
    COMPLETED,
    EXIT_LOG_CAP,
    EXIT_REFUSED,
    LOG_CAP,
    TIMEOUT,
    BoundedError,
    free_space_problems,
    main,
    parse_df_free_bytes,
    run_bounded,
)

CAP = 1_000_000


def _alive(pid: int) -> bool:
    """True if the process exists and is not a zombie."""
    out = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
    return out.returncode == 0 and not out.stdout.strip().startswith("Z")


@pytest.mark.parametrize(
    "script",
    [
        pytest.param("while True:\n    print('x' * 200, flush=True)", id="chatty"),
        pytest.param(
            "import sys\nwhile True:\n    sys.stdin.read()\n    print('pxh> ', end='', flush=True)",
            id="prompt-with-no-terminal",
        ),
    ],
)
def test_chatty_process_is_stopped_at_the_cap(tmp_path: Path, script: str) -> None:
    log = tmp_path / "run.log"
    started = time.monotonic()
    result = run_bounded([sys.executable, "-c", script], log, max_log_bytes=CAP, timeout_s=60)
    assert result.outcome == LOG_CAP
    assert result.returncode is None
    assert result.log_bytes == CAP
    assert log.stat().st_size == CAP
    assert time.monotonic() - started < 30


def test_children_of_a_chatty_process_are_stopped_too(tmp_path: Path) -> None:
    pid_file = tmp_path / "child.pid"
    script = (
        "import subprocess, sys\n"
        "child = subprocess.Popen([sys.executable, '-c', "
        "\"while True:\\n    print('y' * 200, flush=True)\"])\n"
        f"open({str(pid_file)!r}, 'w').write(str(child.pid))\n"
        "child.wait()\n"
    )
    result = run_bounded(
        [sys.executable, "-c", script], tmp_path / "run.log", max_log_bytes=CAP, timeout_s=60
    )
    assert result.outcome == LOG_CAP
    child = int(pid_file.read_text())
    deadline = time.monotonic() + 10
    while _alive(child) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _alive(child)


def test_silent_process_is_stopped_at_the_time_limit(tmp_path: Path) -> None:
    result = run_bounded(
        [sys.executable, "-c", "import time; time.sleep(600)"],
        tmp_path / "run.log",
        max_log_bytes=CAP,
        timeout_s=0.5,
    )
    assert result.outcome == TIMEOUT
    assert result.returncode is None


def test_command_gets_no_stdin(tmp_path: Path) -> None:
    log = tmp_path / "run.log"
    result = run_bounded(
        [sys.executable, "-c", "import sys; print(repr(sys.stdin.read()))"],
        log,
        max_log_bytes=CAP,
        timeout_s=30,
    )
    assert result.outcome == COMPLETED
    assert log.read_text().strip() == "''"


def test_normal_command_keeps_its_exit_code_and_output(tmp_path: Path) -> None:
    log = tmp_path / "run.log"
    result = run_bounded(
        [sys.executable, "-c", "print('done'); raise SystemExit(7)"],
        log,
        max_log_bytes=CAP,
        timeout_s=30,
    )
    assert result == type(result)(COMPLETED, 7, len("done" + os.linesep))
    assert log.read_text().strip() == "done"


def test_existing_log_is_never_overwritten(tmp_path: Path) -> None:
    log = tmp_path / "run.log"
    log.write_text("kept")
    with pytest.raises(FileExistsError):
        run_bounded([sys.executable, "-c", "pass"], log, max_log_bytes=CAP, timeout_s=30)
    assert log.read_text() == "kept"


@pytest.mark.parametrize(("cap", "limit"), [(0, 1.0), (1, 0.0)])
def test_bounds_must_be_positive(tmp_path: Path, cap: int, limit: float) -> None:
    with pytest.raises(BoundedError):
        run_bounded(["true"], tmp_path / "run.log", max_log_bytes=cap, timeout_s=limit)


def test_free_space_is_refused_on_any_volume_below_the_minimum() -> None:
    minimum = 20_000_000_000
    assert free_space_problems({"host": minimum, "VM": minimum}, minimum) == []
    problems = free_space_problems({"host": minimum, "VM": minimum - 1}, minimum)
    assert len(problems) == 1 and problems[0].startswith("VM")


def test_cli_refuses_to_start_below_the_minimum(tmp_path: Path) -> None:
    marker = tmp_path / "started"
    code = main(
        [
            "--log",
            str(tmp_path / "run.log"),
            "--min-free-bytes",
            str(10**18),
            "--",
            sys.executable,
            "-c",
            f"open({str(marker)!r}, 'w')",
        ]
    )
    assert code == EXIT_REFUSED
    assert not marker.exists()
    assert not (tmp_path / "run.log").exists()


def test_cli_reports_the_cap(tmp_path: Path) -> None:
    code = main(
        [
            "--log",
            str(tmp_path / "run.log"),
            "--max-log-bytes",
            str(CAP),
            "--min-free-bytes",
            "1",
            "--",
            sys.executable,
            "-c",
            "while True:\n    print('x' * 200, flush=True)",
        ]
    )
    assert code == EXIT_LOG_CAP


def test_df_output_is_parsed() -> None:
    text = "Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/vda1 100 40 60 40% /\n"
    assert parse_df_free_bytes(text) == 60 * 1024
    with pytest.raises(BoundedError):
        parse_df_free_bytes("nonsense")
