import os
import pandas
from pandas.core import indexing
import common
import json

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def parse_d2_file(filename, column_to_filter_rows_by='', rows_to_keep=[], columns_to_keep=[]):
    entries = common.create_dictionary(os.path.join(data_dir, filename))

    if len(rows_to_keep) > 0:
        # Filter all entries where their id isn't in the list
        entries = [entry for entry in entries if entry[column_to_filter_rows_by] in rows_to_keep]

    # If we are filtering out at least one column
    if len(columns_to_keep) > 0:
        filtered_entries = []
        for entry in entries:
            filtered_entries.append(common.filter_columns(entry, columns_to_keep))
    else:
        filtered_entries = entries

    return filtered_entries

# def parse_MonStats():
#     monster_ids_to_keep = ['andariel']
#     columns_to_keep = ['Id', 'Level', 'Level(N)', 'Level(H)']

#     monsters = common.create_dictionary(os.path.join(data_dir, "MonStats.txt"))

#     # Filter all monsters where their id isn't in the list
#     monsters = [monster for monster in monsters if monster['Id'] in monster_ids_to_keep]

#     filtered_monsters = []
#     for monster in monsters:
#         filtered_monsters.append(common.filter_columns(monster, columns_to_keep))

#     return filtered_monsters

# def parse_UniqueItems():
#     item_indexes_to_keep = ['Harlequin Crest']
#     columns_to_keep = ['index', 'lvl']

#     unique_items = common.create_dictionary(os.path.join(data_dir, "UniqueItems.txt"))

#     # Filter all monsters where their id isn't in the list
#     unique_items = [item for item in unique_items if item['Id'] in item_indexes_to_keep]



#bosses = parse_MonStats()
#uniques = parse_UniqueItems()
bosses = parse_d2_file("MonStats.txt",
                        column_to_filter_rows_by='Id',
                        rows_to_keep=['andariel'],
                        columns_to_keep=['Id', 'Level', 'Level(N)', 'Level(H)'])

unique_items = parse_d2_file("UniqueItems.txt",
                        column_to_filter_rows_by='index',
                        rows_to_keep=['Harlequin Crest', 'The Stone of Jordan'],
                        columns_to_keep=['index', 'lvl'])

results = {"bosses": bosses, "uniqueitems": unique_items}

# Write the full results.json file
with open(os.path.join(data_dir, "results.json"), "w") as f:
    f.write(json.dumps(results, indent=2))

print("Finished parsing files")
