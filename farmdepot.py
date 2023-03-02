"""
Stardew Modded Farm Depot
Generates two files for Crafting recipes and ingredients
based on a crawl of your Mods directory.
Change line 18 to suit your needs.
Output files go in the same directory as this script.
"""

import os
import sys
import argparse
import math
import csv

import pyjson5

# change this to your Mods directory.
targetdir = "E:\\Program Files\\SteamLibrary\\steamapps\\common\\Stardew Valley\\Mods"

# vanilla ID dictionary along with the hardcoded More New Fish IDs
vanillaids = {
    0: "Weeds",
    2: "Stone",
    4: "Stone",
    16: "Wild Horseradish",
    18: "Daffodil",
    20: "Leek",
    22: "Dandelion",
    24: "Parsnip",
    25: "Stone",
    30: "Lumber",
    60: "Emerald",
    62: "Aquamarine",
    64: "Ruby",
    66: "Amethyst",
    68: "Topaz",
    69: "Banana Sapling",
    70: "Jade",
    71: "Trimmed Lucky Purple Shorts",
    72: "Diamond",
    73: "Golden Walnut",
    74: "Prismatic Shard",
    75: "Stone",
    76: "Stone",
    77: "Stone",
    78: "Cave Carrot",
    79: "Secret Note",
    80: "Quartz",
    82: "Fire Quartz",
    84: "Frozen Tear",
    86: "Earth Crystal",
    88: "Coconut",
    90: "Cactus Fruit",
    91: "Banana",
    92: "Sap",
    93: "Torch",
    94: "Spirit Torch",
    95: "Stone",
    96: "Dwarf Scroll I",
    97: "Dwarf Scroll II",
    98: "Dwarf Scroll III",
    99: "Dwarf Scroll IV",
    100: "Chipped Amphora",
    101: "Arrowhead",
    102: "Lost Book",
    103: "Ancient Doll",
    104: "Elvish Jewelry",
    105: "Chewing Stick",
    106: "Ornamental Fan",
    107: "Dinosaur Egg",
    108: "Rare Disc",
    109: "Ancient Sword",
    110: "Rusty Spoon",
    111: "Rusty Spur",
    112: "Rusty Cog",
    113: "Chicken Statue",
    114: "Ancient Seed",
    115: "Prehistoric Tool",
    116: "Dried Starfish",
    117: "Anchor",
    118: "Glass Shards",
    119: "Bone Flute",
    120: "Prehistoric Handaxe",
    121: "Dwarvish Helm",
    122: "Dwarf Gadget",
    123: "Ancient Drum",
    124: "Golden Mask",
    125: "Golden Relic",
    126: "Strange Doll",
    127: "Strange Doll",
    128: "Pufferfish",
    129: "Anchovy",
    130: "Tuna",
    131: "Sardine",
    132: "Bream",
    136: "Largemouth Bass",
    137: "Smallmouth Bass",
    138: "Rainbow Trout",
    139: "Salmon",
    140: "Walleye",
    141: "Perch",
    142: "Carp",
    143: "Catfish",
    144: "Pike",
    145: "Sunfish",
    146: "Red Mullet",
    147: "Herring",
    148: "Eel",
    149: "Octopus",
    150: "Red Snapper",
    151: "Squid",
    152: "Seaweed",
    153: "Green Algae",
    154: "Sea Cucumber",
    155: "Super Cucumber",
    156: "Ghostfish",
    157: "White Algae",
    158: "Stonefish",
    159: "Crimsonfish",
    160: "Angler",
    161: "Ice Pip",
    162: "Lava Eel",
    163: "Legend Fish",
    164: "Sandfish",
    165: "Scorpion Carp",
    166: "Treasure Chest",
    167: "Joja Cola",
    168: "Trash",
    169: "Driftwood",
    170: "Broken Glasses",
    171: "Broken CD",
    172: "Soggy Newspaper",
    174: "Large Egg",
    176: "Egg",
    178: "Hay",
    180: "Egg",
    182: "Large Egg",
    184: "Milk",
    186: "Large Milk",
    188: "Green Bean",
    190: "Cauliflower",
    191: "Ornate Necklace",
    192: "Potato",
    194: "Fried Egg",
    195: "Omelet",
    196: "Salad",
    197: "Cheese Cauliflower",
    198: "Baked Fish",
    199: "Parsnip Soup",
    200: "Vegetable Medley",
    201: "Complete Breakfast",
    202: "Fried Calamari",
    203: "Strange Bun",
    204: "Lucky Lunch",
    205: "Fried Mushroom",
    206: "Pizza",
    207: "Bean Hotpot",
    208: "Glazed Yams",
    209: "Carp Surprise",
    210: "Hashbrowns",
    211: "Pancakes",
    212: "Salmon Dinner",
    213: "Fish Taco",
    214: "Crispy Bass",
    215: "Pepper Poppers",
    216: "Bread",
    218: "Tom Kha Soup",
    219: "Trout Soup",
    220: "Chocolate Cake",
    221: "Pink Cake",
    222: "Rhubarb Pie",
    223: "Cookie",
    224: "Spaghetti",
    225: "Fried Eel",
    226: "Spicy Eel",
    227: "Sashimi",
    228: "Maki Roll",
    229: "Tortilla",
    230: "Red Plate",
    231: "Eggplant Parmesan",
    232: "Rice Pudding",
    233: "Ice Cream",
    234: "Blueberry Tart",
    235: "Autumn's Bounty",
    236: "Pumpkin Soup",
    237: "Super Meal",
    238: "Cranberry Sauce",
    239: "Stuffing",
    240: "Farmer's Lunch",
    241: "Survival Burger",
    242: "Dish O' The Sea",
    243: "Miner's Treat",
    244: "Roots Platter",
    245: "Sugar",
    246: "Wheat Flour",
    247: "Oil",
    248: "Garlic",
    250: "Kale",
    251: "Tea Sapling",
    252: "Rhubarb",
    253: "Triple Shot Espresso",
    254: "Melon",
    256: "Tomato",
    257: "Morel",
    258: "Blueberry",
    259: "Fiddlehead Fern",
    260: "Hot Pepper",
    261: "Warp Totem: Desert",
    262: "Wheat",
    264: "Radish",
    265: "Seafoam Pudding",
    266: "Red Cabbage",
    267: "Flounder",
    268: "Starfruit",
    269: "Midnight Carp",
    270: "Corn",
    271: "Unmilled Rice",
    272: "Eggplant",
    273: "Rice Shoot",
    274: "Artichoke",
    275: "Artifact Trove",
    276: "Pumpkin",
    277: "Wilted Bouquet",
    278: "Bok Choy",
    279: "Magic Rock Candy",
    280: "Yam",
    281: "Chanterelle",
    282: "Cranberries",
    283: "Holly",
    284: "Beet",
    286: "Cherry Bomb",
    287: "Bomb",
    288: "Mega Bomb",
    289: "Ostrich Egg",
    290: "Stone",
    292: "Mahogany Seed",
    293: "Brick Floor",
    294: "Twig",
    295: "Twig",
    296: "Salmonberry",
    297: "Grass Starter",
    298: "Hardwood Fence",
    299: "Amaranth Seeds",
    300: "Amaranth",
    301: "Grape Starter",
    302: "Hops Starter",
    303: "Pale Ale",
    304: "Hops",
    305: "Void Egg",
    306: "Mayonnaise",
    307: "Duck Mayonnaise",
    308: "Void Mayonnaise",
    309: "Acorn",
    310: "Maple Seed",
    311: "Pine Cone",
    313: "Weeds",
    314: "Weeds",
    315: "Weeds",
    316: "Weeds",
    317: "Weeds",
    318: "Weeds",
    319: "Weeds",
    320: "Weeds",
    321: "Weeds",
    322: "Wood Fence",
    323: "Stone Fence",
    324: "Iron Fence",
    325: "Gate",
    326: "Dwarvish Translation Guide",
    328: "Wood Floor",
    329: "Stone Floor",
    330: "Clay",
    331: "Weathered Floor",
    333: "Crystal Floor",
    334: "Copper Bar",
    335: "Iron Bar",
    336: "Gold Bar",
    337: "Iridium Bar",
    338: "Refined Quartz",
    340: "Honey",
    341: "Tea Set",
    342: "Pickles",
    343: "Stone",
    344: "Jelly",
    346: "Beer",
    347: "Rare Seed",
    348: "Wine",
    349: "Energy Tonic",
    350: "Juice",
    351: "Muscle Remedy",
    368: "Basic Fertilizer",
    369: "Quality Fertilizer",
    370: "Basic Retaining Soil",
    371: "Quality Retaining Soil",
    372: "Clam",
    373: "Golden Pumpkin",
    376: "Poppy",
    378: "Copper Ore",
    380: "Iron Ore",
    382: "Coal",
    384: "Gold Ore",
    386: "Iridium Ore",
    388: "Wood",
    390: "Stone",
    392: "Nautilus Shell",
    393: "Coral",
    394: "Rainbow Shell",
    395: "Coffee",
    396: "Spice Berry",
    397: "Sea Urchin",
    398: "Grape",
    399: "Spring Onion",
    400: "Strawberry",
    401: "Straw Floor",
    402: "Sweet Pea",
    403: "Field Snack",
    404: "Common Mushroom",
    405: "Wood Path",
    406: "Wild Plum",
    407: "Gravel Path",
    408: "Hazelnut",
    409: "Crystal Path",
    410: "Blackberry",
    411: "Cobblestone Path",
    412: "Winter Root",
    413: "Blue Slime Egg",
    414: "Crystal Fruit",
    415: "Stepping Stone Path",
    416: "Snow Yam",
    417: "Sweet Gem Berry",
    418: "Crocus",
    419: "Vinegar",
    420: "Red Mushroom",
    421: "Sunflower",
    422: "Purple Mushroom",
    423: "Rice",
    424: "Cheese",
    425: "Fairy Seeds",
    426: "Goat Cheese",
    427: "Tulip Bulb",
    428: "Cloth",
    429: "Jazz Seeds",
    430: "Truffle",
    431: "Sunflower Seeds",
    432: "Truffle Oil",
    433: "Coffee Bean",
    434: "Stardrop",
    436: "Goat Milk",
    437: "Red Slime Egg",
    438: "L. Goat Milk",
    439: "Purple Slime Egg",
    440: "Wool",
    441: "Explosive Ammo",
    442: "Duck Egg",
    444: "Duck Feather",
    445: "Caviar",
    446: "Rabbit's Foot",
    447: "Aged Roe",
    449: "Stone Base",
    450: "Stone",
    452: "Weeds",
    453: "Poppy Seeds",
    454: "Ancient Fruit",
    455: "Spangle Seeds",
    456: "Algae Soup",
    457: "Pale Broth",
    458: "Bouquet",
    459: "Mead",
    460: "Mermaid's Pendant",
    461: "Decorative Pot",
    463: "Drum Block",
    464: "Flute Block",
    465: "Speed-Gro",
    466: "Deluxe Speed-Gro",
    472: "Parsnip Seeds",
    473: "Bean Starter",
    474: "Cauliflower Seeds",
    475: "Potato Seeds",
    476: "Garlic Seeds",
    477: "Kale Seeds",
    478: "Rhubarb Seeds",
    479: "Melon Seeds",
    480: "Tomato Seeds",
    481: "Blueberry Seeds",
    482: "Pepper Seeds",
    483: "Wheat Seeds",
    484: "Radish Seeds",
    485: "Red Cabbage Seeds",
    486: "Starfruit Seeds",
    487: "Corn Seeds",
    488: "Eggplant Seeds",
    489: "Artichoke Seeds",
    490: "Pumpkin Seeds",
    491: "Bok Choy Seeds",
    492: "Yam Seeds",
    493: "Cranberry Seeds",
    494: "Beet Seeds",
    495: "Spring Seeds",
    496: "Summer Seeds",
    497: "Fall Seeds",
    498: "Winter Seeds",
    499: "Ancient Seeds",
    516: "Small Glow Ring",
    517: "Glow Ring",
    518: "Small Magnet Ring",
    519: "Magnet Ring",
    520: "Slime Charmer Ring",
    521: "Warrior Ring",
    522: "Vampire Ring",
    523: "Savage Ring",
    524: "Ring of Yoba",
    525: "Sturdy Ring",
    526: "Burglar's Ring",
    527: "Iridium Band",
    528: "Jukebox Ring",
    529: "Amethyst Ring",
    530: "Topaz Ring",
    531: "Aquamarine Ring",
    532: "Jade Ring",
    533: "Emerald Ring",
    534: "Ruby Ring",
    535: "Geode",
    536: "Frozen Geode",
    537: "Magma Geode",
    538: "Alamite",
    539: "Bixite",
    540: "Baryte",
    541: "Aerinite",
    542: "Calcite",
    543: "Dolomite",
    544: "Esperite",
    545: "Fluorapatite",
    546: "Geminite",
    547: "Helvite",
    548: "Jamborite",
    549: "Jagoite",
    550: "Kyanite",
    551: "Lunarite",
    552: "Malachite",
    553: "Neptunite",
    554: "Lemon Stone",
    555: "Nekoite",
    556: "Orpiment",
    557: "Petrified Slime",
    558: "Thunder Egg",
    559: "Pyrite",
    560: "Ocean Stone",
    561: "Ghost Crystal",
    562: "Tigerseye",
    563: "Jasper",
    564: "Opal",
    565: "Fire Opal",
    566: "Celestine",
    567: "Marble",
    568: "Sandstone",
    569: "Granite",
    570: "Basalt",
    571: "Limestone",
    572: "Soapstone",
    573: "Hematite",
    574: "Mudstone",
    575: "Obsidian",
    576: "Slate",
    577: "Fairy Stone",
    578: "Star Shards",
    579: "Prehistoric Scapula",
    580: "Prehistoric Tibia",
    581: "Prehistoric Skull",
    582: "Skeletal Hand",
    583: "Prehistoric Rib",
    584: "Prehistoric Vertebra",
    585: "Skeletal Tail",
    586: "Nautilus Fossil",
    587: "Amphibian Fossil",
    588: "Palm Fossil",
    589: "Trilobite",
    590: "Artifact Spot",
    591: "Tulip",
    593: "Summer Spangle",
    595: "Fairy Rose",
    597: "Blue Jazz",
    599: "Sprinkler",
    604: "Plum Pudding",
    605: "Artichoke Dip",
    606: "Stir Fry",
    607: "Roasted Hazelnuts",
    608: "Pumpkin Pie",
    609: "Radish Salad",
    610: "Fruit Salad",
    611: "Blackberry Cobbler",
    612: "Cranberry Candy",
    613: "Apple",
    614: "Green Tea",
    618: "Bruschetta",
    621: "Quality Sprinkler",
    628: "Cherry Sapling",
    629: "Apricot Sapling",
    630: "Orange Sapling",
    631: "Peach Sapling",
    632: "Pomegranate Sapling",
    633: "Apple Sapling",
    634: "Apricot",
    635: "Orange",
    636: "Peach",
    637: "Pomegranate",
    638: "Cherry",
    645: "Iridium Sprinkler",
    648: "Coleslaw",
    649: "Fiddlehead Risotto",
    651: "Poppyseed Muffin",
    668: "Stone",
    670: "Stone",
    674: "Weeds",
    675: "Weeds",
    676: "Weeds",
    677: "Weeds",
    678: "Weeds",
    679: "Weeds",
    680: "Green Slime Egg",
    681: "Rain Totem",
    682: "Mutant Carp",
    684: "Bug Meat",
    685: "Bait",
    686: "Spinner",
    687: "Dressed Spinner",
    688: "Warp Totem Farm",
    689: "Warp Totem Mountains",
    690: "Warp Totem Beach",
    691: "Barbed Hook",
    692: "Lead Bobber",
    693: "Treasure Hunter",
    694: "Trap Bobber",
    695: "Cork Bobber",
    698: "Sturgeon",
    699: "Tiger Trout",
    700: "Bullhead",
    701: "Tilapia",
    702: "Chub",
    703: "Magnet",
    704: "Dorado",
    705: "Albacore",
    706: "Shad",
    707: "Lingcod",
    708: "Halibut",
    709: "Hardwood",
    710: "Crab Pot",
    715: "Lobster",
    716: "Crayfish",
    717: "Crab",
    718: "Cockle",
    719: "Mussel",
    720: "Shrimp",
    721: "Snail",
    722: "Periwinkle",
    723: "Oyster",
    724: "Maple Syrup",
    725: "Oak Resin",
    726: "Pine Tar",
    727: "Chowder",
    728: "Fish Stew",
    729: "Escargot",
    730: "Lobster Bisque",
    731: "Maple Bar",
    732: "Crab Cakes",
    733: "Shrimp Cocktail",
    734: "Woodskip",
    745: "Strawberry Seeds",
    746: "Jack-O-Lantern",
    747: "Rotten Plant",
    748: "Rotten Plant",
    749: "Omni Geode",
    750: "Weeds",
    751: "Stone",
    760: "Stone",
    762: "Stone",
    764: "Stone",
    765: "Stone",
    766: "Slime",
    767: "Bat Wing",
    768: "Solar Essence",
    769: "Void Essence",
    770: "Mixed Seeds",
    771: "Fiber",
    772: "Oil of Garlic",
    773: "Life Elixir",
    774: "Wild Bait",
    775: "Glacierfish",
    784: "Weeds",
    785: "Weeds",
    786: "Weeds",
    787: "Battery Pack",
    788: "Lost Axe",
    789: "Lucky Purple Shorts",
    790: "Berry Basket",
    791: "Golden Coconut",
    792: "Weeds",
    793: "Weeds",
    794: "Weeds",
    795: "Void Salmon",
    796: "Slimejack",
    797: "Pearl",
    798: "Midnight Squid",
    799: "Spook Fish",
    800: "Blobfish",
    801: "Wedding Ring",
    802: "Cactus Seeds",
    803: "Iridium Milk",
    805: "Tree Fertilizer",
    807: "Dinosaur Mayonnaise",
    808: "Void Ghost Pendant",
    809: "Movie Ticket",
    810: "Crabshell Ring",
    811: "Napalm Ring",
    812: "Roe",
    814: "Squid Ink",
    815: "Tea Leaves",
    816: "Stone",
    817: "Stone",
    818: "Stone",
    819: "Stone",
    820: "Fossilized Skull",
    821: "Fossilized Spine",
    822: "Fossilized Tail",
    823: "Fossilized Leg",
    824: "Fossilized Ribs",
    825: "Snake Skull",
    826: "Snake Vertebrae",
    827: "Mummified Bat",
    828: "Mummified Frog",
    829: "Ginger",
    830: "Taro Root",
    831: "Taro Tuber",
    832: "Pineapple",
    833: "Pineapple Seeds",
    834: "Mango",
    835: "Mango Sapling",
    836: "Stingray",
    837: "Lionfish",
    838: "Blue Discus",
    839: "Thorns Ring",
    840: "Rustic Plank Floor",
    841: "Stone Walkway Floor",
    842: "Journal Scrap",
    843: "Stone",
    844: "Stone",
    845: "Stone",
    846: "Stone",
    847: "Stone",
    848: "Cinder Shard",
    849: "Stone",
    850: "Stone",
    851: "Magma Cap",
    852: "Dragon Tooth",
    856: "Curiosity Lure",
    857: "Tiger Slime Egg",
    858: "Qi Gem",
    859: "Lucky Ring",
    860: "Hot Java Ring",
    861: "Protection Ring",
    862: "Soul Sapper Ring",
    863: "Phoenix Ring",
    864: "War Memento",
    865: "Gourmet Tomato Salt",
    866: "Stardew Valley Rose",
    867: "Advanced TV Remote",
    868: "Arctic Shard",
    869: "Wriggling Worm",
    870: "Pirate's Locket",
    872: "Fairy Dust",
    873: "Pina Colada",
    874: "Bug Steak",
    875: "Ectoplasm",
    876: "Prismatic Jelly",
    877: "Quality Bobber",
    879: "Monster Musk",
    880: "Combined Ring",
    881: "Bone Fragment",
    882: "Weeds",
    883: "Weeds",
    884: "Weeds",
    885: "Fiber Seeds",
    886: "Warp Totem: Island",
    887: "Immunity Band",
    888: "Glowstone Ring",
    889: "Qi Fruit",
    890: "Qi Bean",
    891: "Mushroom Tree Seed",
    892: "Warp Totem: Qi's Arena",
    893: "Fireworks (Red)",
    894: "Fireworks (Purple)",
    895: "Fireworks (Green)",
    896: "Galaxy Soul",
    897: "Pierre's Missing Stocklist",
    898: "Son of Crimsonfish",
    899: "Ms. Angler",
    900: "Legend II",
    901: "Radioactive Carp",
    902: "Glacierfish Jr.",
    903: "Ginger Ale",
    904: "Banana Pudding",
    905: "Mango Sticky Rice",
    906: "Poi",
    907: "Tropical Curry",
    908: "Magic Bait",
    909: "Radioactive Ore",
    910: "Radioactive Bar",
    911: "Horse Flute",
    913: "Enricher",
    915: "Pressure Nozzle",
    917: "Qi Seasoning",
    918: "Hyper Speed-Gro",
    919: "Deluxe Fertilizer",
    920: "Deluxe Retaining Soil",
    921: "Squid Ink Ravioli",
    922: "SupplyCrate",
    923: "SupplyCrate",
    924: "SupplyCrate",
    925: "Slime Crate",
    926: "Cookout Kit",
    927: "Camping Stove",
    928: "Golden Egg",
    929: "Hedge",
    -4: "Any Fish",
    -5: "Any Milk",
    -6: "Any Egg",
    -75: "Any Vegetable",
    -79: "Any Fruit",
    1056: "Clown Knifefish",
    1057: "Freshwater Butterflyfish",
    1058: "Mimic Octopus",
    1059: "Blue-Ringed Octopus",
    1060: "Stubby Squid",
    1061: "Dumbo Octopus",
    1062: "Barreleye",
    1063: "Freshwater Pufferfish",
    1064: "Void Algae",
    1065: "Void Evilpus",
    1066: "Trapped Soul",
    1067: "Lamprey",
    1068: "Ribbon Eel",
    1069: "Ghost Eel",
    1070: "Robalo",
    1071: "Anchoviella",
    1072: "Hagfish",
    1073: "Green Terror",
    1074: "Clown Loach",
    1075: "Brain Slug",
    1076: "Zebra Eel",
    1077: "Yamabuki Koi",
    1078: "Ghost Koi",
    1079: "Hi Utsuri Koi",
    1080: "Conger",
    1081: "Shiro Utsuri Koi",
    1082: "Ki Utsuri Koi",
    1083: "Redtail Shark",
    1084: "Elephantfish",
    1085: "Sauger",
    1086: "Pacu",
    1087: "Common Pleco",
    1088: "Siamese Algae Eater",
    1089: "Snowball Pleco",
    1090: "Ide",
    1091: "Pangasius",
    1092: "Trahira",
    1093: "Blue Dragon Slug",
    1094: "Nautilus",
    1095: "Cyclops Shark",
    1096: "Starfish",
    1097: "Blue Starfish",
    1098: "Royal Starfish",
    1099: "Crown of Thorns Starfish",
    1100: "Holy Grenade Starfish",
    1101: "Freshwater Shrimp",
    1102: "Red Freshwater Shrimp",
    1103: "Blue Freshwater Shrimp",
    1104: "Harlequin Freshwater Shrimp",
    1105: "Red Harlequin Freshwater Shrimp",
    1106: "Brief Squid",
    1107: "Prawn",
    1108: "Sand Dollar",
    1109: "King Crab",
    1110: "Decapod",
    1111: "Mudskipper",
    1114: "Cave Lobster",
    1115: "Freshwater Crab",
    1116: "Fishing Elixir",
    1117: "Warrior Elixir",
    1118: "Shinidamachu",
    1119: "Vampire Squid",
    1120: "Ladyfish",
    1121: "Tancho Koi",
    1122: "Kohaku Koi",
    1123: "Sanke Koi",
    1124: "Zebra Tilapia",
    1125: "Tucunare",
    1126: "Small Goblin Shark",
    1127: "Tui",
    1128: "La",
    1129: "Small Mantaray",
    1130: "Piranha",
    1131: "Blinky",
    1132: "Arowana",
    1133: "Arctic Char",
    1134: "Tench",
    1135: "Haddock",
    1136: "Small Swordfish",
    1137: "Barracuda",
    1138: "Longfin Icedevil",
    1139: "Spinny Dogfish",
    1140: "Void Carp",
    1141: "Water Snake",
    1142: "Electric Catfish",
    1143: "Sea Snake",
    1144: "Swimmer Crab",
    1145: "Glassfish",
    1146: "Goldfish",
    1147: "Lionhead",
    1148: "Comet",
    1149: "Telescope",
    1150: "Celestial Eye",
    1151: "Jellyfish",
    1152: "Vampire Fish",
    1153: "Lungfish",
    1154: "Tigerfish",
    1155: "Longnose Gar",
    1156: "Sebae Clownfish",
    1157: "Wide-band Clownfish",
    1158: "Saddleback Clownfish",
    1159: "Orange Clownfish",
    1160: "Skunk Clownfish",
    1161: "Pink Skunk Clownfish",
    1162: "Maroon Clownfish",
    1163: "Whitesnout Clownfish",
    1164: "Fire Clownfish",
    1165: "Two-Band Clownfish",
    1166: "Yellowtail Clownfish",
    1167: "Pollock",
    1168: "Blue Tang",
    1169: "Moorish Idol",
    1170: "Royal Angelfish",
    1171: "Ornate Angelfish",
    1172: "Banded Angelfish",
    1173: "Threespot Angelfish",
    1174: "Flame Angelfish",
    1175: "Dwarf Stingray",
    1176: "Monkfish",
    1177: "Squirrelfish",
    1178: "Icefish",
    1179: "Soldierfish",
    1180: "False Kelpfish",
    1181: "Thread-Sail Filefish",
    1182: "Wolffish",
    1184: "Coelacanth",
    1185: "Cavefish",
    1186: "Mandarinfish",
    1187: "Tiger Puffer",
    1188: "Great Firefly Squid",
    1201: "Black Ghost Knifefish",
    1202: "Clown Triggerfish",
    1203: "Bonnethead",
    1204: "Goblin Shark Pup",
    1205: "Bonnethead Pup",
    1206: "Spiny Dogfish Pup",
    1207: "Dwarf Stingray Pup",
    1208: "Manta Ray Pup",
}

# we'll need this later
ingredients = {}

# vanilla recipes
recipes = {
    "Cherry Bomb": {"Copper Ore": 4, "Coal": 1},
    "Bomb": {"Iron Ore": 4, "Coal": 1},
    "Mega Bomb": {"Gold Ore": 4, "Solar Essence": 1, "Void Essence": 1},
    "Gate": {"Wood": 10},
    "Wood Fence": {"Wood": 2},
    "Stone Fence": {"Stone": 2},
    "Iron Fence": {"Iron Bar": 1},
    "Hardwood Fence": {"Hardwood": 1},
    "Sprinkler": {"Copper Bar": 1, "Iron Bar": 1},
    "Quality Sprinkler": {"Iron Bar": 1, "Gold Bar": 1, "Refined Quartz": 1},
    "Iridium Sprinkler": {"Gold Bar": 1, "Iridium Bar": 1, "Battery Pack": 1},
    "Mayonnaise Machine": {"Wood": 15, "Stone": 15, "Earth Crystal": 1, "Copper Bar": 1},
    "Bee House": {"Wood": 40, "Coal": 8, "Iron Bar": 1, "Maple Syrup": 1},
    "Preserves Jar": {"Wood": 50, "Stone": 40, "Coal": 8},
    "Cheese Press": {"Wood": 45, "Stone": 45, "Hardwood": 10, "Copper Bar": 1},
    "Loom": {"Wood": 60, "Fiber": 30, "Pine Tar": 1},
    "Keg": {"Wood": 30, "Copper Bar": 1, "Oak Resin": 1, "Iron Bar": 1},
    "Oil Maker": {"Slime": 50, "Hardwood": 20, "Gold Bar": 1},
    "Cask": {"Wood": 20, "Hardwood": 1},
    "Basic Fertilizer": {"Sap": 2},
    "Quality Fertilizer": {"Sap": 2, "Any Fish": 1},
    "Deluxe Fertilizer": {"Iridium Bar": 1, "Sap": 40},
    "Speed-Gro": {"Pine Tar": 1, "Clam": 1},
    "Deluxe Speed-Gro": {"Oak Resin": 1, "Coral": 1},
    "Hyper Speed-Gro": {"Radioactive Ore": 1, "Bone Fragment": 3, "Solar Essence": 1},
    "Basic Retaining Soil": {"Stone": 2},
    "Quality Retaining Soil": {"Stone": 3, "Clay": 1},
    "Deluxe Retaining Soil": {"Stone": 5, "Fiber": 3, "Clay": 1},
    "Tree Fertilizer": {"Fiber": 5, "Stone": 5},
    "Wild Seeds (Sp)": {"Wild Horseradish": 1, "Daffodil": 1, "Leek": 1, "Dandelion": 1},
    "Wild Seeds (Su)": {"Spice Berry": 1, "Grape": 1, "Sweet Pea": 1},
    "Wild Seeds (Fa)": {"Common Mushroom": 1, "Wild Plum": 1, "Hazelnut": 1, "Blackberry": 1},
    "Wild Seeds (Wi)": {"Winter Root": 1, "Crystal Fruit": 1, "Snow Yam": 1, "Crocus": 1},
    "Ancient Seeds": {"Ancient Seed": 1},
    "Grass Starter": {"Fiber": 10},
    "Tea Sapling": {"Any Wild Seeds": 2, "Fiber": 5, "Wood": 5},
    "Fiber Seeds": {"Mixed Seeds": 1, "Sap": 5, "Clay": 1},
    "Wood Floor": {"Wood": 1},
    "Rustic Plank Floor": {"Wood": 1},
    "Straw Floor": {"Wood": 1, "Fiber": 1},
    "Weathered Floor": {"Wood": 1},
    "Crystal Floor": {"Refined Quartz": 1},
    "Stone Floor": {"Stone": 1},
    "Stone Walkway Floor": {"Stone": 1},
    "Brick Floor": {"Clay": 2, "Stone": 5},
    "Wood Path": {"Wood": 1},
    "Gravel Path": {"Stone": 1},
    "Cobblestone Path": {"Stone": 1},
    "Stepping Stone Path": {"Stone": 1},
    "Crystal Path": {"Refined Quartz": 1},
    "Spinner": {"Iron Bar": 2},
    "Trap Bobber": {"Copper Bar": 1, "Sap": 10},
    "Cork Bobber": {"Wood": 10, "Hardwood": 5, "Slime": 10},
    "Quality Bobber": {"Copper Bar": 1, "Sap": 20, "Solar Essence": 5},
    "Treasure Hunter": {"Gold Bar": 2},
    "Dressed Spinner": {"Iron Bar": 2, "Cloth": 1},
    "Barbed Hook": {"Copper Bar": 1, "Iron Bar": 1, "Gold Bar": 1},
    "Magnet": {"Iron Bar": 1},
    "Bait ": {"Bug Meat": 1},
    "Wild Bait": {"Fiber": 10, "Bug Meat": 5, "Slime": 5},
    "Magic Bait": {"Radioactive Ore": 1, "Bug Meat": 3},
    "Crab Pot": {"Iron Bar": 3, "Wood": 40},
    "Sturdy Ring": {"Copper Bar": 2, "Bug Meat": 25, "Slime": 25},
    "Warrior Ring": {"Iron Bar": 10, "Coal": 25, "Frozen Tear": 10},
    "Ring Of Yoba": {"Gold Bar": 5, "Iron Bar": 5, "Diamond": 1},
    "Thorns Ring": {"Bone Fragment": 50, "Stone": 50, "Gold Bar": 1},
    "Glowstone Ring": {"Solar Essence": 5, "Iron Bar": 5},
    "Iridium Band": {"Iridium Bar": 5, "Solar Essence": 50, "Void Essence": 50},
    "Wedding Ring": {"Iridium Bar": 5, "Prismatic Shard": 1},
    "Field Snack": {"Acorn": 1, "Maple See": 1, "Pine Cone": 1},
    "Bug Steak": {"Bug Meat": 10},
    "Life Elixir": {"Red Mushroom": 1, "Purple Mushroom": 1, "Morel": 1, "Chanterelle": 1},
    "Oil Of Garlic": {"Garlic": 10, "Oil": 1},
    "Monster Musk": {"Bat Wing": 30, "Slime": 30},
    "Fairy Dust": {"Diamond": 1, "Fairy Rose": 1},
    "Warp Totem: Beach": {"Hardwood": 1, "Coral": 2, "Fiber": 10},
    "Warp Totem: Mountains": {"Hardwood": 1, "Iron Bar": 1, "Stone": 25},
    "Warp Totem: Farm": {"Hardwood": 1, "Honey": 1, "Fiber": 20},
    "Warp Totem: Desert": {"Hardwood": 2, "Coconut": 1, "Iridium Ore": 4},
    "Warp Totem: Island": {"Hardwood": 5, "Dragon Tooth": 1, "Ginger": 1},
    "Rain Totem": {"Hardwood": 1, "Truffle Oil": 1, "Pine Tar": 5},
    "Torch": {"Wood": 1, "Sap": 2},
    "Campfire": {"Stone": 10, "Wood": 10, "Fiber": 10},
    "Wooden Brazier": {"Wood": 10, "Coal": 1, "Fiber": 5},
    "Stone Brazier": {"Stone": 10, "Coal": 1, "Fiber": 5},
    "Gold Brazier": {"Gold Bar": 1, "Coal": 1, "Fiber": 5},
    "Carved Brazier": {"Hardwood": 10, "Coal": 1},
    "Stump Brazier": {"Hardwood": 5, "Coal": 1},
    "Barrel Brazier": {"Wood": 50, "Coal": 1, "Solar Essence": 1},
    "Skull Brazier": {"Bone Fragment": 10},
    "Marble Brazier": {"Marble": 1, "Aquamarine": 1, "Stone": 100},
    "Wood Lamp-post": {"Wood": 50, "Battery Pack": 1},
    "Iron Lamp-post": {"Iron Bar": 1, "Battery Pack": 1},
    "Jack-O-Lantern": {"Pumpkin": 1, "Wood": 1, "Sap": 2},
    "Charcoal Kiln": {"Wood": 20, "Copper Bar": 2},
    "Crystalarium": {"Stone": 99, "Gold Bar": 5, "Iridium Bar": 2, "Battery Pack": 1},
    "Furnace": {"Copper Ore": 20, "Stone": 25},
    "Lightning Rod": {"Iron Bar": 1, "Refined Quartz": 1, "Bat Wing": 5},
    "Solar Panel": {"Refined Quartz": 10, "Iron Bar": 5, "Gold Bar": 5},
    "Recycling Machine": {"Wood": 25, "Stone": 25, "Iron Bar": 1},
    "Seed Maker": {"Wood": 25, "Coal": 10, "Gold Bar": 1},
    "Slime Incubator": {"Iridium Bar": 2, "Slime": 100},
    "Ostrich Incubator": {"Bone Fragment": 50, "Hardwood": 50, "Cinder Shard": 20},
    "Slime Egg-Press": {"Coal": 25, "Fire Quartz": 1, "Battery Pack": 1},
    "Tapper": {"Wood": 40, "Copper Bar": 2},
    "Heavy Tapper": {"Hardwood": 30, "Radioactive Bar": 1},
    "Worm Bin": {"Hardwood": 25, "Gold Bar": 1, "Iron Bar": 1, "Fiber": 50},
    "Bone Mill": {"Bone Fragment": 10, "Clay": 3, "Stone": 20},
    "Geode Crusher": {"Gold Bar": 2, "Stone": 50, "Diamond": 1},
    "Tub O Flowers": {"Wood": 15, "Tulip Bulb": 1, "Jazz Seeds": 1, "Poppy Seeds": 1, "Spangle Seeds": 1},
    "Wicked Statue": {"Stone": 25, "Coal": 5},
    "Flute Block": {"Wood": 10, "Copper Ore": 2, "Fiber": 20},
    "Drum Block": {"Stone": 10, "Copper Ore": 2, "Fiber": 20},
    "Chest": {"Wood": 50},
    "Stone Chest": {"Stone": 50},
    "Wood Sign": {"Wood": 25},
    "Stone Sign": {"Stone": 25},
    "Dark Sign": {"Bat Wing": 5, "Bone Fragment": 5},
    "Garden Pot": {"Clay": 1, "Stone": 10, "Refined Quartz": 1},
    "Scarecrow": {"Wood": 50, "Coal": 1, "Fiber": 20},
    "Deluxe Scarecrow": {"Wood": 50, "Fiber": 40, "Iridium Ore": 1},
    "Staircase": {"Stone": 99},
    "Explosive Ammo": {"Iron Bar": 1, "Coal": 2},
    "Transmute (Fe)": {"Copper Bar": 3},
    "Transmute (Au)": {"Iron Bar": 2},
    "Mini-Jukebox": {"Iron Bar": 2, "Battery Pack": 1},
    "Mini-Obelisk": {"Hardwood": 30, "Solar Essence": 20, "Gold Bar": 3},
    "Farm Computer": {"Dwarf Gadget": 1, "Battery Pack": 1, "Refined Quartz": 10},
    "Hopper": {"Hardwood": 10, "Iridium Bar": 1, "Radioactive Bar": 1},
    "Cookout Kit": {"Wood": 15, "Fiber": 10, "Coal": 3},
}


# find all json files in "BigCraftables" subfolders within the Mods directory
def objectdirs(rootdir):
    pathlist = []
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if name == "object.json" or name == "big-craftable.json":
                full_path = os.path.join(root, name)
                pathlist.append(full_path)
    return pathlist


# parse the json files within each directory
# add all recipes to the recipe list
# In this case we want anything that has recipe ingredients but isn't Cooking.
def jsonparse(filepath):
    try:
        data = pyjson5.load(open(filepath, encoding="utf-8"))
        recipename = data["Name"]
        # recipecategory = data["Category"]
        # print(recipename + " " + recipecategory)
        itemlist = {}
        if (("Category" in data and data["Category"] != "Cooking") or "Category" not in data) and "Recipe" in data and data["Recipe"] is not None and "Ingredients" in data["Recipe"]:
            for item in data["Recipe"]["Ingredients"]:
                if item["Object"] in vanillaids:
                    objectname = vanillaids[item["Object"]]
                else:
                    objectname = item["Object"]
                itemlist[objectname] = item["Count"]
                # Add the recipe to the recipes list
                recipes[recipename] = itemlist
    except Exception:
        print("Could not parse: " + str(filepath))


def craftmaster():
    print("Now scanning your Mods directory. If nothing is generated,\n"
          "go back and edit line 18 of the script to point to your Mods folder.")
    dirlist = objectdirs(targetdir)
    # fill the recipes list
    for dirpath in dirlist:
        jsonparse(dirpath)

    print(recipes)  # uncomment to debug

    # output the recipe list to csv
    with open('bigcraftables.csv', 'w', newline='', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=",")
        filewriter.writerow(['Object', 'Ingredients'])
        # sort alpha
        sorted_recipes = {key: value for key, value in sorted(recipes.items())}
        for k, v in sorted_recipes.items():
            inglist = []
            for k1, v1 in sorted_recipes[k].items():
                prettytext = str(v1) + " " + str(k1)
                inglist.append(prettytext)
            ingtext = "\r\n".join(inglist)
            filewriter.writerow([k, ingtext])

    # Now let's walk through that recipe list and make the ingredients list
    # Unlike Cooking, no recursion is needed for Big Craftables.
    for k, v in recipes.items():
        for k1, v1 in v.items():
            if k1 in ingredients:
                ingredients[k1] += v1
            else:
                ingredients[k1] = v1

    # print(ingredients)  # uncomment to debug

    with open('craft_ingredients.csv', 'w', newline='', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=",")
        filewriter.writerow(['Ingredient', 'Amount'])
        # sort alpha
        sorted_ingredients = {key: value for key, value in sorted(ingredients.items())}
        for k, v in sorted_ingredients.items():
            filewriter.writerow([k, v])

    print("Files written to the same directory as this script.\n\n"
          "If I said that I could not read some or any files,\n"
          "it is probably because they are poorly formatted JSON.\n"
          "If they happen to be required for Craft Master, you will have to\n"
          "manually add them to the tallies created.\n\n"
          "This script handles JSON Assets and Vanilla items only.\n"
          "If an item is added via DLL or DGA it will not be included.\n\n"
          "If you are a Trapper, deduct 15 Wood and 3 Iron bars and\n"
          "add 2 Copper Bars to the crafting ingredients list.\n\n"
          "The Wedding Ring (included) is not required for\n"
          "solo players. If you are playing solo, deduct 5 Iridium Bars\n"
          "and 1 Prismatic Shard from the ingredients list.")


def calculate(amount, searchitem):
    tocraft = {}
    if searchitem in recipes:
        tocraft = recipes[searchitem]
    else:
        print("Hang on while I look up that recipe...")
        for dirpath, dirnames, filenames in os.walk(targetdir):
            for dirname in dirnames:
                if dirname.endswith(searchitem):
                    dirname = os.path.join(dirpath, dirname)
                    name = "big-craftable.json"
                    data = pyjson5.load(open(os.path.join(dirname, name), encoding="utf-8"))
                    if "Recipe" in data and "Ingredients" in data["Recipe"]:
                        for item in data["Recipe"]["Ingredients"]:
                            if item["Object"] in vanillaids:
                                objectname = vanillaids[item["Object"]]
                            else:
                                objectname = item["Object"]
                            tocraft[objectname] = item["Count"]
    for element, quantity in tocraft.items():
        total = int(quantity) * int(amount)
        chests = 0
        stacks = 0
        substack = 0
        if total > 35964:  # a full chest
            chests, overflow = divmod(total, 35964)
            # print(chests)
            # print(overflow)
            stacks, substack = divmod(overflow, 999)
            output = str(total) + " (" + str(chests) + " chest + " + str(stacks) + " stack + " + str(substack) + ")"
        elif total > 999:
            stacks, substack = divmod(total, 999)
            output = str(total) + " (" + str(stacks) + " stack + " + str(substack) + ")"
        else:
            output = str(total)
        print(element + ": " + output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-master', action='store_true', help='output full craft master CSVs (default)')
    parser.add_argument('-math', '-m', action='store_true', help='calculate ingredients for a recipe, format example -math 10 Mayonnaise Machine')
    parser.add_argument('calculation', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        mode = "master"
    elif args.math:
        mode = "math"
    else:
        mode = "master"

    if mode == "master":
        craftmaster()
    else:
        quantity = args.calculation.pop(0)
        if not quantity.isnumeric():
            print("No quantity detected.")
        searchterm = " ".join(args.calculation).title()
        calculate(quantity, searchterm)
