import os
from collections import deque

import pandas as pd

import common

data_dir = os.path.join(os.path.dirname(__file__), 'data')

treasureClassEx = common.create_dictionary(os.path.join(data_dir, "TreasureClassEx.txt"))


def main():
    boss = 'Mephisto (H)'
    item = "Tyrael's Might"
    boss_tcs = AllTreasureClasses(boss)

    print(boss_tcs)

    equip_group = DropGroupName("armo", 85)

    print("--------------------")
    print(f"Can {boss} drop {item}?")
    print(f"{equip_group in boss_tcs}")



def EquipGroupLevel(level):
    return level + (3 - (level % 3))


def DropGroupName(prefix, level):
    group_level = EquipGroupLevel(level)
    return f'{prefix}{group_level}'


def GetSubTreasureClasses(treasure_class_name):
    """Returns all sub treasure classes from a treasure_class_name
    e.g.
        For 'Duriel' returns ['tsc', 'Duriel - Base']

    TreasureClassEx.txt
        Treasure Class ... Item1 ... Item2         ... Item3
        Duriel             tsc       Duriel - Base     NaN

    Args:
        treasure_class_name ([str]): name of the row in the column 'Treasure Class'

    Returns:
        [str]: List of all Item1-10 strings that aren't NaN for the matching row
    """
    treasure_classes = []

    for row in treasureClassEx:
        if row['Treasure Class'] == treasure_class_name:
            # Go through item1 - item10
            item_columns = [f"Item{i}" for i in range(1,11)]

            for col in item_columns:
                tc = row[col]

                # Pandas columns without data return NaN
                if not pd.isna(tc):
                    treasure_classes.append(tc)

    return treasure_classes


def AllTreasureClasses(treasure_class_name):
    """Returns every droppable Treasure Class for a given Treasure Class

    Args:
        treasure_class_name ([str]): name of the row in the column 'Treasure Class'

    Returns:
        [str]: List of every Treasure Class including all sub TCs for a given string
    """
    q = deque([treasure_class_name])
    all_treasure_classes = []

    while q:
        entry = q.popleft()

        # Get the column 'monster' from TreasureClassEx.txt and find all Item1-10 entries
        # Add them to our queue
        for tc in GetSubTreasureClasses(entry):
            q.append(tc)

        all_treasure_classes.append(entry)
    return all_treasure_classes


def AllTreasureClassesRecursive(treasure_class_name, all_treasure_classes=[]):
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

    for row in treasureClassEx:
        if row['Treasure Class'] == treasure_class_name:
            # Go through columns Item1-10
            item_columns = [f"Item{i}" for i in range(1,11)]

            for col in item_columns:
                entry = row[col]
                AllTreasureClassesRecursive(entry, all_treasure_classes)
    return all_treasure_classes


if __name__ == '__main__':
    main()
