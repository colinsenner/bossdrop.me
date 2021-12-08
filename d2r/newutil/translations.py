import json
import os


def get(translation_dir):
    results = dict()

    results['item-names'] = load(os.path.join(translation_dir, 'item-names.json'))
    results['item-runes'] = load(os.path.join(translation_dir, 'item-runes.json'))
    results['monsters'] = load(os.path.join(translation_dir, 'monsters.json'))

    return results


def load(filepath):
    contents = None
    with open(filepath, "rt", encoding='utf-8-sig') as f:
        contents = json.load(f)
    return contents
