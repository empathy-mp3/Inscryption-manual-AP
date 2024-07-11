# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    act1 = get_option_value(multiworld, player, "Act_1_Enabled") or False
    act2 = get_option_value(multiworld, player, "Act_2_Enabled") or False
    act3 = get_option_value(multiworld, player, "Act_3_Enabled") or False
    kaycee = get_option_value(multiworld, player, "Kaycees_Mod_Enabled") or False
    consumable = get_option_value(multiworld, player, "Consumable_Rando_Enabled") or False
    starter = get_option_value(multiworld, player, "Starter_Deck_Rando_Enabled") or False
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove

    for location in world.location_table:
        if "act1" in location.get("category", []) and not act1:
            locationNamesToRemove.append(location["name"])
        elif "act2" in location.get("category", []) and not act2:
            locationNamesToRemove.append(location["name"])
        elif "act3" in location.get("category", []) and not act3:
            locationNamesToRemove.append(location["name"])
        elif "kaycee" in location.get("category", []) and not kaycee:
            locationNamesToRemove.append(location["name"])
        elif "act2kaycee" in location.get("category", []) and not (act2 or kaycee):
            locationNamesToRemove.append(location["name"])
        elif "act2act3" in location.get("category", []) and not (act2 or act3):
            locationNamesToRemove.append(location["name"])
        elif "act1act2kaycee" in location.get("category", []) and not (act1 or act2 or kaycee):
            locationNamesToRemove.append(location["name"])
        elif "act1kaycee" in location.get("category", []) and not (act1 or kaycee):
            locationNamesToRemove.append(location["name"])
        elif "mycobot" in location.get("category", []) and not (act2 and act3):
            locationNamesToRemove.append(location["name"])
        elif "Consumable" in location.get("category", []) and not consumable:
            locationNamesToRemove.append(location["name"])
        elif "Starter Deck" in location.get("category", []) and not starter:
            locationNamesToRemove.append(location["name"])

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    act1 = is_option_enabled(multiworld, player, "Act_1_Enabled")
    act2 = is_option_enabled(multiworld, player, "Act_2_Enabled")
    act3 = is_option_enabled(multiworld, player, "Act_3_Enabled")
    kaycee = is_option_enabled(multiworld, player, "Kaycees_Mod_Enabled")
    consumable = is_option_enabled(multiworld, player, "Consumable_Rando_Enabled")
    starter = is_option_enabled(multiworld, player, "Starter_Deck_Rando_Enabled")
    hammer = is_option_enabled(multiworld, player, "Hammer_Rando_Enabled")
    stack = get_option_value(multiworld, player, "Stack_Size_Rando")
    deck = get_option_value(multiworld, player, "Deck_Size_Rando")

    if act1:
        start_item_list = ["Squirrel"]
        for item_name in start_item_list:
            item = next(i for i in item_pool if i.name == item_name)
            multiworld.push_precollected(item)
            item_pool.remove(item)

    if act3:
        start_item_list = ["Empty Vessel"]
        for item_name in start_item_list:
            item = next(i for i in item_pool if i.name == item_name)
            multiworld.push_precollected(item)
            item_pool.remove(item)

    if kaycee and starter:
        multiworld.random.shuffle(item_pool) # shuffles the pool to give random items
        for count in range(1): # give 1 starting items
            item = next(i for i in item_pool if "kayceestarter" in world.item_name_to_item[i.name].get("category", []))
            multiworld.push_precollected(item)
            item_pool.remove(item)
    

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    stack = get_option_value(multiworld, player, "Stack_Size_Rando")
    deck = get_option_value(multiworld, player, "Deck_Size_Rando")
    act2 = is_option_enabled(multiworld, player, "Act_2_Enabled")

    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names


    if act2:
        for i in range(15-stack):
            itemNamesToRemove.append("+1 Max Card Stack Size")
        for i in range(15-deck):
            itemNamesToRemove.append("-1 Min Deck Size")

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    act1 = is_option_enabled(multiworld, player, "Act_1_Enabled")
    act2 = is_option_enabled(multiworld, player, "Act_2_Enabled")
    act3 = is_option_enabled(multiworld, player, "Act_3_Enabled")
    kaycee = is_option_enabled(multiworld, player, "Kaycees_Mod_Enabled")
    consumable = is_option_enabled(multiworld, player, "Consumable_Rando_Enabled")
    starter = is_option_enabled(multiworld, player, "Starter_Deck_Rando_Enabled")
    hammer = is_option_enabled(multiworld, player, "Hammer_Rando_Enabled")
    stack = is_option_enabled(multiworld, player, "Stack_Size_Rando")
    deck = is_option_enabled(multiworld, player, "Deck_Size_Rando")

    def addReq(loc, req):
        if loc["requires"] == []:
            loc["requires"] = req
        else:
            loc["requires"] = "(" + loc["requires"] + ") and (" + req + ")"

    if act1:
        addReq(region_table["Act I - Late Woodlands"], "{ItemValue(act_1_offense:1)} and |Squirrel|")
        addReq(region_table["Act I - Dagger"], "|Caged Wolf|")
        addReq(region_table["Act I - Prospector"], "{ItemValue(act_1_offense:3)}")
        addReq(region_table["Act I - Late Wetlands"], "({ItemValue(act_1_offense:4)} or ({ItemValue(act_1_offense:3)} and {ItemValue(act_1_defense:2)}) or ({ItemValue(act_1_offense:3)} and {ItemValue(act_1_utility:1)}) or ({ItemValue(act_1_offense:2)} and {ItemValue(act_1_defense:2)} and {ItemValue(act_1_utility:1)}))")
        addReq(region_table["Act I - Angler"], "({ItemValue(act_1_offense:6)} or ({ItemValue(act_1_offense:4)} and {ItemValue(act_1_defense:3)}) or ({ItemValue(act_1_offense:4)} and {ItemValue(act_1_utility:2)}) or ({ItemValue(act_1_offense:3)} and {ItemValue(act_1_defense:2)} and {ItemValue(act_1_utility:1)}))")
        addReq(region_table["Act I - Late Snow Line"], "({ItemValue(act_1_offense:7)} or ({ItemValue(act_1_offense:5)} and {ItemValue(act_1_defense:4)}) or ({ItemValue(act_1_offense:5)} and {ItemValue(act_1_utility:3)}) or ({ItemValue(act_1_offense:4)} and {ItemValue(act_1_defense:3)} and {ItemValue(act_1_utility:2)}))")
        addReq(region_table["Act I - Trapper"], "({ItemValue(act_1_offense:8)} or ({ItemValue(act_1_offense:6)} and {ItemValue(act_1_defense:4)}) or ({ItemValue(act_1_offense:6)} and {ItemValue(act_1_utility:3)}) or ({ItemValue(act_1_offense:5)} and {ItemValue(act_1_defense:3)} and {ItemValue(act_1_utility:2)}))")
        addReq(region_table["Act I - Leshy"], "({ItemValue(act_1_offense:9)} or ({ItemValue(act_1_offense:7)} and {ItemValue(act_1_defense:5)}) or ({ItemValue(act_1_offense:7)} and {ItemValue(act_1_utility:4)}) or ({ItemValue(act_1_offense:6)} and {ItemValue(act_1_defense:4)} and {ItemValue(act_1_utility:3)}))")
        addReq(region_table["Act I - End"], "|Caged Wolf|")

    if act1 and consumable:
        addReq(region_table["Act I - Eye"], "|Special Dagger|")
        addReq(region_table["Act I - Post-Angler"], "|@act1consumable:3|")
        addReq(region_table["Act I - Post-Trapper"], "|@act1consumable:5|")
        addReq(region_table["Act I - End"], "|Special Dagger|")

    if act2:
        addReq(region_table["Act II - Prospector"], "{test()}")
        addReq(region_table["Act II - Kaycee"], "{act_two_power(2)}")
        addReq(region_table["Act II - Sawyer"], "{act_two_power(4)}")
        addReq(region_table["Act II - Royal"], "{act_two_power(5)}")
        addReq(region_table["Act II - Angler"], "{act_two_power(5)}")
        addReq(region_table["Act II - Trapper"], "{act_two_power(6)}")
        addReq(region_table["Act II - Leshy"], "{act_two_power(7)}")
        addReq(region_table["Act II - Grimora"], "{act_two_power(7)}")
        addReq(region_table["Act II - P03"], "{act_two_power(8)}")
        addReq(region_table["Act II - Magnificus"], "{act_two_power(8)}")

    if act3:
        addReq(region_table["Act III - Initial Gauntlet"], "|Empty Vessel| and ((|Shieldbot| and (|Energy Bot| or |Double Gunner|)) or |Sniper Bot|)")
        addReq(region_table["Act III - Pre-Bridge"], "({ItemValue(act_3_offense:5)} or ({ItemValue(act_3_offense:4)} and {ItemValue(act_3_defense:4)}) or ({ItemValue(act_3_offense:4)} and {ItemValue(act_3_utility:4)}) or ({ItemValue(act_3_offense:4)} and {ItemValue(act_3_defense:4)} and {ItemValue(act_3_utility:3)}))")
        addReq(region_table["Act III - Post-Bridge"], "({ItemValue(act_3_offense:8)} or {ItemValue(act_3_offense_bridge:5)} or ({ItemValue(act_3_offense_bridge:4)} and {ItemValue(act_3_defense:6)}) or {ItemValue(act_3_defense_bridge:7)} or ({ItemValue(act_3_offense:6)} and {ItemValue(act_3_utility:5)}) or ({ItemValue(act_3_offense_bridge:3)} and {ItemValue(act_3_utility:7)}) or {ItemValue(act_3_utility_bridge:6)} or ({ItemValue(act_3_offense:6)} and {ItemValue(act_3_defense:5)} and {ItemValue(act_3_utility:5)}) or ({ItemValue(act_3_offense_bridge:4)} and {ItemValue(act_3_defense:4)} and {ItemValue(act_3_utility:4)}) or ({ItemValue(act_3_defense_bridge:4)} and {ItemValue(act_3_utility_bridge:5)}))")
        addReq(region_table["Act III - End"], "({ItemValue(act_3_offense:9)} or {ItemValue(act_3_offense_bridge:6)} or ({ItemValue(act_3_offense_bridge:5)} and {ItemValue(act_3_defense:7)}) or {ItemValue(act_3_defense_bridge:8)} or ({ItemValue(act_3_offense:7)} and {ItemValue(act_3_utility:6)}) or ({ItemValue(act_3_offense_bridge:4)} and {ItemValue(act_3_utility:8)}) or {ItemValue(act_3_utility_bridge:7)} or ({ItemValue(act_3_offense:7)} and {ItemValue(act_3_defense:6)} and {ItemValue(act_3_utility:6)}) or ({ItemValue(act_3_offense_bridge:5)} and {ItemValue(act_3_defense:5)} and {ItemValue(act_3_utility:5)}) or ({ItemValue(act_3_defense_bridge:5)} and {ItemValue(act_3_utility_bridge:6)}))")

    if act3 and consumable:
        addReq(region_table["Act III - Pre-Bridge"], "|@act3consumable:1|")
        addReq(region_table["Act III - Post-Bridge"], "|@act3consumable:2|")

    if kaycee:
        addReq(region_table["Kaycee's Mod - Pre-Prospector"], "{ItemValue(kaycees_mod_offense:1)} and (|Squirrel| or |Aquasquirrel|)")
        addReq(region_table["Kaycee's Mod - Post-Prospector"], "|@Kaycee's Mod:4| and (|Squirrel| or |Aquasquirrel|) and {ItemValue(kaycees_mod_offense:4)}")
        addReq(region_table["Kaycee's Mod - Post-Angler"], "({ItemValue(kaycees_mod_offense:6)} or ({ItemValue(kaycees_mod_offense:5)} and {ItemValue(kaycees_mod_defense:4)}) or ({ItemValue(kaycees_mod_offense:4)} and {ItemValue(kaycees_mod_utility:2)}) or ({ItemValue(kaycees_mod_offense:3)} and {ItemValue(kaycees_mod_defense:2)} and {ItemValue(kaycees_mod_utility:1)}))")
        addReq(region_table["Kaycee's Mod - Post-Trapper"], "({ItemValue(kaycees_mod_offense:7)} or ({ItemValue(kaycees_mod_offense:5)} and {ItemValue(kaycees_mod_defense:4)}) or ({ItemValue(kaycees_mod_offense:5)} and {ItemValue(kaycees_mod_utility:3)}) or ({ItemValue(kaycees_mod_offense:4)} and {ItemValue(kaycees_mod_defense:3)} and {ItemValue(kaycees_mod_utility:2)}))")
        addReq(region_table["Kaycee's Mod - End"], "({ItemValue(kaycees_mod_offense:8)} or ({ItemValue(kaycees_mod_offense:7)} and {ItemValue(kaycees_mod_defense:5)}) or ({ItemValue(kaycees_mod_offense:7)} and {ItemValue(kaycees_mod_utility:4)}) or ({ItemValue(kaycees_mod_offense:6)} and {ItemValue(kaycees_mod_defense:4)} and {ItemValue(kaycees_mod_utility:3)}))")

    if kaycee and consumable:
        addReq(region_table["Kaycee's Mod - Post-Prospector"], "|@kayceeconsumable:1|")
        addReq(region_table["Kaycee's Mod - Post-Angler"], "|@kayceeconsumable:3|")
        addReq(region_table["Kaycee's Mod - Post-Trapper"], "|@kayceeconsumable:5|")
        addReq(region_table["Kaycee's Mod - End"], "|@kayceeconsumable:6|")

    if kaycee and starter:
        addReq(region_table["Kaycee's Mod - Vanilla Deck"], "|Vanilla Deck|")
        addReq(region_table["Kaycee's Mod - High Cost Deck"], "|High Cost Deck|")
        addReq(region_table["Kaycee's Mod - Ant Deck"], "|Ant Deck|")
        addReq(region_table["Kaycee's Mod - Mantis God Deck"], "|Mantis God Deck|")
        addReq(region_table["Kaycee's Mod - Waterborne Deck"], "|Waterborne Deck|")
        addReq(region_table["Kaycee's Mod - Bone Deck"], "|Bone Deck|")
        addReq(region_table["Kaycee's Mod - No Cost Deck"], "|No Cost Deck|")
        addReq(region_table["Kaycee's Mod - Curious Egg Deck"], "|Curious Egg Deck|")

    if act2 and deck >= 1 and stack == 0:
        addReq(region_table["Act II - Prospector"], "{enoughDeckSize(3)} or ({enoughDeckSize(2)} and {test()}) or {test()}")
        addReq(region_table["Act II - Sawyer"], "{enoughDeckSize(4)} or ({enoughDeckSize(3)} and {act_two_power(5)}) or {act_two_power(6)}")
        addReq(region_table["Act II - Royal"], "{enoughDeckSize(5)} or ({enoughDeckSize(4)} and {act_two_power(6)}) or {act_two_power(7)}")
        addReq(region_table["Act II - Angler"], "{enoughDeckSize(5)} or ({enoughDeckSize(4)} and {act_two_power(6)}) or {act_two_power(7)}")
        addReq(region_table["Act II - Trapper"], "{enoughDeckSize(6)} or ({enoughDeckSize(5)} and {act_two_power(7)}) or {act_two_power(8)}")
        addReq(region_table["Act II - Leshy"], "{enoughDeckSize(7)} or ({enoughDeckSize(6)} and {act_two_power(8)}) or {act_two_power(9)}")
        addReq(region_table["Act II - Grimora"], "{enoughDeckSize(7)} or ({enoughDeckSize(6)} and {act_two_power(4)}) or {act_two_power(9)}")
        addReq(region_table["Act II - P03"], "{enoughDeckSize(8)} or ({enoughDeckSize(7)} and {act_two_power(9)}) or {act_two_power(10)}")
        addReq(region_table["Act II - Magnificus"], "{enoughDeckSize(8)} or ({enoughDeckSize(7)} and {act_two_power(9)}) or {act_two_power(10)}")

    elif act2 and stack >= 1 and deck == 0:
        addReq(region_table["Act II - Prospector"], "{enoughStackSize(1)} or {test()}")
        addReq(region_table["Act II - Royal"], "{enoughStackSize(1)} or {act_two_power(6)}")
        addReq(region_table["Act II - Angler"], "{enoughStackSize(1)} or {act_two_power(6)}")
        addReq(region_table["Act II - Trapper"], "{enoughStackSize(2)} or {act_two_power(7)}")
        addReq(region_table["Act II - Leshy"], "{enoughStackSize(3)} or {act_two_power(8)}")
        addReq(region_table["Act II - Grimora"], "{enoughStackSize(3)} or {act_two_power(8)}")
        addReq(region_table["Act II - P03"], "{enoughStackSize(4)} or {act_two_power(9)}")
        addReq(region_table["Act II - Magnificus"], "{enoughStackSize(4)} or {act_two_power(9)}")

    elif act2 and stack >= 1 and deck >= 1:
        addReq(region_table["Act II - Prospector"], "{enoughDeckSize(3)} or ({enoughDeckSize(2)} and {test()}) or {test()}")
        addReq(region_table["Act II - Sawyer"], "({enoughDeckSize(4)} and {enoughStackSize(1)}) or ({enoughDeckSize(3)} and {enoughStackSize(1)} and {act_two_power(5)}) or {act_two_power(6)}")
        addReq(region_table["Act II - Royal"], "({enoughDeckSize(5)} and {enoughStackSize(1)}) or ({enoughDeckSize(4)} and {enoughStackSize(1)} and {act_two_power(6)}) or {act_two_power(7)}")
        addReq(region_table["Act II - Angler"], "({enoughDeckSize(5)} and {enoughStackSize(1)}) or ({enoughDeckSize(4)} and {enoughStackSize(1)} and {act_two_power(6)}) or {act_two_power(7)}")
        addReq(region_table["Act II - Trapper"], "({enoughDeckSize(6)} and {enoughStackSize(2)}) or ({enoughDeckSize(5)} and {enoughStackSize(1)} and {act_two_power(7)}) or {act_two_power(8)}")
        addReq(region_table["Act II - Leshy"], "({enoughDeckSize(7)} and {enoughStackSize(3)}) or ({enoughDeckSize(6)} and {enoughStackSize(2)} and {act_two_power(8)}) or {act_two_power(9)}")
        addReq(region_table["Act II - Grimora"], "({enoughDeckSize(7)} and {enoughStackSize(3)}) or ({enoughDeckSize(6)} and {enoughStackSize(2)} and {act_two_power(4)}) or {act_two_power(9)}")
        addReq(region_table["Act II - P03"], "({enoughDeckSize(8)} and {enoughStackSize(4)}) or ({enoughDeckSize(7)} and {enoughStackSize(3)} and {act_two_power(9)}) or {act_two_power(10)}")
        addReq(region_table["Act II - Magnificus"], "({enoughDeckSize(8)} and {enoughStackSize(4)}) or ({enoughDeckSize(7)} and {enoughStackSize(3)} and {act_two_power(9)}) or {act_two_power(10)}")

    if act1 and not act2 and not act3 and not kaycee: #1
        addReq(region_table["Act I - Skip"], "|@Act I:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act I:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act I:ALL|")

    elif not act1 and act2 and not act3 and not kaycee: #2
        addReq(region_table["Act I - Beginning"], "|@Act II:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act II:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act II:ALL|")

    elif not act1 and not act2 and act3 and not kaycee: #3
        addReq(region_table["Act I - Beginning"], "|@Act III:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act III:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act III:ALL|")

    elif not act1 and not act2 and not act3 and kaycee: #k
        addReq(region_table["Act I - Beginning"], "|@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Kaycee's Mod:ALL|")

    elif act1 and act2 and not act3 and not kaycee: #12
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Act II:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act I:ALL| and |@Act II:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act I:ALL| and |@Act II:ALL|")

    elif act1 and not act2 and act3 and not kaycee: #13
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Act III:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act I:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act I:ALL| and |@Act III:ALL|")

    elif act1 and not act2 and not act3 and kaycee: #1k
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act I:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act I:ALL| and |@Kaycee's Mod:ALL|")

    elif not act1 and act2 and act3 and not kaycee: #23
        addReq(region_table["Act I - Beginning"], "|@Act II:ALL| and |@Act III:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act II:ALL| and |@Act III:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act II:ALL| and |@Act III:ALL|")

    elif not act1 and act2 and not act3 and kaycee: #2k
        addReq(region_table["Act I - Beginning"], "|@Act II:ALL| and |@Act III:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act II:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act II:ALL| and |@Act III:ALL|")

    elif not act1 and not act2 and act3 and kaycee: #3k
        addReq(region_table["Act I - Beginning"], "|@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act III:ALL| and |@Kaycee's Mod:ALL|")

    elif act1 and act2 and act3 and not kaycee: #123
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL|")

    elif act1 and act2 and not act3 and kaycee: #12k
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act I:ALL| and |@Act II:ALL| and |@Kaycee's Mod:ALL|")

    elif act1 and not act2 and act3 and kaycee: #13k
        addReq(region_table["Act I - Beginning"], "|@Act I:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act I:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Beginning"], "|@Act I:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")

    elif not act1 and act2 and act3 and kaycee: #23k
        addReq(region_table["Act I - Beginning"], "|@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Beginning"], "|@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")

    elif act1 and act2 and act3 and kaycee: #123k
        addReq(region_table["Act I - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act II - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")
        addReq(region_table["Act III - Skip"], "|@Act I:ALL| and |@Act II:ALL| and |@Act III:ALL| and |@Kaycee's Mod:ALL|")

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass
