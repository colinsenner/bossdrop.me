from os import path

import numpy as np
import pandas as pd

from .base_items import (
    calc_base_item_level,
    calc_base_item_type,
    calc_dynamic_tc_level,
    calc_tc_group,
)
from .common import get_base_file, get_excel_dir, get_generated_dir


def get(version):
    df = get_base_file(version, "uniqueitems.txt")

    # Make sure the items are enabled and have valid codes
    # items with lvl == 0 are quest items 'Amulet of the Viper'
    df = df[df["disabled"] != 1.0]
    df = df[df["spawnable"] != 0.0]
    df = df[
        df["spawnable"].notna()
    ]  # RotW update: Some new items are null for spawnable (Darkfear, Crack of the Heavens)
    df = df[df["code"].notna()]
    df = df[df["lvl"] != 0]

    # RotW update: Darkfear
    # Add additional columns, we'll calculate these below
    df["base_item_level"] = np.nan
    df["base_item_type"] = np.nan
    df["tc_group"] = np.nan
    df["rarity_type"] = "unique"

    weapons = get_base_file(version, "weapons.txt")
    armor = get_base_file(version, "armor.txt")
    misc = get_base_file(version, "misc.txt")

    #
    # Calculations
    #

    # Lookup their base items levels
    df["base_item_level"] = df.apply(calc_base_item_level, args=(weapons,), axis=1)
    df["base_item_level"] = df.apply(calc_base_item_level, args=(armor,), axis=1)
    df["base_item_level"] = df.apply(calc_base_item_level, args=(misc,), axis=1)

    assert df["base_item_level"].isnull().sum() == 0, (
        f"One or more of the `base_item_levels` are null"
    )

    # Lookup their base items types
    df["base_item_type"] = df.apply(calc_base_item_type, args=(weapons, "weap"), axis=1)
    df["base_item_type"] = df.apply(calc_base_item_type, args=(armor, "armo"), axis=1)
    df["base_item_type"] = df.apply(calc_base_item_type, args=(misc, "misc"), axis=1)

    assert df["base_item_type"].isnull().sum() == 0, (
        f"One or more of the `base_item_types` are null"
    )

    # Assign their base TC class
    df["tc_group"] = df.apply(calc_tc_group, axis=1)

    # Hack Hack Hack
    # Annihilus is a 'cm1' code but can only be dropped by dclone
    # Change its group so it'll be found in dclone's dropped tcs (which reference it by 'Annihilus' in TreasureClassEx.txt)
    df.loc[df["index"] == "Annihilus", "tc_group"] = "Annihilus"

    # 'Rainbow Facet' - shows up multiple times, they're all the same level with the same code, remove them
    df.drop_duplicates(subset="index", inplace=True)

    # Save for debugging
    df.to_json(
        path.join(get_generated_dir(), "uniqueitems.json"), orient="records", indent=2
    )

    return df[["index", "lvl", "rarity_type", "tc_group"]]
