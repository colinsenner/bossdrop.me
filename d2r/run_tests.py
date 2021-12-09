import json
from os import path

# A bit optimistic calling these real tests
def main():
    test_compare_results()


def test_compare_results():
    old_results_path = path.join("tests", "old_results.json")
    results_path = path.join("tests", "results.json")

    old_results = load_json(old_results_path)
    results = load_json(results_path)

    print("These items are in one file but not the other")
    print("---------------------------------------------")
    print_diff_from_field(old_results['unique_items'],
                          results['items'],
                          'index')

    old_monsters = old_results['bosses']
    new_monsters = results['monsters']

    # Remove all TC fields from both
    remove_keys(old_monsters, ['TC', 'TC(N)', 'TC(H)'])
    remove_keys(new_monsters, ['TC', 'TC(N)', 'TC(H)'])

    print()
    print("These monsters are in one file but not the other")
    print("------------------------------------------------")
    print_diff_from_field(old_monsters,
                          new_monsters,
                          'Id')


    return


def remove_keys(d, keys=[]):
    for entry in d:
        for key in keys:
            entry.pop(key)


def print_diff_from_field(a, b, index_name):
    a_entries = [obj[index_name].lower() for obj in a]
    b_entries = [obj[index_name].lower() for obj in b]

    differences = set(a_entries).symmetric_difference(set(b_entries))

    for diff in differences:
        a_entry = list(filter(lambda x: x[index_name].lower() == diff, a))
        a_entry = a_entry[0] if len(a_entry) > 0 else None

        b_entry = list(filter(lambda x: x[index_name].lower() == diff, b))
        b_entry = b_entry[0] if len(b_entry) > 0 else None

        if a_entry != None:
            print(f"A: {a_entry}")

        if b_entry != None:
            print(f"B: {b_entry}")

    return diff


def load_json(filepath):
    with open(filepath, "rt", encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    main()