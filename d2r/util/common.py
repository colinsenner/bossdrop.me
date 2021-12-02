import os
from os import path

def get_data_dir():
    return path.join(os.getcwd(), "data")

def get_superunique_area(superunique_name):
    # Maps entries in Superuniques.txt in column 'Superunique" to the areas they're in in 'Levels.txt'
    superunique_area_mapping = {
        "Ancient Kaa the Soulless": "Act 2 - Valley of the Kings",
        "Baal Subject 1": "Act 5 - Throne Room",
        "Baal Subject 2": "Act 5 - Throne Room",
        "Baal Subject 3": "Act 5 - Throne Room",
        "Baal Subject 4": "Act 5 - Throne Room",
        "Baal Subject 5": "Act 5 - Throne Room",
        "Beetleburst": "Act 2 - Desert 3",
        "Bishibosh": "Act 1 - Wilderness 2",
        "Bloodwitch the Wild": "Act 2 - Tomb 2 Treasure",
        "Boneash": "Act 1 - Cathedral",
        "Bonebreak": "Act 1 - Crypt 1 A",
        "Bonesaw Breaker": "Act 5 - Ice Cave 2",
        "Bremm Sparkfist": "Act 3 - Mephisto 3",
        "Coldcrow": "Act 1 - Cave 2",
        "Coldworm the Burrower": "Act 2 - Lair 1 Treasure",
        "Corpsefire": "Act 1 - Cave 1",
        "Dac Farren": "Act 5 - Siege 1",
        "Dark Elder": "Act 2 - Desert 4",
        "Eyeback Unleashed": "Act 5 - Barricade 1",
        "Fangskin": "Act 2 - Tomb 3 Treasure",
        "Fire Eye": "Act 2 - Basement 3",
        "Frozenstein": "Act 5 - Ice Cave 1A",
        "Geleb Flamefinger": "Act 3 - Travincal",
        "Grand Vizier of Chaos": "Act 4 - Diablo 1",
        "Griswold": "Act 1 - Tristram",
        "Icehawk Riftwing": "Act 3 - Sewer 1",
        "Infector of Souls": "Act 4 - Diablo 1",
        "Ismail Vilehand": "Act 3 - Travincal",
        "Lord De Seis": "Act 4 - Diablo 1",
        "Maffer Dragonhand": "Act 3 - Mephisto 3",
        "Nihlathak Boss": "Act 5 - Temple Boss",
        "Pindleskin": "Act 5 - Temple Entrance",
        "Pitspawn Fouldog": "Act 1 - Jail 2",
        "Radament": "Act 2 - Sewer 1 C",
        "Rakanishu": "Act 1 - Wilderness 3",
        "Sarina the Battlemaid": "Act 3 - Temple 1",
        "Sharp Tooth Sayer": "Act 5 - Barricade 1",
        "Siege Boss": "Act 5 - Siege 1",
        "Snapchip Shatter": "Act 5 - Ice Cave 3A",
        "Stormtree": "Act 3 - Jungle 3",
        "The Countess": "Act 1 - Crypt 3 E",
        "The Cow King": "Act 1 - Moo Moo Farm",
        "The Feature Creep": "Act 4 - Lava 1",
        "Leatherarm": "Act 2 - Tomb 1 Treasure",
        "The Smith": "Act 1 - Barracks",
        "Threash Socket": "Act 5 - Barricade 2",
        "Toorc Icefist": "Act 3 - Travincal",
        "Treehead WoodFist": "Act 1 - Wilderness 4",
        "Web Mage the Burning": "Act 3 - Spider 2",
        "Witch Doctor Endugu": "Act 3 - Dungeon 2 Treasure",
        "Wyand Voidfinger": "Act 3 - Mephisto 3",
    }

    if superunique_name not in superunique_area_mapping.keys():
        return None

    return superunique_area_mapping[superunique_name]


def rename_superuniques(superunique_name):
    renamed_superuniques = {
        "Baal Subject 1": "Colenzo the Annihilator",
        "Baal Subject 2": "Achmel the Cursed",
        "Baal Subject 3": "Bartuc the Bloody",
        "Baal Subject 4": "Ventar the Unholy",
        "Baal Subject 5": "Lister the Tormentor",
        "Sarina the Battlemaid": "Battlemaid Sarina",
        "Siege Boss": "Shenk the Overseer",
        "The Feature Creep": "Hephasto the Armorer",
        "Leatherarm": "Creeping Feature",
        "Threash Socket": "Thresh Socket",
        "Web Mage the Burning": "Sszark the Burning"
    }

    if superunique_name in renamed_superuniques.keys():
        return renamed_superuniques[superunique_name]

    return superunique_name