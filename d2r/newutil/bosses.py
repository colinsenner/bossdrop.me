from os import path

import numpy as np
import pandas as pd

from .common import get_base_file, get_generated_dir
from .treasureclasses import get_treasure_class_for_difficulty, get_all_treasure_classes


def get(version):
    monstats = get_base_file(version, "monstats.txt")
    treasureclassex = get_base_file(version, "treasureclassex.txt")

    df = monstats.copy()

    df = df[df['boss'] == 1]

    # Remove some bosses we don't want to show up
    # e.g. We don't want
    boss_ids_to_keep = ['andariel', 'duriel', 'mephisto',
                        'diablo', 'summoner', 'nihlathakboss',
                        'baalcrab', 'diabloclone', 'uberandariel',
                        'uberduriel', 'uberizual', 'uberbaal']

    df = df.loc[df['Id'].isin(boss_ids_to_keep)]

    # df['TC'] = df.apply(get_treasure_class_for_difficulty, args=(
    #     treasureclassex, 'TreasureClass3',), axis=1)
    # df['TC(N)'] = df.apply(get_treasure_class_for_difficulty,
    #                        args=(treasureclassex, 'TreasureClass3(N)',), axis=1)
    # df['TC(H)'] = df.apply(get_treasure_class_for_difficulty,
    #                        args=(treasureclassex, 'TreasureClass3(H)',), axis=1)

    # Get all the TC items each can drop
    # Sometime around v2.7.0 they changed the column to "TreasureClassUnique"
    df['TC'] = df.apply(get_treasure_class_for_difficulty, args=(
        treasureclassex, 'TreasureClassUnique',), axis=1)
    df['TC(N)'] = df.apply(get_treasure_class_for_difficulty,
                           args=(treasureclassex, 'TreasureClassUnique(N)',), axis=1)
    df['TC(H)'] = df.apply(get_treasure_class_for_difficulty,
                           args=(treasureclassex, 'TreasureClassUnique(H)',), axis=1)

    # Change bosses NameStr's to be a bit more user friendly
    id_to_namestr_mapping = {
        'izual': 'Izual',
        'diabloclone': 'Diablo Clone',
        'baalcrab': 'Baal',
        'nihlathakboss': 'Nihlathak',
        'uberandariel': 'Lilith',
        'ubermephisto': 'Uber Mephisto',
        'uberdiablo': 'Uber Diablo',
        'uberizual': 'Uber Izual',
        'uberduriel': 'Uber Duriel',
        'uberbaal': 'Uber Baal',
    }

    df['NameStr'] = df['Id'].apply(
        lambda Id: id_to_namestr_mapping[Id] if Id in id_to_namestr_mapping.keys() else Id)

    # We don't want diablo clone showing results for normal and nightmare
    # It might be possible for him to spawn in those difficulties, but it's visual clutter
    # and confusing for users
    # We're going to just set their level on Normal and NM to a very low value
    # So it won't pass the high enough level check
    df.loc[df['Id'] == 'diabloclone', 'Level'] = -9999
    df.loc[df['Id'] == 'diabloclone', 'Level(N)'] = -9999

    # Save for debugging
    df.to_json(path.join(get_generated_dir(), "monstats.json"),
               orient='records', indent=2)

    return df[['Id', 'NameStr', 'Level', 'Level(N)', 'Level(H)', 'boss', 'TC', 'TC(N)', 'TC(H)']]
