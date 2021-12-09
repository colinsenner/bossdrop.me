import os
import pathlib
from os import path

import pandas as pd

__cached_files = {}


def get_data_dir():
    return path.join(os.getcwd(), "data")


def get_generated_dir():
    return path.join(os.getcwd(), "generated")


def get_excel_dir(version):
    return pathlib.Path(get_data_dir(), version, "data", "data", "global", "excel")


def get_translation_dir(version):
    return pathlib.Path(get_data_dir(), version, "data", "data", "local", "lng", "strings")


def get_base_file(version, filename):
    global __cached_files

    if filename not in __cached_files:
        df = pd.read_csv(path.join(get_excel_dir(version), filename), sep='\t')

        # Cache it
        __cached_files[filename] = df

    return __cached_files[filename]
