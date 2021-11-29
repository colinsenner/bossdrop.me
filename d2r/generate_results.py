import json
import os
from os import path

import util.items
import util.monsters


def main():
    # UniqueItems.txt
    unique_items = util.items.get_unique_items()
    runes = util.items.get_runes()

    # Save for debugging
    unique_items.to_json(path.join("generated", "unique_items.json"), orient='records', indent=2)
    runes.to_json(path.join("generated", "runes.json"), orient='records', indent=2)

    # Put runes in the unique_items list
    unique_items = unique_items.append(runes)

    bosses = util.monsters.get_bosses()

    bosses.to_json(path.join("generated", "bosses.json"), orient='records', indent=2)

    results = dict()
    results['unique_items'] = unique_items.to_dict(orient='records')
    results['bosses'] = bosses.to_dict(orient='records')

    # Write our file for the JS side
    with open(path.join("generated", "results.json"), "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
