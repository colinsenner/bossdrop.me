import pandas as pd
from os import path
from .common import get_data_dir

def get_unique_items():
    unique_items = []

    df = pd.read_csv(path.join(get_data_dir(), 'UniqueItems.txt'), sep='\t')

    print(df.head())
    return unique_items
