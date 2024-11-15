import json
import os
from shutil import copyfile

import newutil.common as common
import newutil.misc
import newutil.sets
import newutil.bosses
import newutil.superuniques
import newutil.uniqueitems
from newutil.translations import translate


def main():
    game_version = "2.7.0"

    os.makedirs(common.get_generated_dir(), exist_ok=True)

    translation_dir = common.get_translation_dir(game_version)

    # uniqueitems
    uniqueitems = newutil.uniqueitems.get(game_version)
    uniqueitems['index'] = uniqueitems['index'].apply(
        lambda index: translate(translation_dir, index))

    # Add player friendly names to some items
    uniqueitems.loc[uniqueitems['index'] == 'Harlequin Crest',
                    'index'] = 'Harlequin Crest (Shako)'
    uniqueitems.loc[uniqueitems['index'] == 'The Stone of Jordan',
                    'index'] = 'The Stone of Jordan (SOJ)'

    # sets
    sets = newutil.sets.get(game_version)
    sets['index'] = sets['index'].apply(
        lambda index: translate(translation_dir, index))

    # misc items (Runes, etc)
    misc = newutil.misc.get(game_version)
    misc['index'] = misc['tc_group'].apply(
        lambda code: translate(translation_dir, code))
    misc.dropna(subset=['index'], inplace=True)

    # Combine all items
    items = list()
    items += uniqueitems.to_dict(orient="records")
    items += sets.to_dict(orient="records")
    items += misc.to_dict(orient="records")

    # Create results.json data
    results = dict()
    results['items'] = items

    # Get monsters
    bosses = newutil.bosses.get(game_version)

    superuniques = newutil.superuniques.get(game_version)
    superuniques['NameStr'] = superuniques['Id'].apply(
        lambda id: translate(translation_dir, id))

    monsters = list()
    monsters += bosses.to_dict(orient="records")
    monsters += superuniques.to_dict(orient="records")

    results['monsters'] = monsters

    # Write our file for the JS side
    results_file = os.path.join("generated", "results.json")
    with open(results_file, "wt", encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Copy the results to the JS directory
    copyfile(results_file, "../src/static/results.json")

    print("results.json generated and copied to /src/static/ directory.")


if __name__ == '__main__':
    main()
