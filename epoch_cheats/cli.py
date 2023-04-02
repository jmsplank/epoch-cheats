"""
This module provides a CLI for evaluating deck files.

It defines a CLI app using the `typer` library, with a sub-command `deck eval`
that takes a single argument as a path to a `.deck` file. The `eval` command
reads the specified `.deck` file and extracts the constants defined in the
file. It then prints the constants to the console.

This module also depends on a `deck_parse` module that provides the
`get_deck_constants` function used for parsing `.deck` files.

Example usage:
    $ epoch-cheats deck eval my_deck_file.deck
"""
from __future__ import annotations

from pathlib import Path

import typer

from .deck_parse import get_deck_constants

epoch_cheats = typer.Typer()
deck = typer.Typer()
epoch_cheats.add_typer(deck, name="deck")


@deck.command("eval")
def eval(file_path: Path) -> None:
    """
    Evaluate a deck file.

    Args:
        file_path (Path): The path to the `.deck` file to be evaluated.

    Raises:
        typer.Abort: If the specified file does not have a `.deck` extension.

    Returns:
        None: This function only prints the constants defined in the `.deck` file.
        It does not return any value.
    """
    if not file_path.suffix == ".deck":
        raise typer.Abort()

    consts = get_deck_constants(file_path)

    print("begin: constant")
    longest_name = max([len(i) for i in consts])
    for k, v in consts.items():
        k_str = f"{k:>{longest_name}}"
        v_str = f"{v: .3E}".replace("E", "e")
        print(f"  {k_str}  = {v_str}")
    print("end: constant")

    print(f"Successfully evaluated {file_path}")
