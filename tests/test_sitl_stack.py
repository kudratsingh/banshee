"""The simulator stack switch: Jazzy by default, Humble on request, nothing else."""

from __future__ import annotations

from pathlib import Path

import pytest

from banshee.sitl import stack


def test_jazzy_is_the_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BANSHEE_STACK", raising=False)
    assert stack.vm_name() == "banshee-sitl"
    assert stack.resolved_lock(Path("/r")) == Path("/r/config/stack-lock.resolved.json")


def test_humble_has_its_own_vm_and_lock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BANSHEE_STACK", "humble")
    assert stack.vm_name() == "banshee-sitl-humble"
    assert stack.resolved_lock(Path("/r")).name == "stack-lock.humble.resolved.json"


def test_an_unknown_stack_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BANSHEE_STACK", "iron")
    with pytest.raises(SystemExit):
        stack.vm_name()
