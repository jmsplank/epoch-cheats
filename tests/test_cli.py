"""Tests for epoch_cheats/cli.py
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from epoch_cheats.deck_parse import get_deck_constants


@pytest.fixture
def deck_file():
    # Create a temporary deck file for testing
    yield Path("tests/test_input.deck")


def test_eval_command_success(deck_file):
    # Test that eval command works when given a valid .deck file
    result = subprocess.run(
        ["epoch-cheats", "deck", "eval", str(deck_file)],
        capture_output=True,
        text=True,
    )

    # Check that constants were printed correctly
    assert "   pi  =  3.140e+00" in result.stdout
    assert "    g  =  9.810e+00" in result.stdout

    # Check that success message was printed
    assert f"Successfully evaluated {deck_file}" in result.stdout


def test_eval_command_invalid_extension():
    # Test that eval command fails when given a file with invalid extension
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"begin:constant\n    pi = 3.14\n    g = 9.81\nend:constant")
        f.flush()
        invalid_file_path = Path(f.name)
    os.unlink(f.name)

    result = subprocess.run(
        ["epoch-cheats", "deck", "eval", str(invalid_file_path)],
        capture_output=True,
        text=True,
    )

    # Check that the CLI returns an error message
    assert "Aborted!" in result.stderr


def test_get_deck_constants(deck_file):
    # Test that the get_deck_constants function works as expected
    expected = dict(
        pi=3.140e00,
        g=9.810e00,
    )
    test = get_deck_constants(deck_file)
    for k, v in expected.items():
        assert pytest.approx(v) == test[k]
