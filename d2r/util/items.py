import pandas as pd
import os
import json
import numpy as np
from .common import get_data_dir


def EquipGroupLevel(level):
    if level % 3 == 0:
        return level
    return level + (3 - (level % 3))


def find_level(row, other_df):
    base_item_level = row['base_item_level']

    # Lookup the item level in the other dataframe
    if pd.isna(base_item_level):
        if row.code in other_df.index:
            return other_df.loc[row.code].level
    return base_item_level


def get_base_tc_class(row):
    pass


def remove_duplicate_rows(df):
    '''
    Returns a dataframe with duplicate indexes removed
    '''
    return df[~df.index.duplicated(keep='first')]


def get_unique_items():
    #
    # Read UniqueItems.txt and setup the dataframe to only include enabled items with codes
    #
    unique_items = pd.read_csv(os.path.join(get_data_dir(), 'UniqueItems.txt'), sep='\t')
    unique_items.set_index('index', inplace=True, drop=True)

    df1 = unique_items.copy()

    df1 = df1[df1['enabled'] == 1.0]
    df1 = df1[df1['code'].notna()]

    # Add additional columns, we'll calculate these below
    df1['base_item_level'] = np.nan
    df1['base_tc_class'] = np.nan

    #
    # Read Weapons.txt to find the base item type's level
    #
    weapons = pd.read_csv(os.path.join(get_data_dir(), 'Weapons.txt'), sep='\t')
    weapons.set_index('code', inplace=True, drop=True, verify_integrity=True)

    #
    # Read Armor.txt to find the base item type's level
    #
    armor = pd.read_csv(os.path.join(get_data_dir(), 'Armor.txt'), sep='\t')
    armor.set_index('code', inplace=True, drop=True, verify_integrity=True)

    #
    # Read Misc.txt to find the base item type's level
    #
    misc = pd.read_csv(os.path.join(get_data_dir(), 'Misc.txt'), sep='\t')
    misc.set_index('code', inplace=True, drop=True, verify_integrity=True)

    #
    # Add runes to our items list
    #
    # runes = misc[misc.name.str.contains("Rune")]

    # # misc is indexed on 'code', so we need to assign it's code to another column
    # # so it'll propogate when appended to the other df
    # runes.loc[runes.index, 'code'] = runes.index

    # # Only keep these columns
    # runes = runes[['name', 'code']]
    # runes.set_index('name', inplace=True)

    # df1 = df1.append(runes)

    #
    # Calculate
    # Lookup their base items levels
    df1['base_item_level'] = df1.apply(find_level, args=(weapons,), axis=1)
    df1['base_item_level'] = df1.apply(find_level, args=(armor,), axis=1)
    df1['base_item_level'] = df1.apply(find_level, args=(misc,), axis=1)

    assert df1['base_item_level'].isnull().sum() == 0, f"One or more of the base_item_levels are null"

    # Assign their base TC class
    df1['base_tc_class'] = df1.apply(get_base_tc_class, axis=1)

    # 'Rainbow Facet' - shows up multiple times, they're all the same level with the same code, remove them
    df1 = remove_duplicate_rows(df1)

    return df1
