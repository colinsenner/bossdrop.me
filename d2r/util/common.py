import os
from os import path

def get_data_dir():
    return path.join(os.getcwd(), "data")

def remove_duplicate_rows(df):
    '''
    Returns a dataframe with duplicate indexes removed
    '''
    return df[~df.index.duplicated(keep='first')]
