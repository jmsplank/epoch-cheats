"""Constant Parameters."""
from typing import NamedTuple

from sympy import Symbol


class Params(NamedTuple):
    """NamedTuple of constants and unparseable lines.

    - Used by load_params() to check .PARAMS.params for valid values

    Attributes:
        constant (dict[Symbol, float]): dictionary of constant values
        unparseable (list[str]): list of lines that could not be parsed
    """

    constant: dict[Symbol, float]
    unparseables: list[str]


default_params = Params(
    constant={
        Symbol("qe"): 1.60217663e-19,
        Symbol("mu0"): 1.25663706212e-6,
        Symbol("kb"): 1.380649e-23,
        Symbol("pi"): 3.141592653589793,
    },
    unparseables=[
        "always",
        "never",
        "species",
        "Protons",
        "shock",
        "periodic",
        "F",
        "T",
        ",",
    ],
)
