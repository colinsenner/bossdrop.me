import json
import os

from shutil import copyfile
import numpy as np

__translations = None


def translate(dir, name, locale='enUS'):
    global __translations

    if __translations == None:
        __translations = __get(dir)

    items = list(filter(lambda item: item['Key'] == name, __translations))

    if len(items) == 0:
        print(f"Couldn't find a translation for '{name}'. This is not necessarily a problem, but this item will not show up in the results list")
        return np.nan

    assert len(items) == 1, f"Multiple keys found for name '{name}', can't translate."

    translation = items[0][locale]

    if name != translation:
        print(f"Translating '{name}' to '{translation}'")

    return translation


def __get(translation_dir):
    results = __load(os.path.join(translation_dir, 'item-names.json'))
    results += __load(os.path.join(translation_dir, 'item-runes.json'))
    results += __load(os.path.join(translation_dir, 'monsters.json'))
    results += __load(os.path.join(translation_dir, 'levels.json'))

    return results


def __load(filepath):
    contents = None
    with open(filepath, "rt", encoding='utf-8-sig') as f:
        contents = json.load(f)

    # Save for debugging
    copyfile(filepath, os.path.join("generated", "translations.json"))

    return contents
