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

from worlds.generic.Rules import set_rule

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



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    act1 = is_option_enabled(multiworld, player, "act_1_enabled")
    act2 = is_option_enabled(multiworld, player, "act_2_enabled")
    act3 = is_option_enabled(multiworld, player, "act_3_enabled")
    kaycee = is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    consumable = is_option_enabled(multiworld, player, "consumable_rando_Enabled")
    act1dupe = is_option_enabled(multiworld, player, "act_1_duplicate_locations")
    act2dupe = is_option_enabled(multiworld, player, "act_2_duplicate_locations")
    bucks = is_option_enabled(multiworld, player, "robobucks_locations")
    choice = is_option_enabled(multiworld, player, "card_choice_locations")
    unique = is_option_enabled(multiworld, player, "unique_card_locations")
    kayceedupe = is_option_enabled(multiworld, player, "kaycees_mod_duplicate_locations")
    challenge = is_option_enabled(multiworld, player, "kaycees_mod_challenge_locations")
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
        elif "Consumable" in location.get("category", []) and not consumable:
            locationNamesToRemove.append(location["name"])
        elif "actonesecond" in location.get("category", []) and not act1dupe:
            locationNamesToRemove.append(location["name"])
        elif "acttwosecond" in location.get("category", []) and not act2dupe:
            locationNamesToRemove.append(location["name"])
        elif "robobucks" in location.get("category", []) and not bucks:
            locationNamesToRemove.append(location["name"])
        elif "cardchoice" in location.get("category", []) and not choice:
            locationNamesToRemove.append(location["name"])
        elif "uniquecard" in location.get("category", []) and not unique:
            locationNamesToRemove.append(location["name"])
        elif "kayceesecond" in location.get("category", []) and not kayceedupe:
            locationNamesToRemove.append(location["name"])
        elif "Challenges" in location.get("category", []) and not challenge:
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
    act1 = is_option_enabled(multiworld, player, "act_1_enabled")
    act3 = is_option_enabled(multiworld, player, "act_3_enabled")
    kaycee = is_option_enabled(multiworld, player, "kaycees_mod_enabled")

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

    if not act1 and kaycee:
        start_item_list = ["Aquasquirrel"]
        for item_name in start_item_list:
            item = next(i for i in item_pool if i.name == item_name)
            multiworld.push_precollected(item)
            item_pool.remove(item)
    

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    stack = 20 - get_option_value(multiworld, player, "stack_size_rando")
    deck = get_option_value(multiworld, player, "deck_size_rando") - 20
    act2 = is_option_enabled(multiworld, player, "act_2_enabled")

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
    act1 = is_option_enabled(multiworld, player, "act_1_enabled")
    act2 = is_option_enabled(multiworld, player, "act_2_enabled")
    act3 = is_option_enabled(multiworld, player, "act_3_enabled")
    kaycee = is_option_enabled(multiworld, player, "kaycees_mod_enabled")
    consumable = is_option_enabled(multiworld, player, "consumable_rando_Enabled")
    hammer = is_option_enabled(multiworld, player, "hammer_rando_Enabled")
    stack = 20 - get_option_value(multiworld, player, "stack_size_rando")
    deck = get_option_value(multiworld, player, "deck_size_rando") - 20
    vessel = is_option_enabled(multiworld, player, "hammer_rando_Enabled")

    def late_woodlands(state: CollectionState):
        return state.has("Squirrel", player, 1) and state.has_group("act1damage", player, 2)

    def dagger(state:CollectionState):
        return state.has("Caged Wolf", player, 1)

    def prospector(state:CollectionState):
        return state.has_group("act1damage", player, 3) or (state.has_group("act1damage", player, 2) and state.has_group("act1other", player, 1))

    def late_wetlands(state:CollectionState):
        return state.has_group("act1damage", player, 4) or (state.has_group("act1damage", player, 3) and state.has_group("act1other", player, 1))

    def angler(state:CollectionState):
        if consumable:
            return state.has_group("act1consumable", player, 3) and (state.has_group("act1damage", player, 5) or (state.has_group("act1damage", player, 4) and state.has_group("act1other", player, 2)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1other", player, 2)) or (state.has_group("act1damage", player, 4) and state.has_group("act1otherrare", player, 1)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1otherrare", player, 1)))
        else:
            return state.has_group("act1damage", player, 5) or (state.has_group("act1damage", player, 4) and state.has_group("act1other", player, 2)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1other", player, 2)) or (state.has_group("act1damage", player, 4) and state.has_group("act1otherrare", player, 1)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1otherrare", player, 1))

    def late_snow_line(state:CollectionState):
        return state.has_group("act1damage", player, 6) or (state.has_group("act1damage", player, 5) and state.has_group("act1other", player, 3)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1other", player, 3)) or (state.has_group("act1damage", player, 5) and state.has_group("act1otherrare", player, 1)) or (state.has_group("act1damagerare", player, 2) and state.has_group("act1otherrare", player, 1))

    def trapper(state:CollectionState):
        if consumable:
            return state.has_group("act1consumable", player, 5) and (state.has_group("act1damage", player, 7) or (state.has_group("act1damage", player, 6) and state.has_group("act1other", player, 3)) or (state.has_group("act1damagerare", player, 3) and state.has_group("act1other", player, 3)) or (state.has_group("act1damage", player, 6) and state.has_group("act1otherrare", player, 1)) or (state.has_group("act1damagerare", player, 3) and state.has_group("act1otherrare", player, 1)))
        else:
            return state.has_group("act1damage", player, 7) or (state.has_group("act1damage", player, 6) and state.has_group("act1other", player, 3)) or (state.has_group("act1damagerare", player, 3) and state.has_group("act1other", player, 3)) or (state.has_group("act1damage", player, 6) and state.has_group("act1otherrare", player, 1)) or (state.has_group("act1damagerare", player, 3) and state.has_group("act1otherrare", player, 1))

    def leshy(state:CollectionState):
        return state.has_group("act1damage", player, 8) or (state.has_group("act1damage", player, 7) and state.has_group("act1other", player, 4)) or (state.has_group("act1damagerare", player, 4) and state.has_group("act1other", player, 4)) or (state.has_group("act1damage", player, 7) and state.has_group("act1otherrare", player, 2)) or (state.has_group("act1damagerare", player, 4) and state.has_group("act1otherrare", player, 2))

    def end(state:CollectionState):
        if consumable:
            return state.has_all(["Caged Wolf", "Special Dagger"], player)
        elif act1:
            return state.has("Caged Wolf", player, 1)
        return True

    def eye(state:CollectionState):
        if consumable:
            return state.has("Special Dagger", player, 1)
        return True
    
    def act2blood(state:CollectionState, count:int):
        return (state.has_any(["Squirrel", "Skeleton"], player) or act2energy(state,count*1.4)) and state.has_group("act2damageblood", player, count*0.7) and state.has_group("act2otherblood", player, count*0.3) and (state.has_group("act2damagebloodrare", player, count*0.3) or state.has("Mole Man", player, 1) or (state.has_group("act2damageblood", player, count*1) and state.has_group("act2otherblood", player, count*0.6)))
    
    def act2bones(state:CollectionState, count:int):
        return (state.has("Skeleton", player, 1) or act2blood(state,count*1.3)) and state.has_group("act2damagebones", player, count*0.7) and state.has_group("act2otherbones", player, count*0.4) and (state.has_group("act2damagebonesrare", player, count*0.3) or state.has("Tomb Robber", player, 1) or (state.has_group("act2damagebones", player, count*1) and state.has_group("act2otherbones", player, count*0.6)))
    
    def act2energy(state:CollectionState, count:int):
        return state.has_group("act2damageenergy", player, count*0.8) and state.has_group("act2otherenergy", player, count*0.5) and (state.has_any(["Mrs. Bomb", "Shutterbug", "Curve Hopper"], player) or state.has_group("act2otherenergyrare", player, count*0.2) or state.has_group("act2damagehighenergyrare", player, count*0.2) or state.has_group("act2damagehighenergy", player, count*0.7) or (state.has_group("act2damageenergy", player, count*1.2) and state.has_group("act2otherenergy", player, count*0.8)))
    
    def act2blue(state:CollectionState, count:int):
        return state.has("Sapphire Mox", player, 1) and state.has_group("act2damageblue", player, count/2) and state.has_group("act2otherblue", player, count*0.3)
    
    def act2orange(state:CollectionState, count:int):
        return state.has("Ruby Mox", player, 1) and (state.has_group("act2damageorange", player, count*0.9) or (state.has("Practice Wizard", player, 1) and state.has_group("act2damageorange", player, count*0.8)))
    
    def act2green(state:CollectionState, count:int):
        return state.has("Emerald Mox", player, 1) and state.has_group("act2damagegreen", player, count*0.9)
    
    def act2magick(state:CollectionState, count:int):
        return act2blue(state,count) or act2orange(state,count) or act2green(state,count) or (act2blue(state,count*0.8) and act2orange(state,count*0.8)) or (act2blue(state,count*0.8) and act2green(state,count*0.8)) or (act2green(state,count*0.8) and act2orange(state,count*0.8)) or (act2blue(state,count*0.6) and act2orange(state,count*0.6) and act2green(state,count*0.6))
    
    def act2single(state:CollectionState, count:int):
        return act2blood(state,count*1.1) or act2bones(state,count*1.1) or act2energy(state,count*1.1) or act2magick(state,count*1.1)
    
    def act2double(state: CollectionState, count:int):
        return (act2blood(state,count*0.8) and act2bones(state,count*0.8)) or (act2blood(state,count*0.8) and act2energy(state,count*0.8)) or (act2blood(state,count*0.8) and act2magick(state,count*0.8)) or (act2bones(state,count*0.8) and act2energy(state,count*0.8)) or (act2energy(state,count*0.8) and act2magick(state,count*0.8))
    
    def act2triple(state:CollectionState, count:int):
        return (act2blood(state,count*0.6) and act2bones(state,count*0.6) and act2energy(state,count - 2)) or (act2blood(state,count*0.6) and act2bones(state,count*0.6) and act2magick(state,count*0.6)) or (act2blood(state,count*0.6) and act2energy(state,count*0.6) and act2magick(state,count*0.6)) or (act2bones(state,count*0.6) and act2energy(state,count*0.6) and act2magick(state,count*0.6))
    
    def act2quad(state:CollectionState, count:int):
        return (act2blood(state,count*0.4) and act2bones(state,count*0.4) and act2energy(state,count*0.4) and act2magick(state,count*0.4))
    
    def act2power(state:CollectionState, count:int):
        return act2single(state, count) or act2double(state, count) or act2triple(state, count) or act2quad(state, count)
        
    def act2powerDeck(state:CollectionState, count:int):
        return act2power(state,count+2) or (act2power(state,count) and deckCheck(state,(count+1)/2))
        
    def act2powerStack(state:CollectionState, count:int):
        return act2power(state,count+1) or (act2power(state,count) and stackCheck(state,(count-1)/2))
        
    def act2powerStackDeck(state:CollectionState, count:int):
        return act2power(state,count+3) or (act2power(state,count) and stackCheck(state,(count-1)/2) and deckCheck(state,(count+1)/2))
        
    def act2powerTotal(state:CollectionState, count:int):
        if hammer:
            if stack > 1 and deck > 1:
                return act2powerStackDeck(state,count+1) or (act2powerStackDeck(state,count) and state.has("Hammer", player, 1))
            elif stack > 1:
                return act2powerStack(state,count+1) or (act2powerStack(state,count) and state.has("Hammer", player, 1))
            elif deck > 1:
                return act2powerDeck(state,count+1) or (act2powerDeck(state,count) and state.has("Hammer", player, 1))
            else: return act2power(state,count+1) or (act2power(state,count) and state.has("Hammer", player, 1))
        else:
            if stack > 1 and deck > 1:
                return act2powerStackDeck(state,count)
            elif stack > 1:
                return act2powerStack(state,count)
            elif deck > 1:
                return act2powerDeck(state,count)
            else: return act2power(state,count)

    def deckCheck(state:CollectionState, req:int):
        return state.count("-1 Min Deck Size", player) + 15-deck > req

    def stackCheck(state:CollectionState, req:int):
        return state.count("+1 Max Card Stack Size", player) + 15-stack > req

    def prospector2(state:CollectionState):
        return act2powerTotal(state,3)

    def kaycee2(state:CollectionState):
        return act2powerTotal(state,2)

    def sawyer2(state:CollectionState):
        return act2powerTotal(state,4)

    def royal2(state:CollectionState):
        return act2powerTotal(state,5)

    def angler2(state:CollectionState):
        return act2powerTotal(state,5)

    def trapper2(state:CollectionState):
        return act2powerTotal(state,6)

    def leshy2(state:CollectionState):
        return act2powerTotal(state,9) or (act2powerTotal(state,7) and state.has("Amalgam", player, 1))

    def grimora2(state:CollectionState):
        return act2powerTotal(state,8)

    def leftboss2(state:CollectionState):
        return act2powerTotal(state,9)
    
    def easternBotopia(state:CollectionState):
        return state.has("Empty Vessel", player, 1) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot"], player, 2) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer"], player, 1)
    
    def postEasternBotopia(state:CollectionState):
        if hammer:
            return ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot"], player, 3) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot"], player, 1) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot"], player, 4) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot"], player, 2)))
        else:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot"], player, 3) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot"], player, 1)
    
    def latePostEasternBotopia(state:CollectionState):
        if consumable and hammer:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Qui77", "Gr1zz", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3) and state.has_group("act3consumable", player, 1)
        elif consumable:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Qui77", "Gr1zz", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3) and state.has_group("act3consumable", player, 1)
        elif hammer:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Qui77", "Gr1zz", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3)
        else:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Qui77", "Gr1zz", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3)
        
    def eastboss3(state:CollectionState):
        if hammer:
            return (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4))
        else:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 3)
        
    def lateWesternBotopia(state:CollectionState):
        if consumable and hammer and vessel:
            return ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5))) and state.has("Vessel Upgrade", player, 1) and (state.has_group("act3consumable", player, 3) or (state.has("Hammer", player, 1) and state.has_group("act3consumable", player, 2)) or state.has("Vessel Upgrade", player, 2))
        elif hammer and consumable:
            return (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5)) and (state.has_group("act3consumable", player, 2) or state.has("Hammer", player, 1))
        elif hammer and vessel:
            return ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5))) and (state.has("Vessel Upgrade", player, 1) and state.has("Hammer", player, 1))
        elif consumable and vessel:
            return ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4))) and (state.has("Vessel Upgrade", player, 1) or state.has_group("act3consumable", player, 2))
        elif vessel:
            return (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4) and state.has("Vessel Upgrade", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 5))
        else:
            return state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 6) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher"], player, 4)
        
    def gaudyGemLand(state: CollectionState):
        if consumable:
            return (state.has_from_list(["Emerald Vessel", "Sapphire Vessel", "Ruby Vessel"], player, 1)) or (state.has_group("act3consumable", player, 3))
        return True
        
    def ricketyTower(state: CollectionState):
        if consumable:
            return state.has_from_list(["Emerald Vessel", "Sapphire Vessel", "Ruby Vessel"], player, 1)
        return True
    
    def g0lly(state:CollectionState):
        if consumable and hammer and vessel:
            return state.has("Act 3 Custom Card", player, 1) or (((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 8) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 6))) and state.has("Vessel Upgrade", player, 1) and (state.has_group("act3consumable", player, 3) or (state.has("Hammer", player, 1) and state.has_group("act3consumable", player, 2)) or state.has("Vessel Upgrade", player, 2)))
        elif hammer and consumable:
            return state.has("Act 3 Custom Card", player, 1) or ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 8) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 6)) and (state.has_group("act3consumable", player, 2) or state.has("Hammer", player, 1)))
        elif hammer and vessel:
            return state.has("Act 3 Custom Card", player, 1) or (((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5) and state.has("Hammer", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Ouroboros/Ourobot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 8) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 6))) and (state.has("Vessel Upgrade", player, 1) and state.has("Hammer", player, 1)))
        elif consumable and vessel:
            return state.has("Act 3 Custom Card", player, 1) or (((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5))) and (state.has("Vessel Upgrade", player, 1) or state.has_group("act3consumable", player, 2)))
        elif vessel:
            return state.has("Act 3 Custom Card", player, 1) or ((state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5) and state.has("Vessel Upgrade", player, 1)) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 8) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 6)))
        else:
            return state.has("Act 3 Custom Card", player, 1) or (state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "Bolthound", "Double Gunner", "Swapbot", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian", "Gembound Ripper", "Kind Cell", "Tough Cell", "Splinter Cell"], player, 7) and state.has_from_list(["49er", "Amoebot", "Explode Bot", "Alarm Bot", "Insectodrone", "Shieldbot", "Sniper Bot", "L33pB0t", "Sentry Drone", "Energy Bot", "Gift Bot", "Busted 3D Printer", "Lonely Wizbot", "Fishbot", "Son1a", "Bomb Latcher", "Exeskeleton", "Shield Latcher", "Skel-e-latcher", "Buff Conduit", "Gems Conduit", "Bleene's Vessel", "Goranj's Vessel", "Orlu's Vessel", "Gem Detonator", "Gem Guardian"], player, 5))

    def late_area1(state: CollectionState):
        return (state.has("Squirrel", player, 1) or state.has("Aquasquirrel", player, 1)) and state.has_group("kayceedamage", player, 3)

    def boss1(state:CollectionState):
        return state.has_group("kayceedamage", player, 4) or (state.has_group("kayceedamage", player, 3) and state.has_group("kayceeother", player, 2))

    def late_area2(state:CollectionState):
        return state.has_group("kayceedamage", player, 5) or (state.has_group("kayceedamage", player, 4) and state.has_group("kayceeother", player, 2))

    def boss2(state:CollectionState):
        if consumable:
            return state.has_group("kayceeconsumable", player, 3) and (state.has_group("kayceedamage", player, 7) or (state.has_group("kayceedamage", player, 5) and state.has_group("kayceeother", player, 3)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeother", player, 3)) or (state.has_group("kayceedamage", player, 5) and state.has_group("kayceeotherrare", player, 2)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeotherrare", player, 2)))
        else:
            return state.has_group("kayceedamage", player, 7) or (state.has_group("kayceedamage", player, 5) and state.has_group("kayceeother", player, 3)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeother", player, 3)) or (state.has_group("kayceedamage", player, 5) and state.has_group("kayceeotherrare", player, 2)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeotherrare", player, 2))

    def late_area3(state:CollectionState):
        return state.has_group("kayceedamage", player, 8) or (state.has_group("kayceedamage", player, 6) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamage", player, 6) and state.has_group("kayceeotherrare", player, 2)) or (state.has_group("kayceedamagerare", player, 3) and state.has_group("kayceeotherrare", player, 2))

    def boss3(state:CollectionState):
        if consumable:
            return state.has_group("kayceeconsumable", player, 6) and (state.has_group("kayceedamage", player, 9) or (state.has_group("kayceedamage", player, 7) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamagerare", player, 4) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamage", player, 7) and state.has_group("kayceeotherrare", player, 2)) or (state.has_group("kayceedamagerare", player, 4) and state.has_group("kayceeotherrare", player, 2)))
        else:
            return state.has_group("kayceedamage", player, 9) or (state.has_group("kayceedamage", player, 7) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamagerare", player, 4) and state.has_group("kayceeother", player, 4)) or (state.has_group("kayceedamage", player, 7) and state.has_group("kayceeotherrare", player, 2)) or (state.has_group("kayceedamagerare", player, 4) and state.has_group("kayceeotherrare", player, 2))

    def boss4(state:CollectionState):
        return state.has_group("kayceedamage", player, 11) or (state.has_group("kayceedamage", player, 8) and state.has_group("kayceeother", player, 5)) or (state.has_group("kayceedamagerare", player, 5) and state.has_group("kayceeother", player, 5)) or (state.has_group("kayceedamage", player, 8) and state.has_group("kayceeotherrare", player, 3)) or (state.has_group("kayceedamagerare", player, 5) and state.has_group("kayceeotherrare", player, 3))

    def boss5(state:CollectionState):
        return state.has_group("kayceedamage", player, 12) or (state.has_group("kayceedamage", player, 9) and state.has_group("kayceeother", player, 5)) or (state.has_group("kayceedamagerare", player, 5) and state.has_group("kayceeother", player, 5)) or (state.has_group("kayceedamage", player, 9) and state.has_group("kayceeotherrare", player, 3)) or (state.has_group("kayceedamagerare", player, 6) and state.has_group("kayceeotherrare", player, 3))

    def boss6(state:CollectionState):
        if consumable:
            return state.has_group("kayceeconsumable", player, 9) and (state.has_group("kayceedamage", player, 13) or (state.has_group("kayceedamage", player, 10) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamagerare", player, 6) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamage", player, 10) and state.has_group("kayceeotherrare", player, 3)) or (state.has_group("kayceedamagerare", player, 6) and state.has_group("kayceeotherrare", player, 3)))
        else:
            return state.has_group("kayceedamage", player, 13) or (state.has_group("kayceedamage", player, 10) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamagerare", player, 6) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamage", player, 10) and state.has_group("kayceeotherrare", player, 3)) or (state.has_group("kayceedamagerare", player, 6) and state.has_group("kayceeotherrare", player, 3))

    def boss7(state:CollectionState):
        return state.has_group("kayceedamage", player, 14) or (state.has_group("kayceedamage", player, 11) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamagerare", player, 7) and state.has_group("kayceeother", player, 6)) or (state.has_group("kayceedamage", player, 11) and state.has_group("kayceeotherrare", player, 3)) or (state.has_group("kayceedamagerare", player, 7) and state.has_group("kayceeotherrare", player, 3))

    if act1:
        for exit_obj in multiworld.get_region("Act I - Late Woodlands", player).entrances:
            set_rule(exit_obj, late_woodlands)
        for exit_obj in multiworld.get_region("Act I - Dagger", player).entrances:
            set_rule(exit_obj, dagger)
        for exit_obj in multiworld.get_region("Act I - Prospector", player).entrances:
            set_rule(exit_obj, prospector)
        for exit_obj in multiworld.get_region("Act I - Late Wetlands", player).entrances:
            set_rule(exit_obj, late_wetlands)
        for exit_obj in multiworld.get_region("Act I - Angler", player).entrances:
            set_rule(exit_obj, angler)
        for exit_obj in multiworld.get_region("Act I - Late Snow Line", player).entrances:
            set_rule(exit_obj, late_snow_line)
        for exit_obj in multiworld.get_region("Act I - Trapper", player).entrances:
            set_rule(exit_obj, trapper)
        for exit_obj in multiworld.get_region("Act I - Leshy", player).entrances:
            set_rule(exit_obj, leshy)
        for exit_obj in multiworld.get_region("Act I - End", player).entrances:
            set_rule(exit_obj, end)
        for exit_obj in multiworld.get_region("Act I - Eye", player).entrances:
            set_rule(exit_obj, eye)
        for exit_obj in multiworld.get_region("Act I - Late Woodlands", player).exits:
            set_rule(exit_obj, late_woodlands)
        for exit_obj in multiworld.get_region("Act I - Dagger", player).exits:
            set_rule(exit_obj, dagger)
        for exit_obj in multiworld.get_region("Act I - Prospector", player).exits:
            set_rule(exit_obj, prospector)
        for exit_obj in multiworld.get_region("Act I - Late Wetlands", player).exits:
            set_rule(exit_obj, late_wetlands)
        for exit_obj in multiworld.get_region("Act I - Angler", player).exits:
            set_rule(exit_obj, angler)
        for exit_obj in multiworld.get_region("Act I - Late Snow Line", player).exits:
            set_rule(exit_obj, late_snow_line)
        for exit_obj in multiworld.get_region("Act I - Trapper", player).exits:
            set_rule(exit_obj, trapper)
        for exit_obj in multiworld.get_region("Act I - Leshy", player).exits:
            set_rule(exit_obj, leshy)
        for exit_obj in multiworld.get_region("Act I - End", player).exits:
            set_rule(exit_obj, end)
        for exit_obj in multiworld.get_region("Act I - Eye", player).exits:
            set_rule(exit_obj, eye)

    if act2:
        for exit_obj in multiworld.get_region("Act II - Prospector", player).entrances:
            set_rule(exit_obj, prospector2)
        for exit_obj in multiworld.get_region("Act II - Kaycee", player).entrances:
            set_rule(exit_obj, kaycee2)
        for exit_obj in multiworld.get_region("Act II - Sawyer", player).entrances:
            set_rule(exit_obj, sawyer2)
        for exit_obj in multiworld.get_region("Act II - Royal", player).entrances:
            set_rule(exit_obj, royal2)
        for exit_obj in multiworld.get_region("Act II - Angler", player).entrances:
            set_rule(exit_obj, angler2)
        for exit_obj in multiworld.get_region("Act II - Trapper", player).entrances:
            set_rule(exit_obj, trapper2)
        for exit_obj in multiworld.get_region("Act II - Leshy", player).entrances:
            set_rule(exit_obj, leshy2)
        for exit_obj in multiworld.get_region("Act II - Grimora", player).entrances:
            set_rule(exit_obj, grimora2)
        for exit_obj in multiworld.get_region("Act II - P03", player).entrances:
            set_rule(exit_obj, leftboss2)
        for exit_obj in multiworld.get_region("Act II - Magnificus", player).entrances:
            set_rule(exit_obj, leftboss2)
        for exit_obj in multiworld.get_region("Act II - Prospector", player).exits:
            set_rule(exit_obj, prospector2)
        for exit_obj in multiworld.get_region("Act II - Kaycee", player).exits:
            set_rule(exit_obj, kaycee2)
        for exit_obj in multiworld.get_region("Act II - Sawyer", player).exits:
            set_rule(exit_obj, sawyer2)
        for exit_obj in multiworld.get_region("Act II - Royal", player).exits:
            set_rule(exit_obj, royal2)
        for exit_obj in multiworld.get_region("Act II - Angler", player).exits:
            set_rule(exit_obj, angler2)
        for exit_obj in multiworld.get_region("Act II - Trapper", player).exits:
            set_rule(exit_obj, trapper2)
        for exit_obj in multiworld.get_region("Act II - Leshy", player).exits:
            set_rule(exit_obj, leshy2)
        for exit_obj in multiworld.get_region("Act II - Grimora", player).exits:
            set_rule(exit_obj, grimora2)
        for exit_obj in multiworld.get_region("Act II - P03", player).exits:
            set_rule(exit_obj, leftboss2)
        for exit_obj in multiworld.get_region("Act II - Magnificus", player).exits:
            set_rule(exit_obj, leftboss2)

    if act3:
        for exit_obj in multiworld.get_region("Act III - Eastern Botopia", player).entrances:
            set_rule(exit_obj, easternBotopia)
        for exit_obj in multiworld.get_region("Act III - Filthy Corpse World", player).entrances:
            set_rule(exit_obj, postEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Late Filthy Corpse World", player).entrances:
            set_rule(exit_obj, latePostEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Archivist", player).entrances:
            set_rule(exit_obj, eastboss3)
        for exit_obj in multiworld.get_region("Act III - Foul Backwater", player).entrances:
            set_rule(exit_obj, postEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Late Foul Backwater", player).entrances:
            set_rule(exit_obj, latePostEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Photographer", player).entrances:
            set_rule(exit_obj, eastboss3)
        for exit_obj in multiworld.get_region("Act III - Late Western Botopia", player).entrances:
            set_rule(exit_obj, lateWesternBotopia)
        for exit_obj in multiworld.get_region("Act III - Gaudy Gem Land", player).entrances:
            set_rule(exit_obj, gaudyGemLand)
        for exit_obj in multiworld.get_region("Act III - Rickety Tower", player).entrances:
            set_rule(exit_obj, ricketyTower)
        for exit_obj in multiworld.get_region("Act III - G0lly", player).entrances:
            set_rule(exit_obj, g0lly)
        for exit_obj in multiworld.get_region("Act III - Eastern Botopia", player).exits:
            set_rule(exit_obj, easternBotopia)
        for exit_obj in multiworld.get_region("Act III - Filthy Corpse World", player).exits:
            set_rule(exit_obj, postEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Late Filthy Corpse World", player).exits:
            set_rule(exit_obj, latePostEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Archivist", player).exits:
            set_rule(exit_obj, eastboss3)
        for exit_obj in multiworld.get_region("Act III - Foul Backwater", player).exits:
            set_rule(exit_obj, postEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Late Foul Backwater", player).exits:
            set_rule(exit_obj, latePostEasternBotopia)
        for exit_obj in multiworld.get_region("Act III - Photographer", player).exits:
            set_rule(exit_obj, eastboss3)
        for exit_obj in multiworld.get_region("Act III - Late Western Botopia", player).exits:
            set_rule(exit_obj, lateWesternBotopia)
        for exit_obj in multiworld.get_region("Act III - Gaudy Gem Land", player).exits:
            set_rule(exit_obj, gaudyGemLand)
        for exit_obj in multiworld.get_region("Act III - Rickety Tower", player).exits:
            set_rule(exit_obj, ricketyTower)
        for exit_obj in multiworld.get_region("Act III - G0lly", player).exits:
            set_rule(exit_obj, g0lly)

    if kaycee:
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late First Area", player).entrances:
            set_rule(exit_obj, late_area1)
        for exit_obj in multiworld.get_region("Kaycee's Mod - First Boss", player).entrances:
            set_rule(exit_obj, boss1)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late Second Area", player).entrances:
            set_rule(exit_obj, late_area2)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Second Boss", player).entrances:
            set_rule(exit_obj, boss2)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late Third Area", player).entrances:
            set_rule(exit_obj, late_area3)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Third Boss", player).entrances:
            set_rule(exit_obj, boss3)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Final Boss", player).entrances:
            set_rule(exit_obj, boss4)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Fifth Boss", player).entrances:
            set_rule(exit_obj, boss5)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Sixth Boss", player).entrances:
            set_rule(exit_obj, boss6)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Seventh Boss", player).entrances:
            set_rule(exit_obj, boss7)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late First Area", player).exits:
            set_rule(exit_obj, late_area1)
        for exit_obj in multiworld.get_region("Kaycee's Mod - First Boss", player).exits:
            set_rule(exit_obj, boss1)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late Second Area", player).exits:
            set_rule(exit_obj, late_area2)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Second Boss", player).exits:
            set_rule(exit_obj, boss2)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Late Third Area", player).exits:
            set_rule(exit_obj, late_area3)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Third Boss", player).exits:
            set_rule(exit_obj, boss3)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Final Boss", player).exits:
            set_rule(exit_obj, boss4)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Fifth Boss", player).exits:
            set_rule(exit_obj, boss5)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Sixth Boss", player).exits:
            set_rule(exit_obj, boss6)
        for exit_obj in multiworld.get_region("Kaycee's Mod - Seventh Boss", player).exits:
            set_rule(exit_obj, boss7)

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

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
