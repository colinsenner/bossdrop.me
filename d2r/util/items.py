import pandas as pd
import os
import json
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

    # Merge both dfs together, on key 'code'
    df = df.merge(df_weapons, how='outer', on='code', validate='many_to_one')
    df['base_tc_group'] = 'weap'

    df = df[['index', 'lvl', 'code', 'name', 'level', 'base_tc_group']]

    print(df.head(100))

    return df
