import os
from os import path
import util.items
import json


def main():
    # UniqueItems.txt
    df = util.items.get_unique_items()

    # Add name column
    df = df[['index', 'lvl', 'tc_group']]

    print(df.sample(10))

    # Save for debugging
    df.to_csv(path.join("generated", "unique_items.csv"))
    df.to_json(path.join("generated", "unique_items.json"), orient='records', indent=2)

    results = dict()
    results['unique_items'] = df.to_dict(orient='records')

    # Write our file for the JS side
    with open(path.join("generated", "results.json"), "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
