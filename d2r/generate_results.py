import json
from os import path
from shutil import copyfile

import util.items
import util.monsters


def main():
    # Save for debugging
    unique_items = util.items.get_unique_items()
    unique_items.to_json(path.join("generated", "uniqueitems.json"), orient='records', indent=2)

    misc = util.items.get_misc()
    misc.to_json(path.join("generated", "misc.json"), orient='records', indent=2)

    bosses = util.monsters.get_bosses()
    bosses.to_json(path.join("generated", "bosses.json"), orient='records', indent=2)

    superuniques = util.monsters.get_superuniques()
    superuniques.to_json(path.join("generated", "superuniques.json"), orient='records', indent=2)

    # Put misc in the unique_items list
    unique_items = unique_items.append(misc)

    # Add superunique monsters to our list of bosses
    bosses = bosses.append(superuniques)

    results = dict()
    results['unique_items'] = unique_items.to_dict(orient='records')
    results['bosses'] = bosses.to_dict(orient='records')

    # Write our file for the JS side
    results_file = path.join("generated", "results.json")
    with open(results_file, "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Copy the results to the JS directory
    copyfile(results_file, "../src/static/results.json")

if __name__ == '__main__':
    main()
