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

class HammerRando(Toggle):
    """Should the ability to use the hammer (In Act II and III) be randomized?"""
    display_name = "Hammer Rando"

class CloverRando(Toggle):
    """Should the ability to use the clover (In Act I and II) be randomized?
    In Act I, you'll have to go get the clover yourself.
    """
    display_name = "Clover Rando"

class StackSizeRando(Range):
    """This will reduce the maximum amount of one card you can have in your deck in Act II.
    The amount you set is how many items will be created that nullify this restriction, one at a time.
    At the minimum of 5, you can only have 5 of one card, and 15 items will exist that increase this.
    At the maximum of 20, this restriction is removed. This does not affect other acts."""
    range_start = 5
    range_end = 20
    default = 20
    display_name = "Stack Size Rando"
    
class DeckSizeRando(Range):
    """This will increase the minimum amount of cards you must have in your deck in Act II.
    The amount you set is how many items will be created that nullify this restriction, one at a time.
    At the maximum of 35, you must have 35 cards in your deck, and 15 items will exist that decrease this.
    At the minimum of 20, this restriction is removed. This does not affect other acts."""
    range_start = 20
    range_end = 35
    default = 20
    display_name = "Deck Size Rando"

class VesselUpgradeRando(Toggle):
    """Should the empty vessel upgrades (in Act III) be randomized? This will create 3 "Vessel Upgrade" items.  
    For each Vessel Upgrade item, you may pick up a vessel upgrade from Boss Rewards.
    With none, you must leave them there (so that you may pick them up later).
    There will be another item corresponding to the Conduit Upgrade in Resplendent Bastion."""
    display_name = "Vessel Upgrade Rando"

class Act1DupeLocations(DefaultOnToggle):
    """Should there be duplicate locations for every location in Act I?

    Note: for this option and the next 6, consider how many acts you're playing.
    If you're playing just one Act, it's inadvisable to disable these options.
    Even if you're playing every act, you shouldn't disable all of these. (But you should disable most.)
    It's pretty easy to end up with too few locations if you disable any of these.
    That said, if you are playing acts with a lot of item overlap, disabling at least one of these is a good idea."""
    display_name = "Act I Duplicate Locations"

class Act2DupeLocations(DefaultOnToggle):
    """Should there be duplicate locations for every location in Act II?"""
    display_name = "Act II Duplicate Locations"

class RobobucksLocations(DefaultOnToggle):
    """Should there be locations for each piece of robobucks you can pick up in Botopia? (Act III)"""
    display_name = "Robobucks Locations"

class CardChoiceLocations(DefaultOnToggle):
    """Should there be locations for each Card Choice node in Act III?
    If this option is turned on, you're bound to have a deck with cards you can't play, making Act III harder.
    (However, this is a good thing. Act III is too easy, especially if you've already done the first 2 acts in the rando.)"""
    display_name = "Card Choice Locations"

class UniqueCardLocations(DefaultOnToggle):
    """Should there be locations for each unique card pickup in Act III? (specifically, Ourobot, Lonely Wizbot, Fishbot)"""
    display_name = "Unique Card Locations"

class KayceesModDupeLocations(DefaultOnToggle):
    """Should there be duplicate locations for every location in Kaycee's Mod?"""
    display_name = "Kaycee's Mod Duplicate Locations"

class KayceesModChallengeLocations(DefaultOnToggle):
    """Should there be locations for beating every encounter with a certain amount of challenge points?
    There aren't duplicates of these.
    You'll never be expected to do the Grizzly Bosses challenge (it sucks)."""
    display_name = "Kaycee's Mod Challenge Locations"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["Act_1_Enabled"] = Act1Enabled
    options["Act_2_Enabled"] = Act2Enabled
    options["Act_3_Enabled"] = Act3Enabled
    options["Kaycees_Mod_Enabled"] = KayceesModEnabled
    options["Consumable_Rando"] = ConsumableRando
    options["Hammer_Rando"] = HammerRando
    options["Clover_Rando"] = CloverRando
    options["Stack_Size_Rando"] = StackSizeRando
    options["Deck_Size_Rando"] = DeckSizeRando
    options["Vessel_Upgrade_Rando"] = VesselUpgradeRando
    options["Act_1_Duplicate_Locations"] = Act1DupeLocations
    options["Act_2_Duplicate_Locations"] = Act2DupeLocations
    options["Robobucks_Locations"] = RobobucksLocations
    options["Card_Choice_Locations"] = CardChoiceLocations
    options["Unique_Card_Locations"] = UniqueCardLocations
    options["Kaycees_Mod_Duplicate_Locations"] = KayceesModDupeLocations
    options["Kaycees_Mod_Challenge_Locations"] = KayceesModChallengeLocations
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options