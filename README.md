# Inscryption Manual Randomizer Guide

This is my take on the Inscryption randomizer! There's 3 rules: 
1. If you haven't received the item for a card, you aren't allowed to play it.
2. You also can't use a card that has a *soul* of a card you're not allowed to play (In the sacrifice altar)
3. Cards that can be played without being "played" (Corpse Maggots, Pelt Lice, Ijiraq) cannot be added to your deck until you have the item for them.

## Where is the settings page?

The .yaml file is included with the GitHub release.

## How do the acts work?

There are 4 "acts" in this randomizer: Act I, Act II, Act III, and Kaycee's Mod, in that order.
If you have every act enabled, you can only access Act II after beating Act I, you can only access Act III after beating Act II, and you can only access Kaycee's Mod after beating Act III
You can disable whatever act you wish, so for instance if you only have Act I and Act III enabled, you beat Act I, and then move on to Act III, and once you beat that, you've beaten your goal.
Disabled acts will remove all locations in them, and if an item isn't in any enabled acts, it will be removed as well.
You start Act I at the second option in chapter select; skip the intro.
For Act III, completely ignore all of this randomizer's restrictions until you reach the first waypoint (right before the shop.)

## What are the items?

By default, the items are just Cards, which means you can't play a card until you receive the item for it.
Note that some cards exist in multiple acts, so if you get the "Wolf Cub" item, you can play it in Act I, Act II, and Kaycee's Mod.
The filler item is "Ignore a Restriction Once", which lets you play a banned card, use a banned consumable, use a hammer when you're not supposed to, etc. You can't use it to get vessel upgrades or ignore deck size or stack size limits, though.

There are additional items that can be enabled:

- Consumable Rando: (Act I, III, and Kaycee's Mod only) You cannot play a consumable item until you receive the Archipelago Item for it.
- Hammer Rando: (Act II and III only) You cannot use the hammer until you receive the Archipelago Item for it.
- Clover Rando: (Act I and II only) You cannot use the clover until you receive the Archipelago Item for it.
- Stack Size Rando: (Act II only) This option has a value from 5 to 20, creating up to 15 "+1 Max Card Stack Size" items when using the minimum of 5.
  - With this option, you can only have up to the yaml option of the same card in your deck, which is alleviated by "+1 Max Card Stack Size" items
  - For instance, if you selected 8, you cannot have more than 8 Squirrels in your deck, but if you receive 3 "+1 Max Card Stack Size" items, you can have up to 11 Squirrels.
  - If you set this option to 20, this restriction is removed.
- Deck Size Rando: (Act II only) This option has a value from 20 to 35, creating up to 15 "-1 Min Deck Size" items when using the maximum of 35.
  - With this option, you can must have a minimum of the yaml option of cards in your deck, which is alleviated by "-1 Min Deck Size" items
  - For instance, if you selected 27, you must have 27 cards in your deck, but if you receive 3 "-1 Min Deck Size" items, you can have 24 cards instead.
  - If you set this option to 20, this restriction is removed.
- Vessel Upgrade Rando: (Act III only) This option creates 3 "Vessel Upgrade" items, and 1 "Conduit Upgrade" item.
  - You cannot pick up a Vessel Upgrade (from Uberbots) until you get a Vessel Upgrade item. You can only pick up as many as you have Archipelago Items for, so if you have 2 items, you'll have to ignore the third one once you beat the third Uberbot.
  - You can't pick up the Conduit Upgrade (immediately after entering Resplendent Bastion) until you get the item for it.
- Filler Traps: Replace a percentage of "Ignore a Restriction Once" filler with "Bell Trap" traps, which force you to ring the bell as soon as possible once you receive them.

## What are the locations?

By default, there are locations for progressing through the acts. They are as follows:

- In Act I, there are locations for progressing forward on the map, and doing things around the Cabin.
- In Act II, there are locations for gaining Card Packs, progressing the story, and beating enemies.
- In Act III, there are locations for interacting with nodes and beating encounters, and doing things around the Factory.
- In Kaycee's Mod, there are locations for progressing forward on the map, and beating bosses with each challenge enabled.

By default, there are duplicates of each location in Act I, Act II, and Kaycee's Mod. You can disable them by act, but if you test generate and it says that it's removing items since you have more items than locations, consider enabling some of them.
You can disable specific types of Act III locations (specifically: Robobucks Locations, Card Choice Locations, and Unique Card Locations.)
You can disable the Challenge Locations with Kaycee's Mod.
If you're playing just one act, you should enable every location option associated with that act (else you'll have too few locations.)

## What is the goal of Inscryption when randomized?

7 Different Goals to choose from:

- End of Act I
- End of Act II
- End of Act III
- End of Kaycee's Mod
- End of Kaycee's Mod (50 Challenge Points)
- End of Kaycee's Mod (80 Challenge Points)
- End of Kaycee's Mod (110 Challenge Points)

Make sure to set you goal as the last enabled act.
If you're going for every act, it may be wise to choose one of the goals with Challenge Points, since by then you'll have a lot of Kaycee's mod cards.

## Required Software

- Inscryption
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Installation Procedures

Make sure a copy of the Manual world is in the lib/world directory of your client-side installation.
If you include Kaycee's Mod in your settings, either have a save file with everything unlocked in Kaycee's Mod, or use the [Unlock All Mod](https://thunderstore.io/c/inscryption/p/IngoH/Unlock_All/) on the Thunderstore Mod Manager.
If you don't have a save with everything unlocked in the base game, you can press Alt + K + C + M to unlock chapter select.

## Joining a MultiWorld Game

1. Launch the launcher.
2. Click on Manual client on the right.
3. At the top enter your server's ip with the port provided (by default archipelago.gg:38281).
4. In Manual Game ID put "Manual_Inscryption_mp3" then press the Connect button on the top right.
5. In the command field at the bottom enter the name of your slot you chose in your Player.yaml then press enter

## Manual Client

In the "Manual" tab you'll find buttons corresponding with all the available locations in the Randomizer. Since this is a manual game its built on trust™ you press the locations when you get to them, hopefully in the future only what you can access will be visible but at the moment you could press victory and it would accept it. Also, if you have death_link enabled, there's a button at the top right to trigger and receive death links.

## How does the Inscryption Don't Starve apworld work?

**Note: this is no longer being updated. You can find it in older releases of this, but its logic is broken in a lot of ways, and its design is heavily flawed.**

You need to use the latest version of my [DontStarveExpansion mod](https://thunderstore.io/c/inscryption/p/empathymp3/DontStarveExpansion/).
You need to use the alternate apworlds and yaml files. (with `DontStarve` in the name).
There are a few differences from the original rando:
- Play on Kaycee's Mod.
- Disable the vanilla card pack, and enable the Don't Starve card pack.
- Put "Manual_InscryptionDontStarve_mp3" in the manual client.
- Don't use the aquasquirrel challenge.
- In the side deck selection screen, you should use the gem deer side deck that costs energy, until you get the "You No Longer Have To Use The Gem Deer Side Decks That Cost Energy" item, at which point you should use the gem deer side deck that doesn't cost energy. After you select either of those, you can choose your gem colors.
- There are no cards that fly onto the board, so you don't have to be concerned about those.
- Otherwise, it's like Kaycee's Mod, but with different cards.