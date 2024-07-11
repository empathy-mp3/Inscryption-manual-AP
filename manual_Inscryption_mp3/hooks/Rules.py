from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def enoughDeckSize(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """does the player have a small enough deck?"""
    deck = get_option_value(multiworld, player, "Deck_Size_Rando")
    if deck - state.count("-1 Min Deck Size", player) <= 15 - int(level):
        return True
    return False

def enoughStackSize(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """can the player use enough of one card?"""
    stack = get_option_value(multiworld, player, "Stack_Size_Rando")
    if stack - state.count("+1 Max Card Stack Size", player) <= 15 - int(level):
        return True
    return False

def test(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """test"""
    return "(|Squirrel| or |Skeleton|) and ({ItemValue(act_2_offense_blood:2)} or ({ItemValue(act_2_offense_blood:1)} and {ItemValue(act_2_defense_blood:2)}) or ({ItemValue(act_2_offense_blood:1)} and {ItemValue(act_2_utility_blood:1)}))"

def act_two_blood_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """blood component for act_two_power (supports 1-8)"""
    if int(level) == 1:
        return "(|Squirrel| or |Skeleton| or {act_two_energy_power(3)}) and ({ItemValue(act_2_offense_blood:2)} or ({ItemValue(act_2_offense_blood:1)} and {ItemValue(act_2_defense_blood:2)}) or ({ItemValue(act_2_offense_blood:1)} and {ItemValue(act_2_utility_blood:1)}))"
    elif int(level) == 2:
        return "(|Squirrel| or |Skeleton| or {act_two_energy_power(4)}) and ({ItemValue(act_2_offense_blood:3)} or ({ItemValue(act_2_offense_blood:2)} and {ItemValue(act_2_defense_blood:3)}) or ({ItemValue(act_2_offense_blood:2)} and {ItemValue(act_2_utility_blood:2)}))"
    elif int(level) == 3:
        return "(|Squirrel| or |Skeleton| or {act_two_energy_power(5)}) and ({ItemValue(act_2_offense_blood:4)} or ({ItemValue(act_2_offense_blood:3)} and {ItemValue(act_2_defense_blood:4)}) or ({ItemValue(act_2_offense_blood:3)} and {ItemValue(act_2_utility_blood:2)}))"
    elif int(level) == 4:
        return "(|Squirrel| or |Skeleton| or {act_two_energy_power(6)}) and ({ItemValue(act_2_offense_blood:5)} or ({ItemValue(act_2_offense_blood:4)} and {ItemValue(act_2_defense_blood:5)}) or ({ItemValue(act_2_offense_blood:4)} and {ItemValue(act_2_utility_blood:3)}) or ({ItemValue(act_2_offense_blood:3)} and {ItemValue(act_2_utility_blood:2)} and {ItemValue(act_2_defense_blood:4)}))"
    elif int(level) == 5:
        return "(|Squirrel| or |Skeleton| or |Bone Heap| or |Tomb Robber| or |L33pb0t| or |M3atB0t|) and ({ItemValue(act_2_offense_blood:6)} or ({ItemValue(act_2_offense_blood:5)} and {ItemValue(act_2_defense_blood:6)}) or ({ItemValue(act_2_offense_blood:5)} and {ItemValue(act_2_utility_blood:4)}) or ({ItemValue(act_2_offense_blood:4)} and {ItemValue(act_2_utility_blood:3)} and {ItemValue(act_2_defense_blood:5)}))"
    elif int(level) == 6:
        return "(|Squirrel| or |Skeleton| or |Bone Heap| or |Tomb Robber| or |L33pb0t| or |M3atB0t|) and ({ItemValue(act_2_offense_blood:7)} or ({ItemValue(act_2_offense_blood:6)} and {ItemValue(act_2_defense_blood:7)}) or ({ItemValue(act_2_offense_blood:6)} and {ItemValue(act_2_utility_blood:4)}) or ({ItemValue(act_2_offense_blood:5)} and {ItemValue(act_2_utility_blood:3)} and {ItemValue(act_2_defense_blood:6)}))"
    elif int(level) == 7:
        return "((|Squirrel| and (|Warren| or |Cat|)) or (|Skeleton| and |Tomb Robber|) or (|L33pb0t| and |M3atB0t|)) and ({ItemValue(act_2_offense_blood:8)} or ({ItemValue(act_2_offense_blood:7)} and {ItemValue(act_2_defense_blood:8)}) or ({ItemValue(act_2_offense_blood:7)} and {ItemValue(act_2_utility_blood:4)}) or ({ItemValue(act_2_offense_blood:6)} and {ItemValue(act_2_utility_blood:3)} and {ItemValue(act_2_defense_blood:7)}))"
    elif int(level) == 8:
        return "((|Squirrel| and (|Warren| or |Cat|)) or (|Skeleton| and |Tomb Robber|)) and ({ItemValue(act_2_offense_blood:9)} or ({ItemValue(act_2_offense_blood:8)} and {ItemValue(act_2_defense_blood:8)}) or ({ItemValue(act_2_offense_blood:6)} and {ItemValue(act_2_utility_blood:4)}) or ({ItemValue(act_2_offense_blood:6)} and {ItemValue(act_2_utility_blood:3)} and {ItemValue(act_2_defense_blood:7)}))"
    return ""

def act_two_bone_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """bone component for act_two_power (supports 1-8)"""
    if int(level) == 1:
        return "(|Squirrel| or |Skeleton|) and ({ItemValue(act_2_offense_bones:2)} or ({ItemValue(act_2_offense_bones:1)} and {ItemValue(act_2_defense_bones:1)}) or ({ItemValue(act_2_offense_bones:1)} and {ItemValue(act_2_utility_bones:1)}))"
    elif int(level) == 2:
        return "(|Squirrel| or |Skeleton|) and ({ItemValue(act_2_offense_bones:3)} or ({ItemValue(act_2_offense_bones:2)} and {ItemValue(act_2_defense_bones:2)}) or ({ItemValue(act_2_offense_bones:2)} and {ItemValue(act_2_utility_bones:2)}))"
    elif int(level) == 3:
        return "((|Squirrel| and {act_two_blood_power(2)}) or |Skeleton| or {act_two_energy_power(3)}) and ({ItemValue(act_2_offense_bones:4)} or ({ItemValue(act_2_offense_bones:3)} and {ItemValue(act_2_defense_bones:3)}) or ({ItemValue(act_2_offense_bones:3)} and {ItemValue(act_2_utility_bones:2)}))"
    elif int(level) == 4:
        return "((|Squirrel| and {act_two_blood_power(2)}) or |Skeleton| or {act_two_energy_power(3)}) and ({ItemValue(act_2_offense_bones:5)} or ({ItemValue(act_2_offense_bones:4)} and {ItemValue(act_2_defense_bones:4)}) or ({ItemValue(act_2_offense_bones:4)} and {ItemValue(act_2_utility_bones:3)}) or ({ItemValue(act_2_offense_bones:3)} and {ItemValue(act_2_utility_bones:2)} and {ItemValue(act_2_defense_bones:3)}))"
    elif int(level) == 5:
        return "((|Squirrel| and {act_two_blood_power(3)}) or |Skeleton| or {act_two_energy_power(4)}) and ({ItemValue(act_2_offense_bones:6)} or ({ItemValue(act_2_offense_bones:5)} and {ItemValue(act_2_defense_bones:4)}) or ({ItemValue(act_2_offense_bones:5)} and {ItemValue(act_2_utility_bones:4)}) or ({ItemValue(act_2_offense_bones:4)} and {ItemValue(act_2_utility_bones:3)} and {ItemValue(act_2_defense_bones:3)}))"
    elif int(level) == 6:
        return "((|Squirrel| and {act_two_blood_power(3)}) or |Skeleton| or {act_two_energy_power(4)}) and ({ItemValue(act_2_offense_bones:7)} or ({ItemValue(act_2_offense_bones:6)} and {ItemValue(act_2_defense_bones:5)}) or ({ItemValue(act_2_offense_bones:6)} and {ItemValue(act_2_utility_bones:4)}) or ({ItemValue(act_2_offense_bones:5)} and {ItemValue(act_2_utility_bones:3)} and {ItemValue(act_2_defense_bones:4)}))"
    elif int(level) == 7:
        return "((|Squirrel| and {act_two_blood_power(4)}) or |Skeleton| or {act_two_energy_power(5)}) and ({ItemValue(act_2_offense_bones:8)} or ({ItemValue(act_2_offense_bones:7)} and {ItemValue(act_2_defense_bones:5)}) or ({ItemValue(act_2_offense_bones:7)} and {ItemValue(act_2_utility_bones:4)}) or ({ItemValue(act_2_offense_bones:6)} and {ItemValue(act_2_utility_bones:3)} and {ItemValue(act_2_defense_bones:4)}))"
    elif int(level) == 8:
        return "((|Squirrel| and {act_two_blood_power(4)}) or |Skeleton| or {act_two_energy_power(5)}) and ({ItemValue(act_2_offense_bones:9)} or ({ItemValue(act_2_offense_bones:8)} and {ItemValue(act_2_defense_bones:5)}) or ({ItemValue(act_2_offense_bones:6)} and {ItemValue(act_2_utility_bones:4)}) or ({ItemValue(act_2_offense_bones:6)} and {ItemValue(act_2_utility_bones:3)} and {ItemValue(act_2_defense_bones:4)}))"
    return ""

def act_two_energy_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """energy component for act_two_power (supports 1-8)"""
    if int(level) == 1:
        return "{ItemValue(act_2_offense_energy:2)} or ({ItemValue(act_2_offense_energy:1)} and {ItemValue(act_2_defense_energy:2)}) or ({ItemValue(act_2_offense_energy:1)} and {ItemValue(act_2_utility_energy:2)}) or ({ItemValue(act_2_offense_high_energy:2)} and {ItemValue(act_2_defense_energy:2)}) or ({ItemValue(act_2_offense_high_energy:2)} and {ItemValue(act_2_utility_energy:2)})"
    if int(level) == 2:
        return "{ItemValue(act_2_offense_energy:3)} or ({ItemValue(act_2_offense_energy:2)} and {ItemValue(act_2_defense_energy:3)}) or ({ItemValue(act_2_offense_energy:2)} and {ItemValue(act_2_utility_energy:3)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_defense_energy:3)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_utility_energy:3)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_defense_energy:3)} and {ItemValue(act_2_utility_high_energy:2)}) or ({ItemValue(act_2_offense_high_energy:2)} and {ItemValue(act_2_utility_energy:2)} and {ItemValue(act_2_defense_high_energy:3)})"
    if int(level) == 3:
        return "{ItemValue(act_2_offense_energy:4)} or ({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_defense_energy:4)}) or ({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_utility_energy:3)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:3)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_utility_energy:3)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:3)} and {ItemValue(act_2_utility_high_energy:2)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_utility_energy:2)} and {ItemValue(act_2_defense_high_energy:3)})"
    if int(level) == 4:
        return "{ItemValue(act_2_offense_energy:4)} or ({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_defense_energy:5)}) or ({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:4)} and {ItemValue(act_2_utility_high_energy:3)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_utility_energy:3)} and {ItemValue(act_2_defense_high_energy:4)})"
    if int(level) == 5:
        return "({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_defense_energy:5)}) or ({ItemValue(act_2_offense_energy:3)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:4)} and {ItemValue(act_2_defense_energy:4)} and {ItemValue(act_2_utility_high_energy:3)}) or ({ItemValue(act_2_offense_high_energy:3)} and {ItemValue(act_2_utility_energy:3)} and {ItemValue(act_2_defense_high_energy:4)})"
    if int(level) == 6:
        return "({ItemValue(act_2_offense_energy:4)} and {ItemValue(act_2_defense_energy:5)}) or ({ItemValue(act_2_offense_energy:4)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_defense_energy:4)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_defense_energy:4)} and {ItemValue(act_2_utility_high_energy:3)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_utility_energy:3)} and {ItemValue(act_2_defense_high_energy:4)})"
    if int(level) == 7:
        return "({ItemValue(act_2_offense_energy:4)} and {ItemValue(act_2_defense_energy:7)}) or ({ItemValue(act_2_offense_energy:4)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_defense_energy:6)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_defense_energy:6)} and {ItemValue(act_2_utility_high_energy:3)}) or ({ItemValue(act_2_offense_high_energy:5)} and {ItemValue(act_2_utility_energy:3)} and {ItemValue(act_2_defense_high_energy:6)})"
    if int(level) == 8:
        return "({ItemValue(act_2_offense_energy:5)} and {ItemValue(act_2_defense_energy:7)}) or ({ItemValue(act_2_offense_energy:5)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:6)} and {ItemValue(act_2_defense_energy:6)}) or ({ItemValue(act_2_offense_high_energy:6)} and {ItemValue(act_2_utility_energy:4)}) or ({ItemValue(act_2_offense_high_energy:6)} and {ItemValue(act_2_defense_energy:6)} and {ItemValue(act_2_utility_high_energy:3)}) or ({ItemValue(act_2_offense_high_energy:6)} and {ItemValue(act_2_utility_energy:3)} and {ItemValue(act_2_defense_high_energy:6)})"
    return ""

def act_two_blue_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """blue component for act_two_magick_power (supports 1-4)"""
    if int(level) == 1:
        return "{ItemValue(act_2_offense_s:1)} and |Sapphire Mox|"
    elif int(level) == 2:
        return "{ItemValue(act_2_offense_s:1)} and ({ItemValue(act_2_defense_s:1)} or {ItemValue(act_2_utility_s:1)}) and |Sapphire Mox|"
    elif int(level) == 3:
        return "{ItemValue(act_2_offense_s:2)} and ({ItemValue(act_2_defense_s:1)} or {ItemValue(act_2_utility_s:1)}) and |Sapphire Mox|"
    elif int(level) == 4:
        return "{ItemValue(act_2_offense_s:3)} and ({ItemValue(act_2_defense_s:2)} or {ItemValue(act_2_utility_s:2)}) and |Sapphire Mox|"
    return ""
    
def actTwoOrangePower(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """orange component for act_two_magick_power (supports 1-4)"""
    if int(level) == 1:
        return "{ItemValue(act_2_offense_r:1)} and |Ruby Mox|"
    elif int(level) == 2:
        return "{ItemValue(act_2_offense_r:1)} and ({ItemValue(act_2_defense_r:1)} or {ItemValue(act_2_utility_r:1)}) and |Ruby Mox|"
    elif int(level) == 3:
        return "{ItemValue(act_2_offense_r:2)} and ({ItemValue(act_2_defense_r:1)} or {ItemValue(act_2_utility_r:1)}) and |Ruby Mox|"
    elif int(level) == 4:
        return "{ItemValue(act_2_offense_r:3)} and ({ItemValue(act_2_defense_r:2)} or {ItemValue(act_2_utility_r:1)}) and |Ruby Mox|"
    return ""
    
def actTwoGreenPower(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """green component for act_two_magick_power (supports 1-4)"""
    if int(level) == 1:
        return "{ItemValue(act_2_offense_e:1)} and |Emerald Mox|"
    elif int(level) == 2:
        return "({ItemValue(act_2_offense_e:2)} or ({ItemValue(act_2_offense_e:1)} and {ItemValue(act_2_defense_e:1)})) and |Emerald Mox|"
    elif int(level) == 3:
        return "({ItemValue(act_2_offense_e:3)} or ({ItemValue(act_2_offense_e:2)} and {ItemValue(act_2_defense_e:1)})) and |Emerald Mox|"
    elif int(level) == 4:
        return "({ItemValue(act_2_offense_e:4)} or ({ItemValue(act_2_offense_e:3)} and {ItemValue(act_2_defense_e:1)})) and |Emerald Mox|"
    return ""

def act_two_magick_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """magick component for act_two_power (supports 1-8)"""
    if int(level) == 1:
        return "{act_two_blue_power(1)} or {actTwoOrangePower(1)} or {actTwoGreenPower(1)}"
    elif int(level) == 2:
        return "{act_two_blue_power(2)} or {actTwoOrangePower(2)} or {actTwoGreenPower(2)} or ({act_two_blue_power(1)} and {actTwoOrangePower(1)}) or ({act_two_blue_power(1)} and {actTwoGreenPower(1)}) or ({actTwoGreenPower(1)} and {actTwoOrangePower(1)})"
    elif int(level) == 3:
        return "{act_two_blue_power(3)} or {actTwoOrangePower(3)} or {actTwoGreenPower(3)} or ({act_two_blue_power(1)} and {actTwoOrangePower(1)}) or ({act_two_blue_power(1)} and {actTwoGreenPower(1)}) or ({actTwoGreenPower(1)} and {actTwoOrangePower(1)})"
    elif int(level) == 4:
        return "{act_two_blue_power(3)} or {actTwoOrangePower(3)} or {actTwoGreenPower(3)} or ({act_two_blue_power(2)} and {actTwoOrangePower(1)}) or ({act_two_blue_power(2)} and {actTwoGreenPower(1)}) or ({actTwoGreenPower(2)} and {actTwoOrangePower(1)}) or ({act_two_blue_power(1)} and {actTwoOrangePower(2)}) or ({act_two_blue_power(1)} and {actTwoGreenPower(2)}) or ({actTwoGreenPower(1)} and {actTwoOrangePower(2)})"
    elif int(level) == 5:
        return "{act_two_blue_power(3)} or {actTwoOrangePower(3)} or {actTwoGreenPower(3)} or ({act_two_blue_power(2)} and {actTwoOrangePower(2)}) or ({act_two_blue_power(2)} and {actTwoGreenPower(2)}) or ({actTwoGreenPower(2)} and {actTwoOrangePower(2)})"
    elif int(level) == 6:
        return "{act_two_blue_power(4)} or {actTwoOrangePower(4)} or {actTwoGreenPower(4)} or ({act_two_blue_power(3)} and {actTwoOrangePower(2)}) or ({act_two_blue_power(3)} and {actTwoGreenPower(2)}) or ({actTwoGreenPower(3)} and {actTwoOrangePower(2)}) or ({act_two_blue_power(2)} and {actTwoOrangePower(3)}) or ({act_two_blue_power(2)} and {actTwoGreenPower(3)}) or ({actTwoGreenPower(2)} and {actTwoOrangePower(3)})"
    elif int(level) == 7:
        return "{act_two_blue_power(4)} or {actTwoOrangePower(4)} or {actTwoGreenPower(4)} or ({act_two_blue_power(3)} and {actTwoOrangePower(3)}) or ({act_two_blue_power(3)} and {actTwoGreenPower(3)}) or ({actTwoGreenPower(3)} and {actTwoOrangePower(3)})"
    elif int(level) == 8:
        return "({act_two_blue_power(4)} and {actTwoOrangePower(3)}) or ({act_two_blue_power(4)} and {actTwoGreenPower(3)}) or ({actTwoGreenPower(4)} and {actTwoOrangePower(3)}) or ({act_two_blue_power(3)} and {actTwoOrangePower(4)}) or ({act_two_blue_power(3)} and {actTwoGreenPower(4)}) or ({actTwoGreenPower(3)} and {actTwoOrangePower(4)})"
    return ""

# You can also return a string from your function, and it will be evaluated as a requires string.
def act_two_power(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """is the player strong enough? (in act 2, specifically) (supports 1-20)"""
    if int(level) == 1:
        return "{act_two_blood_power(1)} or {act_two_bone_power(1)} or {act_two_energy_power(1)} or {act_two_magick_power(1)}"
    elif int(level) == 2:
        return "{act_two_blood_power(2)} or {act_two_bone_power(2)} or {act_two_energy_power(2)} or {act_two_magick_power(2)} OR ({act_two_blood_power(1)} and {act_two_bone_power(1)}) or ({act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_magick_power(1)}) or ({act_two_energy_power(1)} and {act_two_bone_power(1)}) or ({act_two_blood_power(1)} and {act_two_energy_power(1)}) or ({act_two_bone_power(1)} and {act_two_magick_power(1)})"
    elif int(level) == 3:
        return "{act_two_blood_power(3)} or {act_two_bone_power(3)} or {act_two_energy_power(3)} or {act_two_magick_power(3)} OR ({act_two_blood_power(1)} and {act_two_bone_power(1)}) or ({act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_magick_power(1)}) or ({act_two_energy_power(1)} and {act_two_bone_power(1)}) or ({act_two_blood_power(1)} and {act_two_energy_power(1)}) or ({act_two_bone_power(1)} and {act_two_magick_power(1)})"
    elif int(level) == 4:
        return "{act_two_blood_power(3)} or {act_two_bone_power(3)} or {act_two_energy_power(3)} or {act_two_magick_power(3)} OR ({act_two_blood_power(2)} and {act_two_bone_power(1)}) or ({act_two_energy_power(2)} and {act_two_magick_power(1)}) or ({act_two_blood_power(2)} and {act_two_magick_power(1)}) or ({act_two_energy_power(2)} and {act_two_bone_power(1)}) or ({act_two_blood_power(2)} and {act_two_energy_power(1)}) or ({act_two_bone_power(2)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(2)}) or ({act_two_energy_power(1)} and {act_two_magick_power(2)}) or ({act_two_blood_power(1)} and {act_two_magick_power(2)}) or ({act_two_energy_power(1)} and {act_two_bone_power(2)}) or ({act_two_blood_power(1)} and {act_two_energy_power(2)}) or ({act_two_bone_power(1)} and {act_two_magick_power(2)}) OR ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_magick_power(1)}) and {act_two_blood_power(1)} or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)})"
    elif int(level) == 5:
        return "{act_two_blood_power(3)} or {act_two_bone_power(3)} or {act_two_energy_power(3)} or {act_two_magick_power(3)} OR ({act_two_blood_power(2)} and {act_two_bone_power(2)}) or ({act_two_energy_power(2)} and {act_two_magick_power(2)}) or ({act_two_blood_power(2)} and {act_two_magick_power(2)}) or ({act_two_energy_power(2)} and {act_two_bone_power(2)}) or ({act_two_blood_power(2)} and {act_two_energy_power(2)}) or ({act_two_bone_power(2)} and {act_two_magick_power(2)}) OR ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_magick_power(1)}) and {act_two_blood_power(1)} or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)})"
    elif int(level) == 6:
        return "{act_two_blood_power(4)} or {act_two_bone_power(4)} or {act_two_energy_power(4)} or {act_two_magick_power(3)} OR ({act_two_blood_power(2)} and {act_two_bone_power(2)}) or ({act_two_energy_power(2)} and {act_two_magick_power(2)}) or ({act_two_blood_power(2)} and {act_two_magick_power(2)}) or ({act_two_energy_power(2)} and {act_two_bone_power(2)}) or ({act_two_blood_power(2)} and {act_two_energy_power(2)}) or ({act_two_bone_power(2)} and {act_two_magick_power(2)}) OR ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_magick_power(1)}) and {act_two_blood_power(1)} or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) OR ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)})"
    elif int(level) == 7:
        return "{act_two_blood_power(4)} or {act_two_bone_power(4)} or {act_two_energy_power(4)} or {act_two_magick_power(4)} OR ({act_two_blood_power(3)} and {act_two_bone_power(2)}) or ({act_two_energy_power(3)} and {act_two_magick_power(2)}) or ({act_two_blood_power(3)} and {act_two_magick_power(2)}) or ({act_two_energy_power(3)} and {act_two_bone_power(2)}) or ({act_two_blood_power(3)} and {act_two_energy_power(2)}) or ({act_two_bone_power(3)} and {act_two_magick_power(2)}) or ({act_two_blood_power(2)} and {act_two_bone_power(3)}) or ({act_two_energy_power(2)} and {act_two_magick_power(3)}) or ({act_two_blood_power(2)} and {act_two_magick_power(3)}) or ({act_two_energy_power(2)} and {act_two_bone_power(3)}) or ({act_two_blood_power(2)} and {act_two_energy_power(3)}) or ({act_two_bone_power(2)} and {act_two_magick_power(3)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)}) or ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_magick_power(2)}) and {act_two_blood_power(2)} or ({act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)}) or ({act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(2)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(2)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(2)})"
    elif int(level) == 8:
        return "{act_two_blood_power(5)} or {act_two_bone_power(5)} or {act_two_energy_power(5)} or {act_two_magick_power(5)} OR ({act_two_blood_power(3)} and {act_two_bone_power(4)}) or ({act_two_energy_power(3)} and {act_two_magick_power(4)}) or ({act_two_blood_power(3)} and {act_two_magick_power(4)}) or ({act_two_energy_power(3)} and {act_two_bone_power(4)}) or ({act_two_blood_power(3)} and {act_two_energy_power(4)}) or ({act_two_bone_power(3)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_bone_power(3)}) or ({act_two_energy_power(4)} and {act_two_magick_power(3)}) or ({act_two_blood_power(4)} and {act_two_magick_power(3)}) or ({act_two_energy_power(4)} and {act_two_bone_power(3)}) or ({act_two_blood_power(4)} and {act_two_energy_power(3)}) or ({act_two_bone_power(4)} and {act_two_magick_power(3)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)}) or ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_magick_power(2)}) and {act_two_blood_power(2)} or ({act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)}) or ({act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(1)} and {act_two_energy_power(1)} and {act_two_magick_power(1)}) or ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(1)} and {act_two_energy_power(2)} and {act_two_magick_power(1)}) or ({act_two_blood_power(1)} and {act_two_bone_power(2)} and {act_two_energy_power(1)} and {act_two_magick_power(2)})"
    elif int(level) == 9:
        return "{act_two_blood_power(5)} or {act_two_bone_power(5)} or {act_two_energy_power(5)} or {act_two_magick_power(5)} OR ({act_two_blood_power(4)} and {act_two_bone_power(4)}) or ({act_two_energy_power(4)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_magick_power(4)}) or ({act_two_energy_power(4)} and {act_two_bone_power(4)}) or ({act_two_blood_power(4)} and {act_two_energy_power(4)}) or ({act_two_bone_power(4)} and {act_two_magick_power(4)}) OR ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_energy_power(3)}) or ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_magick_power(3)}) and {act_two_blood_power(3)} or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)})"
    elif int(level) == 10:
        return "{act_two_blood_power(6)} or {act_two_bone_power(6)} or {act_two_energy_power(6)} or {act_two_magick_power(6)} OR ({act_two_blood_power(4)} and {act_two_bone_power(4)}) or ({act_two_energy_power(4)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_magick_power(4)}) or ({act_two_energy_power(4)} and {act_two_bone_power(4)}) or ({act_two_blood_power(4)} and {act_two_energy_power(4)}) or ({act_two_bone_power(4)} and {act_two_magick_power(4)}) OR ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_energy_power(3)}) or ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_magick_power(3)}) and {act_two_blood_power(3)} or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)})"
    elif int(level) == 11:
        return "{act_two_blood_power(7)} or {act_two_bone_power(7)} or {act_two_energy_power(7)} or {act_two_magick_power(7)} OR ({act_two_blood_power(5)} and {act_two_bone_power(5)}) or ({act_two_energy_power(5)} and {act_two_magick_power(5)}) or ({act_two_blood_power(5)} and {act_two_magick_power(5)}) or ({act_two_energy_power(5)} and {act_two_bone_power(5)}) or ({act_two_blood_power(5)} and {act_two_energy_power(5)}) or ({act_two_bone_power(5)} and {act_two_magick_power(5)}) OR ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_energy_power(3)}) or ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_magick_power(3)}) and {act_two_blood_power(3)} or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) or ({act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)}) OR ({act_two_blood_power(2)} and {act_two_bone_power(2)} and {act_two_energy_power(2)} and {act_two_magick_power(2)})"
    elif int(level) == 12:
        return "{act_two_blood_power(8)} or {act_two_bone_power(8)} or {act_two_energy_power(8)} or {act_two_magick_power(8)} OR ({act_two_blood_power(6)} and {act_two_bone_power(6)}) or ({act_two_energy_power(6)} and {act_two_magick_power(6)}) or ({act_two_blood_power(6)} and {act_two_magick_power(6)}) or ({act_two_energy_power(6)} and {act_two_bone_power(6)}) or ({act_two_blood_power(6)} and {act_two_energy_power(6)}) or ({act_two_bone_power(6)} and {act_two_magick_power(6)}) OR ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_energy_power(4)}) or ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_magick_power(4)}) and {act_two_blood_power(4)} or ({act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(4)}) or ({act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(4)}) OR ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)})"
    elif int(level) == 13:
        return "{act_two_blood_power(8)} or {act_two_bone_power(8)} or {act_two_energy_power(8)} or {act_two_magick_power(8)} OR ({act_two_blood_power(7)} and {act_two_bone_power(7)}) or ({act_two_energy_power(7)} and {act_two_magick_power(7)}) or ({act_two_blood_power(7)} and {act_two_magick_power(7)}) or ({act_two_energy_power(7)} and {act_two_bone_power(7)}) or ({act_two_blood_power(7)} and {act_two_energy_power(7)}) or ({act_two_bone_power(7)} and {act_two_magick_power(7)}) OR ({act_two_blood_power(5)} and {act_two_bone_power(5)} and {act_two_energy_power(5)}) or ({act_two_blood_power(5)} and {act_two_bone_power(5)} and {act_two_magick_power(5)}) and {act_two_blood_power(5)} or ({act_two_bone_power(5)} and {act_two_energy_power(5)} and {act_two_magick_power(5)}) or ({act_two_bone_power(5)} and {act_two_energy_power(5)} and {act_two_magick_power(5)}) OR ({act_two_blood_power(3)} and {act_two_bone_power(3)} and {act_two_energy_power(3)} and {act_two_magick_power(3)})"
    elif int(level) == 14:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)}) or ({act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_blood_power(8)} and {act_two_magick_power(8)}) or ({act_two_energy_power(8)} and {act_two_bone_power(8)}) or ({act_two_blood_power(8)} and {act_two_energy_power(8)}) or ({act_two_bone_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_energy_power(6)}) or ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_magick_power(6)}) or ({act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(6)}) or ({act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(6)}) OR ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(4)})"
    elif int(level) == 15:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)}) or ({act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_blood_power(8)} and {act_two_magick_power(8)}) or ({act_two_energy_power(8)} and {act_two_bone_power(8)}) or ({act_two_blood_power(8)} and {act_two_energy_power(8)}) or ({act_two_bone_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(7)} and {act_two_bone_power(7)} and {act_two_energy_power(7)}) or ({act_two_blood_power(7)} and {act_two_bone_power(7)} and {act_two_magick_power(7)}) or ({act_two_bone_power(7)} and {act_two_energy_power(7)} and {act_two_magick_power(7)}) or ({act_two_bone_power(7)} and {act_two_energy_power(7)} and {act_two_magick_power(7)}) OR ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(4)})"
    elif int(level) == 16:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_energy_power(8)}) or ({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(5)} and {act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_bone_power(5)} and {act_two_energy_power(4)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_energy_power(5)} and {act_two_magick_power(4)}) or ({act_two_blood_power(4)} and {act_two_bone_power(4)} and {act_two_energy_power(4)} and {act_two_magick_power(5)})"
    elif int(level) == 17:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_energy_power(8)}) or ({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(6)} and {act_two_bone_power(5)} and {act_two_energy_power(5)} and {act_two_magick_power(5)}) or ({act_two_blood_power(5)} and {act_two_bone_power(6)} and {act_two_energy_power(5)} and {act_two_magick_power(5)}) or ({act_two_blood_power(5)} and {act_two_bone_power(5)} and {act_two_energy_power(6)} and {act_two_magick_power(5)}) or ({act_two_blood_power(5)} and {act_two_bone_power(5)} and {act_two_energy_power(5)} and {act_two_magick_power(6)})"
    elif int(level) == 18:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_energy_power(8)}) or ({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_energy_power(5)} and {act_two_magick_power(5)}) or ({act_two_blood_power(6)} and {act_two_bone_power(5)} and {act_two_energy_power(6)} and {act_two_magick_power(5)}) or ({act_two_blood_power(6)} and {act_two_bone_power(5)} and {act_two_energy_power(5)} and {act_two_magick_power(6)}) or ({act_two_blood_power(5)} and {act_two_bone_power(5)} and {act_two_energy_power(6)} and {act_two_magick_power(6)}) or ({act_two_blood_power(5)} and {act_two_bone_power(6)} and {act_two_energy_power(5)} and {act_two_magick_power(6)}) or ({act_two_blood_power(5)} and {act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(5)})"
    elif int(level) == 19:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_energy_power(8)}) or ({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(5)}) or ({act_two_blood_power(6)} and {act_two_bone_power(5)} and {act_two_energy_power(6)} and {act_two_magick_power(6)}) or ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_energy_power(5)} and {act_two_magick_power(6)}) or ({act_two_blood_power(5)} and {act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(6)})"
    elif int(level) == 20:
        return "({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_energy_power(8)}) or ({act_two_blood_power(8)} and {act_two_bone_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) or ({act_two_bone_power(8)} and {act_two_energy_power(8)} and {act_two_magick_power(8)}) OR ({act_two_blood_power(6)} and {act_two_bone_power(6)} and {act_two_energy_power(6)} and {act_two_magick_power(6)})"
    return ""

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

def ItemValue(world: World, multiworld: MultiWorld, state: CollectionState, player: int, args: str):
    """When passed a string with this format: 'valueName:int',
    this function will check if the player has collect at least 'int' valueName worth of items\n
    eg. {ItemValue(Coins:12)} will check if the player has collect at least 12 coins worth of items
    """

    args_list = args.split(":")
    if not len(args_list) == 2 or not args_list[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({args_list[0]}:12)'")
    args_list[0] = args_list[0].lower().strip()
    args_list[1] = int(args_list[1].strip())

    if not hasattr(world, 'item_values_cache'): #Cache made for optimization purposes
        world.item_values_cache = {}

    if not world.item_values_cache.get(player, {}):
        world.item_values_cache[player] = {
            'state': {},
            'count': {},
            }

    if (args_list[0] not in world.item_values_cache[player].get('count', {}).keys()
            or world.item_values_cache[player].get('state') != dict(state.prog_items[player])):
        #Run First Time or if state changed since last check
        existing_item_values = get_items_with_value(world, multiworld, args_list[0])
        total_Count = 0
        for name, value in existing_item_values.items():
            count = state.count(name, player)
            if count > 0:
                total_Count += count * value
        world.item_values_cache[player]['count'][args_list[0]] = total_Count
        world.item_values_cache[player]['state'] = dict(state.prog_items[player]) #save the current gotten items to check later if its the same
    return world.item_values_cache[player]['count'][args_list[0]] >= args_list[1]


# Two useful functions to make require work if an item is disabled instead of making it inaccessible
def OptOne(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Check if the passed item (with or without ||) is enabled, then this returns |item:count|
    where count is clamped to the maximum number of said item in the itempool.\n
    Eg. requires: "{OptOne(|DisabledItem|)} and |other items|" become "|DisabledItem:0| and |other items|" if the item is disabled.
    """
    if item == "":
        return "" #Skip this function if item is left blank
    if not items_counts:
        items_counts = world.get_item_counts()

    require_type = 'item'

    if '@' in item[:2]:
        require_type = 'category'

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = '1'

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_type == 'category':
        if item_count.isnumeric():
            #Only loop if we can use the result to clamp
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(int(item_count), 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    elif require_type == 'item':
        if item_count.isnumeric():
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(int(item_count), 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
def OptAll(world: World, multiworld: MultiWorld, state: CollectionState, player: int, requires: str):
    """Check the passed require string and loop every item to check if they're enabled,
    then returns the require string with items counts adjusted using OptOne\n
    eg. requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"
    become "|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|" """
    requires_list = requires

    items_counts = world.get_item_counts()

    functions = {}
    if requires_list == "":
        return True
    for item in re.findall(r'\{(\w+)\(([^)]*)\)\}', requires_list):
        #so this function doesn't try to get item from other functions, in theory.
        func_name = item[0]
        functions[func_name] = item[1]
        requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "{" + func_name + "(temp)}")
    # parse user written statement into list of each item
    for item in re.findall(r'\|[^|]+\|', requires):
        itemScanned = OptOne(world, multiworld, state, player, item, items_counts)
        requires_list = requires_list.replace(item, itemScanned)

    for function in functions:
        requires_list = requires_list.replace("{" + function + "(temp)}", "{" + func_name + "(" + functions[func_name] + ")}")
    return requires_list

# Rule to expose the can_reach_location core function
def canReachLocation(world: World, multiworld: MultiWorld, state: CollectionState, player: int, location: str):
    """Can the player reach the given location?"""
    if state.can_reach_location(location, player):
        return True
    return False
