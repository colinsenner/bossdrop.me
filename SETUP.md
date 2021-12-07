# Setup

## Python dependencies

1. Run `pip install -r requirements.txt`.

## Generate the front-end data from the game files

1. Run `python .\d2r\download_data_files.py` to download the game files from a github repo
2. Run `python .\d2r\generate_results.py` to create the needed files in the `d2r/generated` directory and copy them to `/src/static/*`.

*Note: Both of these steps are `tasks` in vscode, you can run them there.*

## Site generation

1. `npm install`
2. Local testing: `eleventy --serve`, localhost:8080.
3. Deploy: `eleventy`, generates `/public` folder.

*Note: Both of these steps are `tasks` in vscode, you can run them there.*