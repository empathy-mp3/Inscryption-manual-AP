# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#

class ConsumableRando(Toggle):
    """Should the ability to play consumables (In Act I, Act III, and Kaycee's Mod) be randomized?"""
    display_name = "Consumable Rando"

class DupeLocations(DefaultOnToggle):
    """Should there be duplicate locations for every location?
    Also, this doesn't apply to challenge locations.
    You should have at least one set of duplicate locations enabled (or it will fail to generate)."""
    display_name = "Duplicate Locations"

class ChallengeLocations(DefaultOnToggle):
    """Should there be locations for beating every encounter with a certain amount of challenge points?
    You'll never be expected to do the Grizzly Bosses challenge (it sucks)."""
    display_name = "Challenge Locations"

class DupeChallengeLocations(Toggle):
    """Should there be duplicates of Challenge Locations?
    Only does anything if Challenge_Locations are enabled."""
    display_name = "Dupe Challenge Locations"

class LogicDifficulty(Range):
    """How hard do you want your logic? The higher the number, the harder it is.
    You may be expected to do very difficult and/or grindy things with very little equipment.
    Specifically, how much do you like bashing your head against a wall?"""
    range_start = 0
    range_end = 4
    default = 0
    display_name = "Logic Difficulty"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["consumable_rando"] = ConsumableRando
    options["Duplicate_Locations"] = DupeLocations
    options["Challenge_Locations"] = ChallengeLocations
    options["Duplicate_Challenge_Locations"] = DupeChallengeLocations
    options["Logic_Difficulty"] = LogicDifficulty
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options