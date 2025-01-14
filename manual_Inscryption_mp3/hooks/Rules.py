from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def enoughDeckSize(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """does the player have a small enough deck?"""
    deck = get_option_value(multiworld, player, "deck_size_rando") - 20
    if deck - state.count("-1 Min Deck Size", player) <= 15 - int(level):
        return True
    return False

def enoughStackSize(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """can the player use enough of one card?"""
    stack = 20 - get_option_value(multiworld, player, "stack_size_rando")
    if stack - state.count("+1 Max Card Stack Size", player) <= 15 - int(level):
        return True
    return False