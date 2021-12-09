import pandas as pd

cached_tcs = {}


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


def get_treasure_class_for_difficulty(row, treasureclassex_df, column_name):
    global cached_tcs

    treasure_class_name = row[column_name]

    if pd.isna(treasure_class_name):
        return []

    print(f"Getting TCs for '{treasure_class_name}'")

    if treasure_class_name in cached_tcs:
        return cached_tcs[treasure_class_name]

    tcs = get_all_treasure_classes(row[column_name], treasureclassex_df, [])

    # Cache for immediate lookup next time
    cached_tcs[treasure_class_name] = tcs

    # Sometimes there isn't an entry (uberbaal can't spawn on normal or nightmare, so can't drop anything)
    # Rather than them getting assigned null, assign them an empty list
    if tcs == None:
        tcs = []

    return tcs
