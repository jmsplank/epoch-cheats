"""provides functions for parsing an input deck file.

The input deck file is used by a larger program to
set up a simulation. The conventions include the use of "begin:constant" and
"end:constant" lines to delineate a block of constants. This block of constants
is parsed and converted into a dictionary of Sympy symbols as keys and float
values as values.

The module includes functions to read the input deck file, split it into blocks based
on the "begin" and "end" lines, parse the constant block into a dictionary of Sympy
symbols and float values, and return the dictionary of constants.

The input deck file should contain a section called "constant" with lines in the
format of "name = value" or "name:value". Lines that start with a "#" are considered
comments and are ignored by the parser. Values may include mathematical expressions
that use Sympy symbols.
"""
from __future__ import annotations

from pathlib import Path
from typing import Union

from sympy import Expr, Symbol
from sympy.abc import _clash
from sympy.parsing.sympy_parser import parse_expr

from .deck import Deck
from .PARAMS import Params, default_params


def load_params(param_dict: Params = default_params) -> Params:
    """Load constants, by default from .PARAMS.params.

    Args:
        param_dict (dict[str, Any], optional): .PARAMS.params. Defaults to params.

    Returns:
        Params: NamedTuple of constants and unparseable
    """
    constant = dict(param_dict.constant)
    unparsables: list[str] = list(param_dict.unparseables)
    return Params(constant, unparsables)


def load_deck(fpath: Path) -> list[str]:
    """Read input.deck and return a list of lines with light parsing.

    - leading/trailing whitespace and newlines removed
    - comment lines (starting with #) removed
    - Comments within lines not removed

    Args:
        fpath (Path): path to input.deck

    Returns:
        list[str]: lines of input.deck, trimmed and comment lines removed.

    Example:
        Suppose we have a text file called "deck.txt" containing the following
        lines:

        # This is a comment
        Line 1
        Line 2

        To load this file, we can use the following code:

        >>> from pathlib import Path
        >>> deck_path = Path("deck.txt")
        >>> load_deck(deck_path)
        ["Line 1", "Line 2"]
    """
    with open(fpath, "r") as file:
        lines = file.readlines()
    lines = [
        line.strip()
        for line in lines
        if line.strip() != "" and not line.strip().startswith("#")
    ]
    return lines


def block_to_dict(block: list[str]) -> dict[str, str]:
    """Take a list of 'key = value' or 'key:value' strings and comvert to dict.

    Takes a list of strings as input, where each string is formatted
    as a key-value pair separated by either " = " or ":". The key and value are
    stripped of leading and trailing white space, and any comments following the
    value are removed.

    Args:
        block (list[str]): the lines within the block

    Returns:
        dict[str, str]: 'key = value' parsed to {key:value}

    Example:
        >>> block = ["key1 = value1 # comment",
        ...          "key2:value2"]
        >>> block_to_dict(block)
        {"key1": "value1", "key2": "value2"}
    """
    out = {}
    for b in block:
        b_split = b.split(" = ")
        if len(b_split) != 2:
            b_split = b.split(":")
            if len(b_split) != 2:
                continue
        key, value = [i.strip() for i in b_split]
        value = value.split("#")[0].strip()
        out[key] = value
    return out


def split_to_blocks(lines_list: list[str]) -> dict[str, dict[str, str]]:
    """Iterate over each line in deck and extract begin:name -> end:name blocks.

    'name' becomes the key of a dict and the lines between are converted to dict
    using block_to_dict()

    Args:
        lines_list (list[str]): Lines in input.deck, commonly from load_deck()

    Raises:
        SyntaxError: Raised when no end:name found for a corresponding begin:name

    Returns:
        dict[str, dict[str, str]]: deck as {'block':{'var1':val1,'var2':val2}} format

    Example:
        >>> lines_list = [
            "begin:block1",
            "key1 = value1",
            "key2 = value2",
            "end = block1",
            "begin = block2",
            "key3 = value3",
            "key4 = value4",
            "end = block2",
        ]
        >>> split_to_blocks(lines_list)
        {
            "block1": {
                "key1": "value1",
                "key2": "value2",
            },
            "block2": {
                "key3": "value3",
                "key4": "value4",
            },
        }
    """
    blocks = {}
    current_block_i = [0, 0]
    i = 0
    while i < len(lines_list):
        line = lines_list[i]

        if not line.startswith("begin:"):
            i += 1
            continue

        block_name = line.split(":")[1]
        current_block_i[0] = i
        for j in range(i, len(lines_list)):
            inner_line = lines_list[j]
            if inner_line.startswith(f"end:{block_name}"):
                current_block_i[1] = j
                break
        if current_block_i[1] > current_block_i[0]:
            block_data = lines_list[current_block_i[0] + 1 : current_block_i[1]]
            blocks[block_name] = block_to_dict(block_data)
        else:
            raise SyntaxError(f"No end:{block_name} found!")
        i = current_block_i[1] + 1

    return blocks


def parse_value(expr: str) -> Expr:
    """Use sympy parse_expr() to parse string expression.

    - Replaces ^ exponent with ** exponent

    Args:
        expr (str): the expression to be parsed

    Returns:
        Expr: A Sympy expression

    Example:
        To parse the expression "3*x**2 + 2*x + 1", we can use the following code:

        >>> parse_value("3*x^2 + 2*x + 1")
        3*x**2 + 2*x + 1
    """
    expr = expr.replace("^", "**")
    parsed: Expr = parse_expr(expr, local_dict=_clash)
    return parsed


def parse_constant_block(
    constant_block: dict[str, str], params: dict[Symbol, float]
) -> dict[Symbol, float]:
    """Parse dict of var:value where value can be transformed to expression.

    Args:
        constant_block (dict[str, str]): the Block to parse
        params (dict[Symbol, float]): the parameters to substitute in the expression

    Raises:
        ValueError: Raised when undefined symbols remain in expression
                    that can't be substituted

    Returns:
        dict[Symbol, float]: uses sympy symbols as the key and python float as value

    Example:
        Suppose we have a constant block in a deck file containing the following
        constants:

        g = 9.81
        pi = 3.14159

        To parse this block and return a dictionary of constants and their values,
        we can use the following code:

        >>> constant_block = {"g": "9.81", "pi": "3.14159"}
        >>> parse_constant_block(constant_block)
        {g: 9.81, pi: 3.14159}
    """
    var_dict = dict(params)
    for var_name, var in constant_block.items():
        parsed_var = parse_value(var)
        eval_var = parsed_var.evalf(subs=var_dict)
        try:
            eval_var = float(eval_var)
        except TypeError:
            raise ValueError(
                f"Expression {var_name} = {eval_var} cannot be converted to float!"
                " is there an undefined constant?"
            )
        var_dict[Symbol(var_name)] = eval_var

    return var_dict


def get_deck_constants_sym(deck_path: Path) -> dict[Symbol, float]:
    """Take a path to an input.deck and return the constants block as a dict.

    Args:
        deck_path (Path): pathlib path object pointing to input.deck

    Returns:
        dict[Symbol, float]: {sympy symbol:float value}

    Raises:
        IOError: If the input deck file cannot be found or opened.
        ValueError: If a constant in the input deck contains an undefined
            constant or cannot be converted to float.

    Example:
        >>> from pathlib import Path
        >>> deck_path = Path("input.deck")
        >>> constants = get_deck_constants_sym(deck_path)
        >>> print(constants)
        {
            "mp": 1.67e-27,
            "B0": 1e-08,
            "n0": 10000000.0,
            ...
        }
    """
    params = load_params()
    deck_lines = load_deck(deck_path)
    blocks = split_to_blocks(deck_lines)
    constant = parse_constant_block(blocks["constant"], params.constant)
    return constant


def get_deck_constants(deck_path: Path) -> dict[str, float]:
    """Call get_deck_constants_sym() and converts sympy key to str key.

    Args:
        deck_path (Path): path to input.deck

    Returns:
        dict[str, float]: {const: value}

    Example:
        >>> from pathlib import Path
        >>> deck_path = Path("input.deck")
        >>> constants = get_deck_constants(deck_path)
        >>> print(constants)
        {
            "mp": 1.67e-27,
            "B0": 1e-08,
            "n0": 10000000.0,
            ...
        }
    """
    constant = get_deck_constants_sym(deck_path)
    return {str(k): v for k, v in constant.items()}


BlockTypes = Union[float, str, tuple[float, float]]


def parse_block(
    block: dict[str, str],
    unparseables: list[str],
    constants: dict[Symbol, float],
) -> dict[str, BlockTypes]:
    """Parse dict of var:value.

    - if value cannot be evaluated, it is returned as a string

    TODO: add support for tuples

    Args:
        block (dict[str, str]): the Block to parse
        unparseables (list[str]): list of strings that if found in a variable
                                    will not be parsed
        constants (dict[Symbol, float]): a dictionary of default variables and their values

    Returns:
        dict[str, BlockTypes]: uses sympy symbols as the key and python float as value

    Note:
        constants is updated with new constants found in block
    """
    output: dict[str, BlockTypes] = {}
    for var_name, var in block.items():
        if any(unparseable in var for unparseable in unparseables):
            # don't try to parse this variable
            output[var_name] = var
            continue
        eval_var = parse_value(var).evalf(subs=constants)
        try:
            eval_var = float(eval_var)
            # This is a new constant so add it to constants
            constants[Symbol(var_name)] = eval_var
            output[var_name] = eval_var
        except TypeError:
            # can't convert to float
            output[var_name] = var
    return output


def evaluate_deck(deck_path: Path) -> dict[str, dict[str, BlockTypes]]:
    """Parse input.deck and return a dictionary of blocks and their variables.

    Args:
        deck_path (Path): pathlib path object pointing to input.deck

    Returns:
        dict[str, dict[str, BlockTypes]]: {block_name: {var_name: var_value}}

    Raises:
        IOError: If the input deck file cannot be found or opened.
        ValueError: If a value in the constant block contains an undefined
            constant and cannot be converted to float.

    """
    params = load_params()
    deck_lines = load_deck(deck_path)
    blocks = split_to_blocks(deck_lines)
    output: dict[str, dict[str, BlockTypes]] = {}

    # always parse constant block first
    constants = parse_constant_block(blocks["constant"], params.constant)
    output["constant"] = {str(k): v for k, v in constants.items()}
    del blocks["constant"]

    for block_name, block in blocks.items():
        output[block_name] = parse_block(block, params.unparseables, constants)

    return output


def validate_deck(deck: dict[str, dict[str, BlockTypes]]) -> Deck:
    return Deck.parse_obj(deck)
