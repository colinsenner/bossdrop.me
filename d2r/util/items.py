import pandas as pd
import os
import numpy as np
from .common import get_data_dir


def EquipGroupLevel(level):
    if level % 3 == 0:
        return level
    return level + (3 - (level % 3))


def get_base_item_level(row, other_df):
    base_item_level = row['base_item_level']

    # Lookup the item level in the other dataframe
    if pd.isna(base_item_level):
        if row.code in other_df.index:
            return other_df.loc[row.code].level
    return base_item_level


def get_base_item_type(row, other_df, type_string):
    base_item_type = row['base_item_type']

    if pd.isna(base_item_type):
        if row.code in other_df.index:
            return type_string
    return base_item_type


def get_tc_group(row):
    base_tc_class = ''

    base_item_type = row['base_item_type']
    base_item_level = row['base_item_level']

    # Objects in Misc.txt have their TC set by their 'code'
    if base_item_type == 'misc':
        base_tc_class = row['code']
    else:
        # Weapons and Armors get assigned to dynamically created TCs called 'weap' and 'armo'
        tc_level = EquipGroupLevel(base_item_level)
        base_tc_class = f"{base_item_type}{int(tc_level)}"

    return base_tc_class


def get_misc():
    misc = pd.read_csv(os.path.join(get_data_dir(), 'Misc.txt'), sep='\t')
    #runes = misc[misc.name.str.contains("Rune")]

    misc.dropna(subset=['level'], inplace=True)

    # Most of these are found in these patch files
    # https://github.com/fabd/diablo2/blob/17d60a1085151a640b164e047b4e0afb179af254/code/d2_113_data/TBL/ENG/patchstring.txt
    name_to_friendly_name = {
        'Pandemonium Key 1': 'Key of Terror',
        'Pandemonium Key 2': 'Key of Hate',
        'Pandemonium Key 3': 'Key of Destruction',
    }
    misc['name'] = misc['name'].apply(lambda name: name_to_friendly_name[name] if name in name_to_friendly_name.keys() else name)

    # Drop rows with name == 'Not used"
    names_to_drop = ['Not used', 'gold']
    misc.drop(misc[misc['name'].isin(names_to_drop)].index, inplace=True)
    misc.drop(misc[misc['name'] == 'Not used'].index, inplace=True)

    # Only keep these columns, and format them the same as unique_items
    misc = misc[['name', 'level', 'code']]

    misc = misc.rename( columns={ "name":"index",
                                "level":"lvl",
                                "code":"tc_group"})

    return misc


def get_unique_items():
    #
    # Read UniqueItems.txt and setup the dataframe to only include enabled items with codes
    #
    unique_items = pd.read_csv(os.path.join(get_data_dir(), 'UniqueItems.txt'), sep='\t')

    df1 = unique_items.copy()

    df1 = df1[df1['enabled'] == 1.0]
    df1 = df1[df1['code'].notna()]
    df1 = df1[df1['lvl'] != 0]

    # Add additional columns, we'll calculate these below
    df1['base_item_level'] = np.nan
    df1['base_item_type'] = np.nan
    df1['tc_group'] = np.nan

    # From what I can tell no monster has a drop for the item `Hellfire Torch`
    # Because it's coded `cm2` and it's level 110, Diablo Clone shows he can drop it (in Normal and NM)
    # But he definitely can't, drop the entry for now
    df1.drop(df1[df1['index'] == 'Hellfire Torch'].index, inplace=True)

    # Read Weapons.txt to find the base item type's level
    weapons = pd.read_csv(os.path.join(get_data_dir(), 'Weapons.txt'), sep='\t')
    weapons.set_index('code', inplace=True, drop=True, verify_integrity=True)

    # Read Armor.txt to find the base item type's level
    armor = pd.read_csv(os.path.join(get_data_dir(), 'Armor.txt'), sep='\t')
    armor.set_index('code', inplace=True, drop=True, verify_integrity=True)

    # Read Misc.txt to find the base item type's level
    misc = pd.read_csv(os.path.join(get_data_dir(), 'Misc.txt'), sep='\t')
    misc.set_index('code', inplace=True, drop=True, verify_integrity=True)

    #
    # Calculations
    #

    # Lookup their base items levels
    df1['base_item_level'] = df1.apply(get_base_item_level, args=(weapons,), axis=1)
    df1['base_item_level'] = df1.apply(get_base_item_level, args=(armor,), axis=1)
    df1['base_item_level'] = df1.apply(get_base_item_level, args=(misc,), axis=1)

    assert df1['base_item_level'].isnull().sum() == 0, f"One or more of the `base_item_levels` are null"

    # Lookup their base items types
    df1['base_item_type'] = df1.apply(get_base_item_type, args=(weapons, "weap"), axis=1)
    df1['base_item_type'] = df1.apply(get_base_item_type, args=(armor, "armo"), axis=1)
    df1['base_item_type'] = df1.apply(get_base_item_type, args=(misc, 'misc'), axis=1)

    assert df1['base_item_type'].isnull().sum() == 0, f"One or more of the `base_item_types` are null"

    # Assign their base TC class
    df1['tc_group'] = df1.apply(get_tc_group, axis=1)

    # Hack Hack Hack
    # Annihilus is a 'cm1' code but can only be dropped by dclone
    # Change it's group so it'll be found in dclone's dropped tcs (which reference it by 'Annihilus' in TreasureClassEx.txt)
    df1.at[df1['index'] == 'Annihilus', 'tc_group'] = 'Annihilus'

    # Make some of the item names a bit more friendly to search ('The Stone of Jordan' => add 'soj', and 'Shako' to 'Harlequin Crest')
    df1.at[df1['index'] == 'Harlequin Crest', 'index'] = 'Harlequin Crest (Shako)'
    df1.at[df1['index'] == 'The Stone of Jordan', 'index'] = 'The Stone of Jordan (soj)'

    # 'Rainbow Facet' - shows up multiple times, they're all the same level with the same code, remove them
    df1.drop_duplicates(subset="index", inplace=True)

    # Keep only these
    df1 = df1[['index', 'lvl', 'tc_group']]

    return df1
