import os
from os import path
import pandas as pd
import util.items

def main():
    items = []
    items.extend(util.items.get_unique_items())

    print(items)

if __name__ == '__main__':
    main()

