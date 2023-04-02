from __future__ import annotations

from pathlib import Path

import pytest
from sympy import Symbol

from epoch_cheats.deck_parse import (
    block_to_dict,
    get_deck_constants,
    get_deck_constants_sym,
    load_deck,
    load_params,
    parse_constant_block,
    parse_value,
    split_to_blocks,
)


@pytest.fixture
def default_params():
    return load_params()


@pytest.fixture
def deck_file() -> Path:
    input_path = Path("tests/test_input.deck")
    return input_path


@pytest.fixture
def deck_lines():
    return ["begin:constant", "pi = 3.14", "g = 9.81", "end:constant"]


@pytest.fixture
def deck_path():
    return {"constant": {"pi": "3.14", "g": "9.81"}}


def test_load_deck(deck_file):
    expected_output = ["begin:constant", "pi = 3.14", "g = 9.81", "end:constant"]
    assert load_deck(deck_file) == expected_output


def test_block_to_dict(deck_lines):
    expected = {"pi": "3.14", "g": "9.81"}
    assert block_to_dict(deck_lines[1:-1]) == expected


def test_split_to_blocks(deck_lines):
    expected = {"constant": {"pi": "3.14", "g": "9.81"}}
    assert split_to_blocks(deck_lines) == expected


def test_split_to_blocks_error(deck_lines):
    deck_lines = deck_lines[:-1]  # all but end:constant
    with pytest.raises(SyntaxError):
        split_to_blocks(deck_lines)


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a*b", "a*b"),
        ("a**b", "a**b"),
        ("a^b", "a**b"),
        ("a/b", "a/b"),
        ("(a+2)/b", "(a + 2)/b"),
        ("-a", "-a"),
    ],
)
def test_parse_value(expr, expected):
    assert str(parse_value(expr)) == expected


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a*b", 35.0),
        ("a**b", 275854.7353515625),
        ("a^b", 275854.7353515625),
        ("a/b", 0.35),
        ("(a+2)/b", 0.55),
        ("-a", -3.5),
    ],
)
def test_parse_constant_block(expr, expected):
    params = load_params()
    test_block = {"a": str(3.5), "b": str(10)}
    test_block["c"] = str(expr)
    res = parse_constant_block(test_block, params.constant)
    assert res[Symbol("c")] == pytest.approx(expected)


def test_parse_constant_block_chained():
    params = load_params()
    test_block = dict(a="3.5", b="10", c="a+b", d="a+c")
    expected = {
        "qe": 1.60217663e-19,
        "mu0": 1.25663706212e-06,
        "kb": 1.380649e-23,
        "pi": 3.141592653589793,
        "a": 3.5,
        "b": 10.0,
        "c": 13.5,
        "d": 17.0,
    }
    result = {
        str(k): v for k, v in parse_constant_block(test_block, params.constant).items()
    }
    assert expected.keys() == result.keys()
    for k in expected:
        assert result[k] == pytest.approx(expected[k])


def test_get_deck_constants_sym(deck_file):
    expected = {
        "qe": 1.60217663e-19,
        "mu0": 1.25663706212e-06,
        "kb": 1.380649e-23,
        "pi": 3.14,
        "g": 9.81,
    }
    expected = {Symbol(k): v for k, v in expected.items()}
    assert get_deck_constants_sym(deck_file) == expected


# test get deck constants
def test_get_deck_constants(deck_file):
    expected = {
        "qe": 1.60217663e-19,
        "mu0": 1.25663706212e-06,
        "kb": 1.380649e-23,
        "pi": 3.14,
        "g": 9.81,
    }
    assert get_deck_constants(deck_file) == expected
