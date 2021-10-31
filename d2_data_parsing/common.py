import pandas

def create_dictionary(filename):
    data = pandas.read_csv(filename, sep='\t')

    # Now you transform the DataFrame to a list of dictionaries
    list_of_dicts = [item for item in data.T.to_dict().values()]
    return list_of_dicts

def filter_columns(d, columns_to_keep):
    return {k: v for k, v in d.items() if k in columns_to_keep}
