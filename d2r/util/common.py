import os
from os import path

def get_data_dir():
    return path.join(os.getcwd(), "data")
