import os

import numpy as np
import pandas as pd

from .common import get_data_dir, get_superunique_area, rename_superuniques


def get_all_treasure_classes(treasure_class_name, treasure_class_ex, all_treasure_classes=[]):
    """Returns every droppable Treasure Class for a given Treasure Class

    Args:
        treasure_class_name ([str]): name of the row in the column 'Treasure Class'

    Returns:
        [str]: List of every Treasure Class including all sub TCs for a given string
    """


    # Base case
    # Some values in 'Item#' are empty, pandas returns NaN
    if pd.isna(treasure_class_name):
        return

    all_treasure_classes.append(treasure_class_name)

    # Find this TC name in TreasureClassEx.txt
    df = treasure_class_ex[treasure_class_ex['Treasure Class'] == treasure_class_name]
    if df.empty:
        return

    # Go through columns 'Item1-10'
    for col in [f"Item{i}" for i in range(1,11)]:
        entry = df[col]

        if not entry.empty:
            get_all_treasure_classes(entry.values[0], treasure_class_ex, all_treasure_classes)

    return all_treasure_classes


def get_all_treasure_classes_for_difficulty(row, difficulty):
    treasure_class_ex = pd.read_csv(os.path.join(get_data_dir(), 'TreasureClassEx.txt'), sep='\t')

    column_name = ''

    if difficulty == 'normal':
        column_name = 'TreasureClass3'
    elif difficulty == 'nightmare':
        column_name = 'TreasureClass3(N)'
    elif difficulty == 'hell':
        column_name = 'TreasureClass3(H)'
    else:
        raise Exception("Unsupported difficulty option")

    print(f"Getting TCs for '{row.Id}'")
    tcs = get_all_treasure_classes(row[column_name], treasure_class_ex, [])

    # Sometimes there isn't an entry (uberbaal can't spawn on normal or nightmare, so can't drop anything)
    # Rather than them getting assigned null, assign them an empty list
    if tcs == None:
        tcs = []

    return tcs


def calculate_superunique_levels(superunique, monstats, levels):
    '''
        Assigns the 'Level', 'Level(N)', 'Level(H)', columns to the correct values
    '''
    superunique_name = superunique['Superunique']
    if superunique_name == 'Pindleskin':
        pass
    mob_base = monstats.loc[superunique['Class'] == monstats['Id']]

    assert len(mob_base) == 1, f"Multiple mobs found with Class '{superunique['Class']}'"
    mob_base = mob_base.iloc[0]

    # if the monster in MonStats is 'boss' == 1, you can just use their levels from this file
    if mob_base['boss'] == 1:
        superunique['Level'] = mob_base['Level']
        superunique['Level(N)'] = mob_base['Level(N)']
        superunique['Level(H)'] = mob_base['Level(H)']
    else:
        # In NM and Hell difficulties, superuniques mob level is calculated from the area level +3 (Champions +2) (Normal +0)
        area_name = get_superunique_area(superunique_name)

        # Some mobs were just completely removed from the game, and we don't care about them
        if area_name != None:
            area = levels.loc[levels['Name'] == area_name]
            assert len(area) == 1, f"Multiple levels found with Name '{area_name}'"
            area = area.iloc[0]

            # In normal difficulty, monster levels are set to the 'Level' field from MonStats
            superunique['Level'] = mob_base['Level'] + 3

            # NM and hell get the area level + 3
            superunique['Level(N)'] = area['MonLvl2Ex'] + 3
            superunique['Level(H)'] = area['MonLvl3Ex'] + 3

    return superunique


def get_superuniques():
    '''
    Superuniques are mobs like Pindleskin or Rakanishu
    '''
    su = pd.read_csv(os.path.join(get_data_dir(), 'SuperUniques.txt'), sep='\t')
    monstats = pd.read_csv(os.path.join(get_data_dir(), 'MonStats.txt'), sep='\t')
    levels = pd.read_csv(os.path.join(get_data_dir(), 'Levels.txt'), sep='\t')

    # Drop rows where 'Name' is nan
    su.dropna(subset=['Name'], inplace=True)

    su['Level'] = np.nan
    su['Level(N)'] = np.nan
    su['Level(H)'] = np.nan

    # su['TC'] = np.nan
    # su['TC(N)'] = np.nan
    # su['TC(H)'] = np.nan

    # Superunique monsters use a combination of MonStats and area Levels when not bosses and just monstats levels when bosses
    # To figure out a SuperUnique's NM and Hell levels we have to know what area they're in
    # I don't know a simple programatic way to look this up
    # maybe MonPresets.txt?
    su = su.apply(calculate_superunique_levels, args=(monstats, levels,), axis=1)

    # bosses fields
    #  {
    #    "Id":"andariel",
    #    "NameStr":"andariel",
    #    "Level":12.0,
    #    "Level(N)":49.0,
    #    "Level(H)":75.0,
    #    "boss":1.0,
    #    "TC":[],
    #    "TC(N)":[],
    #    "TC(H)":[]
    #  }

    #su = su[['Superunique', 'Name', 'Class', 'Level', 'Level(N)', 'Level(H)', 'TC', 'TC(N)', 'TC(H)']]

    # Some superunique's were renamed in the expansion pack, apply those transformations here
    su['Superunique'] = su['Superunique'].apply(rename_superuniques)



    # Set their TC's
    #su['TC'] = su.apply(get_all_treasure_classes_for_difficulty, args=('normal',), axis=1)

    # Wrong levels listed on this site
    # https://diablo.fandom.com/wiki/Wyand_Voidbringer
    # https://rankedboost.com/diablo-2/bosses/bonesaw-breaker/#sts=Diablo%202%20Bonesaw%20Breaker
    # https://rankedboost.com/diablo-2/bosses/frozenstein/#sts=Diablo%202%20Frozenstein

    # Nihlathak is wrong on all other sites?!? No, they're the ones who are wrong
    # https://rankedboost.com/diablo-2/bosses/nihlathak/#sts=Diablo%202%20Nihlathak
    # https://diablo.fandom.com/wiki/Nihlathak


    pd.set_option("display.max_rows", None)
    print(su.head(100))

    print(su.head(10))

    return su


def get_bosses():
    #
    # Read MonStats.txt and setup the dataframe to only include enabled items with codes
    #
    monstats = pd.read_csv(os.path.join(get_data_dir(), 'MonStats.txt'), sep='\t')

    monstats = monstats[monstats['boss'] == 1]

    # Remove some bosses we don't want to show up
    # e.g. We don't want
    boss_ids_to_keep = ['andariel', 'duriel', 'mephisto', 'diablo', 'summoner', 'nihlathakboss', 'baalcrab', 'diabloclone']
    monstats = monstats.loc[monstats['Id'].isin(boss_ids_to_keep)]

    # Get all the TC items each can drop
    monstats['TC'] = monstats.apply(get_all_treasure_classes_for_difficulty, args=('normal',), axis=1)
    monstats['TC(N)'] = monstats.apply(get_all_treasure_classes_for_difficulty, args=('nightmare',), axis=1)
    monstats['TC(H)'] = monstats.apply(get_all_treasure_classes_for_difficulty, args=('hell',), axis=1)

    columns_to_keep = ['Id', 'NameStr', 'Level', 'Level(N)', 'Level(H)', 'boss', 'TC', 'TC(N)', 'TC(H)']
    monstats = monstats[columns_to_keep]

    # Change bosses NameStr's to be a bit more user friendly
    id_to_namestr_mapping = {
        'izual': 'Izual',
        'diabloclone': 'Diablo Clone',
        'baalcrab': 'Baal',
        'nihlathakboss': 'Nihlathak',
        'ubermephisto': 'Uber Mephisto',
        'uberdiablo': 'Uber Diablo',
        'uberizual': 'Uber Izual',
        'uberduriel': 'Uber Duriel',
        'uberbaal': 'Uber Baal',
    }

    monstats['NameStr'] = monstats['Id'].apply(lambda Id: id_to_namestr_mapping[Id] if Id in id_to_namestr_mapping.keys() else Id)

    # We don't want diablo clone showing results for normal and nightmare
    # It is possible for him to spawn in those difficulties, but it's visual clutter
    # We're going to just set their level on Normal and NM to a very low value
    # So it won't pass the high enough level check
    monstats.at[monstats['Id'] == 'diabloclone', 'Level'] = -999
    monstats.at[monstats['Id'] == 'diabloclone', 'Level(N)'] = -999

    return monstats
