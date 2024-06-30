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
class Act1Enabled(DefaultOnToggle):
    """Do you want to play Act I in this rando?"""
    display_name = "Act I Enabled"

class Act2Enabled(Toggle):
    """Do you want to play Act II in this rando?"""
    display_name = "Act II Enabled"

class Act3Enabled(Toggle):
    """Do you want to play Act III in this rando?"""
    display_name = "Act III Enabled"

class KayceesModEnabled(Toggle):
    """Do you want to play Kaycee's Mod in this rando?"""
    display_name = "Kaycee's Mod Enabled"

class ConsumableRando(Toggle):
    """Should the ability to play consumables (In Act I, Act III, and Kaycee's Mod) be randomized?"""
    display_name = "Consumable Rando"

class StarterDeckRando(Toggle):
    """Should the ability to use starter decks (In Act II and Kaycee's Mod) be randomized?"""
    display_name = "Starter Deck Rando"


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["Act_1_Enabled"] = Act1Enabled
    options["Act_2_Enabled"] = Act2Enabled
    options["Act_3_Enabled"] = Act3Enabled
    options["Kaycees_Mod_Enabled"] = KayceesModEnabled
    options["Consumable_Rando_Enabled"] = ConsumableRando
    options["Starter_Deck_Rando_Enabled"] = StarterDeckRando
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options