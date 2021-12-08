import json
from shutil import copyfile
from os import path

import newutil.common as common
import newutil.sets
from newutil.translations import translate
import newutil.uniqueitems


def main():
    game_version = "1.1.67358"

    results = {}

    excel_dir = common.get_excel_dir(game_version)
    translation_dir = common.get_translation_dir(game_version)

    # uniqueitems
    uniqueitems = newutil.uniqueitems.get(game_version)
    uniqueitems['index'] = uniqueitems['index'].apply(lambda index: translate(translation_dir, index))

    # sets
    sets = newutil.sets.get(game_version)
    sets['index'] = sets['index'].apply(lambda index: translate(translation_dir, index))

    print(sets.sample(15))

    # Translate the items
    #item1 = translate(translation_dir, "Lenyms Cord")

    # Write our file for the JS side
    results_file = path.join("generated", "results.json")
    with open(results_file, "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Copy the results to the JS directory
    copyfile(results_file, "../src/static/results.json")

    print("results.json generated and copied to /src/static/ directory.")

if __name__ == '__main__':
    main()
