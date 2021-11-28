import pandas as pd
import os
import json
import numpy as np
from .common import get_data_dir


def EquipGroupLevel(level):
    if level % 3 == 0:
        return level
    return level + (3 - (level % 3))


def get_unique_items():
    df = pd.read_csv(os.path.join(get_data_dir(), 'UniqueItems.txt'), sep='\t')

    # Drop rows where the items aren't enabled
    df = df[df['enabled'] == 1.0]

    # Drop rows where we have NaN is code column
    df = df[df['code'].notna()]

    #
    # Read Weapons.txt to find the base item type's level
    #
    df_weapons = pd.read_csv(os.path.join(get_data_dir(), 'Weapons.txt'), sep='\t')

    keep_columns = ['name', 'type', 'code', 'level']
    df = df.merge(df_weapons[keep_columns], how='left', on='code', validate='many_to_one')

    #
    # Read Armor.txt to find the base item type's level
    #
    df_armor = pd.read_csv(os.path.join(get_data_dir(), 'Armor.txt'), sep='\t')

    df = df.merge(df_armor[keep_columns], how='left', on='code', validate='many_to_one')

    print(df.head())
    print()

    # for index, row in df.iterrows():
    #     item_name = row['index']

    #     base_item = df_weapons.loc[df_weapons.code == row.code]

    #     print(base_item['level'])

    #     assert len(base_item) == 0 or len(base_item) == 1, f"Multiple items found in 'Weapons.txt' with code '{row.code}'"

    #     # Not found in this file
    #     if base_item.empty:
    #         continue

    #     # assert not base_item.empty, f"Couldn't find item code '{row.code}' for UniqueItem '{item_name}' in 'Weapons.txt'"

    #     df.at[index, 'base_item_level'] = base_item['level']
    #     df.at[index, 'base_tc_class'] = f"weap{base_item.iloc[0].level}"

    #
    # Read Armor.txt to find the base item type's level
    #



    print(df.head(100))

    return df
