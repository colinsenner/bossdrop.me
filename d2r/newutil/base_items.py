from os import path

import pandas as pd


def calc_base_item_level(row, other_df):
    base_item_level = row['base_item_level']

    # Lookup the item level in the other dataframe
    if pd.isna(base_item_level):
        items = other_df.loc[other_df['code'] == row.code]

        assert len(items) <= 1, f"Found multiple items with code '{row.code}'!"

        if len(items) == 1:
            item = items.iloc[0]
            return item.level

    return base_item_level


def calc_base_item_type(row, other_df, type_string):
    base_item_type = row['base_item_type']

    if pd.isna(base_item_type):
        items = other_df.loc[other_df['code'] == row.code]

        assert len(items) <= 1, f"Found multiple items with code '{row.code}'!"

        if len(items) == 1:
            return type_string
    return base_item_type


def calc_tc_group(row):
    base_tc_class = ''

    base_item_type = row['base_item_type']
    base_item_level = row['base_item_level']

    # Objects in Misc.txt have their TC set by their 'code'
    if base_item_type == 'misc':
        base_tc_class = row['code']
    else:
        # Weapons and Armors get assigned to dynamically created TCs called 'weap' and 'armo'
        tc_level = calc_dynamic_tc_level(base_item_level)
        base_tc_class = f"{base_item_type}{int(tc_level)}"

    return base_tc_class


def calc_dynamic_tc_level(level):
    if level % 3 == 0:
        return level
    return level + (3 - (level % 3))
