import os

import numpy as np
import pandas as pd

from .common import get_data_dir


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


def get_bosses():
    #
    # Read MonStats.txt and setup the dataframe to only include enabled items with codes
    #
    bosses = pd.read_csv(os.path.join(get_data_dir(), 'MonStats.txt'), sep='\t')

    bosses = bosses[bosses['boss'] == 1]

    # Get all the TC items each can drop
    bosses['tcs'] = bosses.apply(get_all_treasure_classes_for_difficulty, args=('normal',), axis=1)
    bosses['tcs(N)'] = bosses.apply(get_all_treasure_classes_for_difficulty, args=('nightmare',), axis=1)
    bosses['tcs(H)'] = bosses.apply(get_all_treasure_classes_for_difficulty, args=('hell',), axis=1)

    columns_to_keep = ['Id', 'NameStr', 'Level', 'Level(N)', 'Level(H)', 'boss', 'tcs', 'tcs(N)', 'tcs(H)']
    bosses = bosses[columns_to_keep]

    return bosses
