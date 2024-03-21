# Stardew Scripts
This is (or eventually will be) my little pile of scripts for dealing with the many, many Stardew Valley Mods that I like to use in my loadout.

I may or may not take requests. Open an Issue if you want something specific.

# Mise En Place (miseenplace.py)

For Stardew 1.5.6. Not tested with 1.6.

Requires pyjson5.

For Python. Walks through your Mods directory, pulls any JSON files for Cooking recipes, collates them and spits them out into two CSV files for your happy importing to Excel or Google Sheets.

## Usage:

Change line 14 to point to your Stardew Mods directory.

`miseenplace.py`  
Outputs two CSV files to the same directory as the script.

* **recipes.csv** lists all the Cooking recipes individually with their ingredients. 
* **ingredients.csv** counts all of the Cooking ingredients required, recursing infinitely deep for pesky menu items like Complete Breakfast or Seafood Platter from More New Fish. Should be able to handle any pile of Mods pretty quickly. I'm currently running with just over 200 mods and it finished in 8.165 seconds.

**Known Issues:** Does not work with items added via DGA (may fix in the future) or DLL (won't fix) at this time. Does not parse recipes added by Content Patcher. I will not fix this in this script but am working on something that will be able to handle these.
**Update 2023-03-01:** If the JSON file for a specific recipe is poorly formatted or miscategorized the script will now skip it and let you know which ones it skips so you can manually add them. Python has no chill when it comes to JSON lint errors. Also, the script tells you a bit more about what it's doing now.

# Farm Depot (farmdepot.py)

For Stardew 1.5.6. Not tested with 1.6.

Requires pyjson5.

For Python. A switchblade for craftables! Get your Craft Master on with similar CSV outputs to Mise En Place, or do the math to find out how many resources you need to craft multiples of any machine or item on the crafting list.

## Usage: 

Change line 18 to point to your Stardew Mods directory.

`farmdepot.py` or  
`farmdepot.py -master`  
Outputs two CSV files to the same directory as the script. 

* **bigcraftables.csv** lists all Crafting recipes individually with ingredients.
* **craft_ingredients.csv** counts all the Crafting ingredients required for one of each for the Craft Master achievement.

`farmdepot.py -m amount item` or  
`farmdepot.py -math amount item`  
Calculates how many resources you need to make X number of a craftable.

Example: `farmdepot.py -m 155 Cheese Press`

In the event that large amounts of resources are required, it subdivides into chests, stacks and remainder.

**Known Issues:** Does not work with items added via DGA (may fix in the future) or DLL (won't fix) at this time.
**Update 2023-03-02:** Bugfix, discovered that not all craftables are in "BigCraftable" directories so it now searches far more broadly for anything with Recipe ingredients that isn't categorized as "Cooking".

# Pack 'n' Ship (packnship.py)

For Stardew 1.5.6. Not tested with 1.6.

Requires pyjson5.

For Python. Exports a CSV list of JSON items added by mods that probably count towards the Full Shipment Achievement. Does NOT include the Vanilla Full Shipment items as you can find those elsewhere easily. List is sorted by category, alphabetized and chunked into rows of 10 items each for somewhat compact display.

## Usage: 

Change line 14 to point to your Stardew Mods directory.

`packnship.py`  
Outputs one CSV file "shipping.csv" to the same directory as the script.

# Image Chopper (imagechopper.py)

Requires Pillow.

For Python. Chops Vanilla Stardew spritesheets into separate images and enlarges to specified dimensions. Created to assist with the updating of the Stardew Valley wiki following the release of the 1.6 update.

# Usage:

If you want to be walked through the process, run from commandline without any parameters.

For help, use the -h parameter: `python imagechopper.py -h` or `python3 imagechopper.py -h`.

Alternately, use the parameters.

* --i or -input: path to origin image in double quotes
* --w or -width: width of a sprite in the origin image (integer)
* --h or -height: height of a sprite in the origin image (integer)
* --o or -output: path to the directory where you want to store the new images
* --rw or -resultwidth: width of the created images. Images will be scaled to maintain ratios.
* --n or -names: (Optional) path to text file containing a list of image names, one name per line.

If a names file is not provided, files will be named numerically following the pattern NAME_1.png, NAME_2.png, etc. where NAME is the name of the original file.

Example full command with params: 

`python imagechopper.py --i="H:/Stardew Decompiled/Content (unpacked)/Maps/springobjects.png" --w=16 --h=16 --o="H:/Stardew To Do List/chopped/" --rw=96 --n="H:/Stardew To Do List/imagenames.txt"`
