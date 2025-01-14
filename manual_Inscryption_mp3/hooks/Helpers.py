from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem
from .. import Helpers


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if category_name == "act2kaycee":
        return Helpers.is_option_enabled(multiworld, player, "act_2_enabled") or Helpers.is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    if category_name == "act2act3":
        return Helpers.is_option_enabled(multiworld, player, "act_2_enabled") or Helpers.is_option_enabled(multiworld, player, "act_3_enabled")
    if category_name == "act1act2kaycee":
        return Helpers.is_option_enabled(multiworld, player, "act_1_enabled") or Helpers.is_option_enabled(multiworld, player, "act_2_enabled") or Helpers.is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    if category_name == "act1kaycee":
        return Helpers.is_option_enabled(multiworld, player, "act_1_enabled") or Helpers.is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    if category_name == "act1act3kaycee":
        return Helpers.is_option_enabled(multiworld, player, "act_1_enabled") or Helpers.is_option_enabled(multiworld, player, "act_3_enabled") or Helpers.is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    if category_name == "act1act2":
        return Helpers.is_option_enabled(multiworld, player, "act_1_enabled") or Helpers.is_option_enabled(multiworld, player, "act_2_enabled")
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    return None
