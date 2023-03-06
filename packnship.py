"""
Stardew Modded Pack 'n' Ship
Generates CSV for JSON Full Shipment Items
based on a crawl of your Mods directory.
Change line 14 to suit your needs.
Output files go in the same directory as this script.
"""

import os
import pyjson5
import csv

# change this to your Mods directory.
targetdir = "E:\\Program Files\\SteamLibrary\\steamapps\\common\\Stardew Valley\\Mods"

# vanilla numeric category list
categoryids = {
    "-2": "Mineral",
    "-4": "Fish",
    "-5": "Egg",
    "-6": "Milk",
    "-7": "Cooking",
    "-8": "Crafting",
    "-9": "BigCraftable",
    "-12": "Mineral",
    "-14": "Meat",
    "-15": "Metal Resource",
    "-16": "Building Resource",
    "-17": "Sell at Pierre",
    "-18": "Sell at Pierre or Marnie",
    "-19": "Fertilizer",
    "-20": "Trash",
    "-21": "Bait",
    "-22": "Fishing Tackle",
    "-23": "Sell at Willy",
    "-24": "Decor",
    "-25": "Cooking",
    "-26": "Artisan Goods",
    "-27": "Syrups",
    "-28": "Monster Loot",
    "-29": "Equipment",
    "-74": "Seed",
    "-75": "Vegetable",
    "-79": "Fruit",
    "-80": "Flower",
    "-81": "Forage",
    "-95": "Hat",
    "-96": "Ring",
    "-98": "Weapon",
    "-99": "Tool"
}

# we'll need this later
items = {}

excludedcategories = ['-2', '-4', '-7', '-8', '-9', '-12', '-19', '-20', '-21',
                      '-22', '-24', '-25', '-29', '-74', '-95', '-96', '-98',
                      '-99', 'Mineral', 'Fish', 'Cooking', 'Crafting', 'BigCraftable',
                      'Fertilizer', 'Trash', 'Bait', 'FishingTackle', 'Decor',
                      'Equipment', 'Seed', 'Hat', 'Ring', 'Weapon', 'Tool', 'Gem']


# find all json files in "Objects" subfolders within the Mods directory
def objectdirs(rootdir):
    pathlist = []
    for root, dirs, files in os.walk(rootdir):
        for name in dirs:
            if name == "Objects":
                full_path = os.path.join(root, name)
                pathlist.append(full_path)
    return pathlist


# parse the json files within each directory
# add all recipes to the recipe list
def jsonparse(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if name.endswith((".json")):
                # full_path = os.path.join(root, name)
                # print(full_path)
                try:
                    data = pyjson5.load(open(os.path.join(root, name), encoding="utf-8"))
                    itemname = data["Name"]
                    truecategory = ""
                    if "Category" in data:
                        if str(data["Category"]) not in excludedcategories:
                            if str(data["Category"]) in categoryids:
                                truecategory = categoryids[str(data["Category"])]
                            else:
                                truecategory = data["Category"]

                            if truecategory not in items:
                                items[truecategory] = [itemname]
                            else:
                                items[truecategory].append(itemname)
                except Exception:
                    full_path = os.path.join(root, name)
                    print("Could not parse: " + str(full_path))


print("Now scanning your Mods directory. If nothing is generated, "
      "go back and edit line 14 of the script to point to your Mods folder.")
dirlist = objectdirs(targetdir)
# fill the recipes list
for dirpath in dirlist:
    jsonparse(dirpath)

# print(items)  # uncomment to debug

# output the item list to csv
with open('shipping.csv', 'w', newline='', encoding="utf-8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=",")
    # sort alpha
    for cat, vlist in items.items():
        # remove the dupes
        uniquelist = []
        [uniquelist.append(item.strip()) for item in vlist if item.strip() not in uniquelist]
        filewriter.writerow([cat])
        # alpha sort the category
        sortedvlist = sorted(uniquelist)
        # chunk into rows of 10 items each
        for i in range(0, len(vlist), 10):
            x = i
            filewriter.writerow(sortedvlist[x:x + 10])

print("Files written to the same directory as this script.\n"
      "If I said that I could not read some or any files,\n"
      "it is probably because they are poorly formatted JSON.\n")
