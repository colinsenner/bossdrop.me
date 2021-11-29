import pandas as pd
import os
import json
import numpy as np
from .common import get_data_dir, remove_duplicate_rows


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


def get_runes():
    #
    # Read Misc.txt to find the base item type's level
    #
    misc = pd.read_csv(os.path.join(get_data_dir(), 'Misc.txt'), sep='\t')
    misc.set_index('code', inplace=True, drop=True, verify_integrity=True)

    #
    # Add runes to our items list
    #
    runes = misc[misc.name.str.contains("Rune")]

    # misc is indexed on 'code', so we need to assign it's code to another column
    # so it'll propogate when appended to the other df
    runes.loc[runes.index, 'code'] = runes.index

    # Only keep these columns
    runes = runes[['name', 'code']]
    runes.set_index('name', inplace=True)

    return runes


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

    # 'Rainbow Facet' - shows up multiple times, they're all the same level with the same code, remove them
    df1 = remove_duplicate_rows(df1)

    return df1
