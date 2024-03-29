"""Initialise epoch_cheats and import the main functions."""

from .cli import epoch_cheats as epoch_cheats
from .deck_parse import evaluate_deck as evaluate_deck  # <- This is the main function
from .deck_parse import get_deck_constants as get_deck_constants
from .deck_parse import validate_deck as validate_deck
