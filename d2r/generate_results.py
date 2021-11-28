import os
from os import path
import pandas as pd
import util.items

def main():
    # UniqueItems.txt
    df = util.items.get_unique_items()

    df = df[['lvl', 'base_item_level']]

    df.to_json("results.json", orient='index', indent=2)


if __name__ == '__main__':
    main()

