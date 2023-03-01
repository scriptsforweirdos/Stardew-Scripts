# Stardew Scripts
This is (or eventually will be) my little pile of scripts for dealing with the many, many Stardew Valley Mods that I like to use in my loadout.

There is only one for now, there will probably be more coming.

I may or may not take requests, find me in the Stardew Discord as NoStealthRaisins#3331.

# Mise En Place (miseenplace.py)

Requires pyjson5.

For Python. Walks through your Mods directory, pulls any JSON files for Cooking recipes, collates them and spits them out into two CSV files for your happy importing to Excel or Google Sheets. 

**recipes.csv** lists all the recipes individually with their ingredients. 

**ingredients.csv** counts all of the ingredients required, recursing 3 levels deep for pesky menu items like Complete Breakfast or Seafood Platter from More New Fish. Should be able to handle any pile of Mods pretty quickly. I'm currently running with just over 200 mods and it finished in 8.165 seconds.

CSV files are output in the same directory as the script. Script can be anywhere on your HD. Change line 14 to point to your Mods directory.

**Known Issue:** If the JSON file for a specific recipe is poorly formed the script will not complete. I need to get some error handling in place for this as right now it will just fail. It uses JSON5 to handle a lot of the weirdness in human-crafted JSON but the game is more relaxed about unlinted JSON than Python is.
