"""Constant Parameters."""
type_params = dict[str, dict[str, float | int] | list[str]]
default_params: type_params = {
    "constant": {
        "qe": 1.60217663e-19,
        "mu0": 1.25663706212e-6,
        "kb": 1.380649e-23,
        "pi": 3.141592653589793,
    },
    "unparseable": [
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
}
