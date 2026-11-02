"""The onboard package imports nothing from ironclad or the off-board banshee package."""

from __future__ import annotations

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src" / "banshee_onboard"
BANNED = ("ironclad", "banshee")
# Standard-library modules added after Python 3.10.
NEWER_STDLIB = ("tomllib", "wsgiref.types")


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 10))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module)
    return names


def test_no_onboard_module_imports_ironclad_or_banshee() -> None:
    found = [
        (path.name, name)
        for path in sorted(SOURCE.glob("*.py"))
        for name in _imports(path)
        if name.split(".")[0] in BANNED
    ]
    assert found == []


def test_no_onboard_module_needs_a_newer_standard_library() -> None:
    found = [
        (path.name, name)
        for path in sorted(SOURCE.glob("*.py"))
        for name in _imports(path)
        if name in NEWER_STDLIB
    ]
    assert found == []
