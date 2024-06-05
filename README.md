# Inscryption Manual Randomizer Guide

**Note: This fails generation about half the time when you play with more than one act. If I can figure out why it doesn't generate sometimes, I'll try to fix it.**

This is my take on the Inscryption randomizer! There's 3 rules: 
1. If you haven't received the item for a card, you aren't allowed to play it.
2. You also can't use a card that has a *soul* of a card you're not allowed to play (In the sacrifice altar)
3. Cards that can be played without being "played" (Corpse Maggots, Pelt Lice, Ijiraq) cannot be added to your deck until you have the item for them (and thus the corresponding checks are locked behind those).

However, you can play Stoat in the first Act I tutorial battle, and no other place (until you get the item).

## Where is the settings page?

The .yaml file is included with the GitHub release.

## What does randomization do to this game?

Every time you add a card to your deck (or side deck, like Squirrel), you get a check. You can receive those items that allow you to play a card.
If you start with a certain card in your deck, you can get the check immediately.
Cards that are only given to you (Bee, Boulder, Frozen Opossum, The Smoke, Greater Smoke, Good Fish, More Fish, Bad Fish, Captive File, and Hydra (and Amalgam if Act I is disabled)) have their locations whenever you obtain them in a fight.
There are unique items and locations for each pre-made deathcard (e.g., Kaycee, Kaminski, etc.), and also an item and location for Custom Deathcards.
There are also locations for the bosses that appear in each act (mostly because there are too few locations in this otherwise).
Cards that appear in multiple acts have one associated item and one associated location, even if they're vastly different in different acts.

## What's up with the weird .yaml settings?

The way this randomizer works, is you start in Act I, then go to Act II, then go to Act III, then go to Kaycee's Mod. (always this order)
But you can disable acts (since playing both Act I and Kaycee's Mod is probably unnecessary), which will allow you to skip from Act I to Act III for example.
Since there is overlap between cards in acts, there are other settings corresponding to multiple acts, but you can ignore them. The triggers in the template yaml will deal with them (unless you mess with those triggers).

Also, make sure to check off the location that tells you to immediately check it off, when you've begun.

If you want to mess around with the triggers, (which you shouldn't), you just need to enable every setting that has one of the acts you're playing in the name.

## What is the goal of Inscryption when randomized?

4 Different Goals to choose from:

- End of Act I
- End of Act II
- End of Act III
- End of Kaycee's Mod

Don't choose a goal that includes an act you're not going to play.

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
4. In Manual Game ID put "Manual_Inscryption_empathymp3" then press the Connect button on the top right.
5. In the command field at the bottom enter the name of your slot you chose in your Player.yaml then press enter

## Manual Client

In the "Tracker and Locations" tab you'll find buttons corresponding with all the available locations in the Randomizer. Since this is a manual game its built on trust™ you press the locations when you get to them, hopefully in the future only what you can access will be visible but at the moment you could press victory and it would accept it. Also, if you have death_link enabled, there's a button at the top right to trigger and receive death links.