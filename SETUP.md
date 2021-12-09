# Setup

## Dependencies

* Run `pip install -r requirements.txt`.
* Run `npm install`.

---

## Generate the front-end data from the game files

Change the variable `game_version` in the `build_all.py` script to correspond with the directory you extracted the files to `./d2r/data/<GAMEVERSION>`.

* Run `python .\d2r\build_all.py`

*Note: This is also a `task` in vscode, you can run them there.*

---

## Site generation

* Local testing: `eleventy --serve`, localhost:8080.
* Deploy: `eleventy`, generates `/public` folder.

*Note: Both of these steps are `tasks` in vscode, you can run them there.*

---

## Unpacking Diablo 2: Resurrected files

Data is now parsed directly from the unpacked data files in the Diablo 2 Ressurected folder, instead of an old third party repo.

There shouldn't be any need to unpack the game files, but to update the parsed game files, I've included the binary `CascView` in the `third_party` folder.

You can use it to open the directory on your harddrive to `Diablo 2: Ressurected` and extract the game files.

Extract the following directories into `./d2r/data/<GAMEVERSION>/`

```
data/data/global/excel
data/data/local/Ing/strings
```

---