# Setup

## Dependencies

* Run `pip install -r requirements.txt`.
* Run `npm install`.

## Generate the front-end data from the game files

* Run `python .\d2r\download_data_files.py` to download the game files from a github repo
* Run `python .\d2r\generate_results.py` to create the needed files in the `d2r/generated` directory and copy them to `/src/static/*`.

*Note: Both of these steps are `tasks` in vscode, you can run them there.*

---

## Site generation

* Local testing: `eleventy --serve`, localhost:8080.
* Deploy: `eleventy`, generates `/public` folder.

*Note: Both of these steps are `tasks` in vscode, you can run them there.*