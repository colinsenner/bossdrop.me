from os import path

import numpy as np
import pandas as pd

from .common import get_base_file, get_generated_dir
from .levels import get_superunique_area
from .treasureclasses import get_treasure_class_for_difficulty


def get(version):
    '''
    Superuniques are mobs like Pindleskin or Rakanishu
    '''

    superuniques = get_base_file(version, "superuniques.txt")
    monstats = get_base_file(version, "monstats.txt")
    levels = get_base_file(version, "levels.txt")
    treasureclassex = get_base_file(version, "treasureclassex.txt")

    df = superuniques.copy()

    # Drop rows where 'Name' is nan
    df.dropna(subset=['Name'], inplace=True)

    df['Level'] = np.nan
    df['Level(N)'] = np.nan
    df['Level(H)'] = np.nan
    df['boss'] = np.nan

    # Superunique monsters use a combination of MonStats and area Levels when not bosses and just monstats levels when bosses
    # To figure out a SuperUnique's NM and Hell levels we have to know what area they're in
    # I don't know a simple programatic way to look this up
    # maybe MonPresets.txt?
    df = df.apply(calculate_superunique_levels, args=(monstats, levels,), axis=1)

    # Drop mobs we couldn't calculate the level for
    df = df.dropna(subset=['Level', 'Level(N)', 'Level(H)'])

    # Drop superuniques we don't care about
    superuniques_to_keep = ['Baal Subject 1', 'Baal Subject 2', 'Baal Subject 3',
                            'Baal Subject 4', 'Baal Subject 5', 'Pindleskin',
                            'Ismail Vilehand', 'Toorc Icefist', 'Geleb Flamefinger',
                            'Bremm Sparkfist', 'Wyand Voidfinger', 'Maffer Dragonhand',
                            'The Countess', 'The Cow King', 'Lord De Seis',
                            'Grand Vizier of Chaos', 'Infector of Souls', 'Threash Socket']

    df = df[df['Superunique'].isin(superuniques_to_keep)]

    df['TC'] = df.apply(get_treasure_class_for_difficulty, args=(treasureclassex, 'TC',), axis=1)
    df['TC(N)'] = df.apply(get_treasure_class_for_difficulty, args=(treasureclassex, 'TC(N)',), axis=1)
    df['TC(H)'] = df.apply(get_treasure_class_for_difficulty, args=(treasureclassex, 'TC(H)',), axis=1)

    # Some superunique's were renamed in the expansion pack, apply those transformations here
    # Apply renaming from string.txt
    # strings = get_rename_mappings("string.txt")
    # su['Superunique'] = su['Superunique'].apply(rename_strings, args=(strings,))

    # # Apply renaming from expansionstring.txt
    # expansion_strings = get_rename_mappings("expansionstring.txt")
    # su['Superunique'] = su['Superunique'].apply(rename_strings, args=(expansion_strings,))

    # Add fields so it merges perfectly with bosses data
    df['Id'] = df['Superunique']
    df['NameStr'] = df['Superunique']

    # Wrong levels listed on this site
    # https://diablo.fandom.com/wiki/Wyand_Voidbringer
    # https://rankedboost.com/diablo-2/bosses/bonesaw-breaker/#sts=Diablo%202%20Bonesaw%20Breaker
    # https://rankedboost.com/diablo-2/bosses/frozenstein/#sts=Diablo%202%20Frozenstein

    # Nihlathak is wrong on all other sites?!? No, they're the ones who are wrong
    # https://rankedboost.com/diablo-2/bosses/nihlathak/#sts=Diablo%202%20Nihlathak
    # https://diablo.fandom.com/wiki/Nihlathak

    # Save for debugging
    df.to_json(path.join(get_generated_dir(), "superuniques.json"), orient='records', indent=2)

    return df[['Id', 'NameStr', 'Level', 'Level(N)', 'Level(H)', 'boss', 'TC', 'TC(N)', 'TC(H)']]


def calculate_superunique_levels(superunique, monstats, levels):
    '''
        Assigns the 'Level', 'Level(N)', 'Level(H)', columns to the correct values
    '''
    superunique_name = superunique['Superunique']
    mob_base = monstats.loc[superunique['Class'] == monstats['Id']]

    assert len(mob_base) == 1, f"Multiple mobs found with Class '{superunique['Class']}'"
    mob_base = mob_base.iloc[0]

    if pd.isna(mob_base['boss']):
        superunique['boss'] = 0
    else:
        superunique['boss'] = mob_base['boss']

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
            superunique['Level(N)'] = area['MonLvlEx(N)'] + 3
            superunique['Level(H)'] = area['MonLvlEx(H)'] + 3

    return superunique
