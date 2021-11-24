import os
import requests
from urllib.parse import urljoin

download_url = f'https://raw.githubusercontent.com/fabd/diablo2/master/code/d2_113_data/'
data_dir = os.path.join(os.path.dirname(__file__), 'data')

files_to_download = ['MonStats.txt', 'UniqueItems.txt', 'Armor.txt', 'Weapons.txt', 'Misc.txt']

os.makedirs(data_dir, exist_ok=True)

for file in files_to_download:
    url = urljoin(download_url, file)

    local_file = os.path.join(data_dir, file)

    res = requests.get(url)

    assert res.status_code == 200, f"Problem downloading file: {file}"

    with open(local_file, "wt", encoding='utf-8') as f:
        f.write(res.text)

print("Files downloaded.")