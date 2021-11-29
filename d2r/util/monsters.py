import os

import numpy as np
import pandas as pd

from .common import get_data_dir


def get_all_treasure_classes(row, difficulty):
    column_name = ''

    if difficulty == 'normal':
        column_name = 'TreasureClass3'
    elif difficulty == 'nightmare':
        column_name = 'TreasureClass3(N)'
    elif difficulty == 'hell':
        column_name = 'TreasureClass3(H)'
    else:
        raise Exception("Unsupported difficulty option")

    all_tcs_from_class

    return [column_name]


def get_bosses():
    #
    # Read MonStats.txt and setup the dataframe to only include enabled items with codes
    #
    bosses = pd.read_csv(os.path.join(get_data_dir(), 'MonStats.txt'), sep='\t')

    bosses = bosses[bosses['boss'] == 1]

    # Get all the TC items each can drop
    bosses['treasure_drops'] = bosses.apply(get_all_treasure_classes, args=('normal',), axis=1)
    bosses['treasure_drops(N)'] = bosses.apply(get_all_treasure_classes, args=('nightmare',), axis=1)
    bosses['treasure_drops(H)'] = bosses.apply(get_all_treasure_classes, args=('hell',), axis=1)

    columns_to_keep = ['Id', 'NameStr', 'Level', 'Level(N)', 'Level(H)', 'boss', 'treasure_drops', 'treasure_drops(N)', 'treasure_drops(H)']
    bosses = bosses[columns_to_keep]

    return bosses
