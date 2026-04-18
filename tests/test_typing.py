"""Tests for PEP 561 py.typed marker and package typing support."""

import pathlib

import src


def test_py_typed_marker_exists():
    """src/py.typed exists — signals PEP 561 compliance to type checkers."""
    package_dir = pathlib.Path(src.__file__).parent
    marker = package_dir / "py.typed"
    assert marker.exists(), "py.typed marker file is missing from the src package"


def test_py_typed_marker_is_empty():
    """py.typed must be a zero-byte file per PEP 561."""
    package_dir = pathlib.Path(src.__file__).parent
    marker = package_dir / "py.typed"
    assert marker.exists(), "py.typed marker file is missing from the src package"
    assert marker.stat().st_size == 0, "py.typed must be empty (zero bytes)"


def test_pyproject_includes_typed_classifier():
    """pyproject.toml declares the 'Typing :: Typed' classifier."""
    repo_root = pathlib.Path(src.__file__).parent.parent
    pyproject = repo_root / "pyproject.toml"
    assert pyproject.exists(), "pyproject.toml not found"
    content = pyproject.read_text()
    assert (
        "Typing :: Typed" in content
    ), "pyproject.toml is missing the 'Typing :: Typed' classifier"
