import os
import pandas
from pandas.core import indexing
import common
import json

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def parse_monstats():
    columns_to_keep = ['Id', 'Level', 'Level(N)', 'Level(H)']
    all_monsters = common.create_dictionary(os.path.join(data_dir, "MonStats.txt"))

    # Filter out monsters that are not bosses
    all_bosses = [monster for monster in all_monsters if monster['boss'] == 1]

    # Only keep these bosses
    bosses_to_keep = ['andariel', 'duriel', 'mephisto', 'diablo', 'summoner', 'baalcrab']
    bosses = [boss for boss in all_bosses if boss['Id'] in bosses_to_keep]

    filtered_bosses = []
    for entry in bosses:
        filtered_bosses.append(common.filter_columns(entry, columns_to_keep))

    bosses = filtered_bosses

    # Transform names to more player friendly names
    # If a name isn't in this list we'll use the 'Id' field itself as the 'name'
    display_names = {'baalcrab': "baal"}
    for boss in bosses:
        boss['name'] = display_names[boss['Id']].capitalize() if boss['Id'] in display_names else boss['Id'].capitalize()

    return bosses

def parse_uniqueitems():
    columns_to_keep=['index', 'lvl']

    all_unique_items = common.create_dictionary(os.path.join(data_dir, "UniqueItems.txt"))

    # Filter out entries that are not enabled
    all_unique_items = [item for item in all_unique_items if item['enabled'] == 1]

    filtered_entries = []
    for item in all_unique_items:
        filtered_entries.append(common.filter_columns(item, columns_to_keep))
    unique_items = filtered_entries

    # Transform names to more player friendly names
    # If a name isn't in this list we'll use the 'Id' field itself as the 'name'
    display_names = {
        'The Stone of Jordan': "The Stone of Jordan (SOJ)",
        'Harlequin Crest': 'Harlequin Crest (Shako)'
    }
    for item in unique_items:
        item['index'] = display_names[item['index']] if item['index'] in display_names else item['index']

    return unique_items

def parse_armor():
    columns_to_keep=['name', 'level']

    all_armors = common.create_dictionary(os.path.join(data_dir, "Armor.txt"))

    filtered_entries = []
    for item in all_armors:
        filtered_entries.append(common.filter_columns(item, columns_to_keep))

    return filtered_entries

if __name__ == "__main__":
    bosses = parse_monstats()
    unique_items = parse_uniqueitems()
    armors = parse_armor()

    results = {"bosses": bosses, "uniqueitems": unique_items, "armors": armors}

    # Write the full results.json file
    with open(os.path.join(data_dir, "results.json"), "w") as f:
        f.write(json.dumps(results, indent=2))

    print("Finished parsing files")
