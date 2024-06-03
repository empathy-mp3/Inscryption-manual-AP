# Inscryption Manual Randomizer Guide

This is my take on the Inscryption randomizer! There's 3 rules: 
1. If you haven't received the item for a card, you aren't allowed to play it.
2. You also can't use a card that has a *soul* of a card you're not allowed to play (In the sacrifice altar)
3. Cards that fly onto the board (Corpse Maggots, Pelt Lice, Ijiraq) cannot be added to your deck until you have the item for them.

## Where is the settings page?

The .yaml file is included with the GitHub release.

## What does randomization do to this game?

Every time you add a card to your deck, you get a check. You can receive those items that allow you to play a card.
There are unique items for each pre-made deathcard (e.g., Kaycee, Kaminski, etc.), and also an item for Custom Deathcards.
Cards that appear in multiple acts have one associated item and one associated location, even if they're vastly different in different acts.

## What is the goal of Inscryption when randomized?

4 Different Goals:

- End of Act I
- End of Act II
- End of Act III
- End of Kaycee's Mod

If all these acts are enabled, they are logically in that exact order. 
Disabling acts doesn't do anything yet, so early goals still have items for later acts.

## Required Software

- Inscryption
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Installation Procedures

Make sure a copy of the Manual world is in the lib/world directory of your client-side installation.
If you include Kaycee's Mod in your settings, either have a save file with everything unlocked in Kaycee's Mod, or use the [Unlock All Mod](https://thunderstore.io/c/inscryption/p/IngoH/Unlock_All/) on the Thunderstore Mod Manager.
If you don't have a save with everything unlocked in the base game, you can press Alt + K + C + M

## Joining a MultiWorld Game

1. Launch the launcher.
2. Click on Manual client on the right.
3. At the top enter your server's ip with the port provided (by default archipelago.gg:38281).
4. In Manual Game ID put "Manual_Inscryption_empathymp3" then press the Connect button on the top right.
5. In the command field at the bottom enter the name of your slot you chose in your Player.yaml then press enter

## Manual Client

In the "Tracker and Locations" tab you'll find buttons corresponding with all the available locations in the Randomizer. Since this is a manual game its built on trust™ you press the locations when you get to them, hopefully in the future only what you can access will be visible but at the moment you could press victory and it would accept it. Also, if you have death_link enabled, there's a button at the top right to trigger and receive death links.