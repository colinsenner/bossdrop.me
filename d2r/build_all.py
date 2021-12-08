import json
from os import path
from shutil import copyfile

import newutil.common as common
import newutil.misc
import newutil.sets
import newutil.uniqueitems
from newutil.translations import translate


def main():
    game_version = "1.1.67358"

    results = {}

    translation_dir = common.get_translation_dir(game_version)

    # uniqueitems
    uniqueitems = newutil.uniqueitems.get(game_version)
    uniqueitems['index'] = uniqueitems['index'].apply(lambda index: translate(translation_dir, index))

    # sets
    sets = newutil.sets.get(game_version)
    sets['index'] = sets['index'].apply(lambda index: translate(translation_dir, index))

    # misc items (Runes, etc)
    misc = newutil.misc.get(game_version)
    misc['index'] = misc['tc_group'].apply(lambda code: translate(translation_dir, code))
    misc.dropna(subset=['index'], inplace=True)

    # Combine all items
    searchable_items = []
    searchable_items += uniqueitems.to_dict(orient="records")
    searchable_items += sets.to_dict(orient="records")
    searchable_items += misc.to_dict(orient="records")

    results['searchable_items'] = searchable_items


    # Write our file for the JS side
    results_file = path.join("generated", "results.json")
    with open(results_file, "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Copy the results to the JS directory
    copyfile(results_file, "../src/static/results.json")

    print("results.json generated and copied to /src/static/ directory.")

if __name__ == '__main__':
    main()
