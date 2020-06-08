# N26 to YNAB automation bridge
This repository implements a small system for generating reports summarising You Need A Budged monthly movements and historical positions. The data is obtained using the YNAB API and the reports are generated using LaTeX.

## Getting started
Follow the next steps to have the project running in your system:

1. Install [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/) in your system following the linked official guides.
2. Open a terminal, clone this repository and `cd` to the cloned folder.
3. Run `pyenv install $(cat .python-version)` in your terminal for installing the required python.
   version.
4. Configure poetry with `poetry config virtualenvs.in-project true`.
5. Create the virtual environment with `poetry install`.
6. Make sure you have LaTeX installed in your system (or install it with `sudo apt-get install texlive-full`) with the needed dependencies.
7. Create the `config/ynab.toml` file following the example in the same folder and fill-in your budget name and API key.
8. Activate the environment with `source .venv/bin/activate`.
9. Run `python main.py -y <report-year> -m <report-month>` to generate a report for the specified date.

## Contribution
Pull requests and issues will be tackled upon availability.

## License
This repository is licensed under MIT license. More info in the LICENSE file. Copyright (c) 2020 Iván Vallés Pérez