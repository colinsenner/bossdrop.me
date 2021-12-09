from os import path

import numpy as np
import pandas as pd

from .common import get_base_file, get_generated_dir

def get(version):
    df = get_base_file(version, "misc.txt")

    df.dropna(subset=['level'], inplace=True)

    df['rarity_type'] = 'misc'

    # Drop rows with name == 'Not used" and "gold"
    names_to_drop = ['Not used', 'gold']
    df.drop(df[df['name'].isin(names_to_drop)].index, inplace=True)
    df.drop(df[df['name'] == 'Not used'].index, inplace=True)

    # Only keep these columns, and format them the same as unique_items
    df = df.rename( columns={ "name":"index",
                                "level":"lvl",
                                "code":"tc_group"})

    # Save for debugging
    df.to_json(path.join(get_generated_dir(), "misc.json"), orient='records', indent=2)

    return df[['index', 'lvl', 'rarity_type', 'tc_group']]
