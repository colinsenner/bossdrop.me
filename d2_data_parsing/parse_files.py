import os
import pandas
from pandas.core import indexing
import common
import json

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def parse_monstats():
    columns_to_keep = ['Id', 'Level', 'Level(N)', 'Level(H)']
    entries = common.create_dictionary(os.path.join(data_dir, "MonStats.txt"))

    # Filter out monsters that are not bosses
    entries = [entry for entry in entries if entry['boss'] == 1]

    # Only keep these bosses
    bosses_to_keep = ['andariel', 'duriel', 'mephisto', 'diablo', 'summoner', 'nihlathakboss', 'baalcrab']
    entries = [entry for entry in entries if entry['Id'] in bosses_to_keep]

    filtered_entries = []
    for entry in entries:
        filtered_entries.append(common.filter_columns(entry, columns_to_keep))

    return filtered_entries

def parse_uniqueitems():
    columns_to_keep=['index', 'lvl']

    entries = common.create_dictionary(os.path.join(data_dir, "UniqueItems.txt"))

    # Filter out entries that are not enabled
    entries = [entry for entry in entries if entry['enabled'] == 1]

    filtered_entries = []
    for entry in entries:
        filtered_entries.append(common.filter_columns(entry, columns_to_keep))

    return filtered_entries

if __name__ == "__main__":
    bosses = parse_monstats()
    unique_items = parse_uniqueitems()

    results = {"bosses": bosses, "uniqueitems": unique_items}

    # Write the full results.json file
    with open(os.path.join(data_dir, "results.json"), "w") as f:
        f.write(json.dumps(results, indent=2))

    print("Finished parsing files")
