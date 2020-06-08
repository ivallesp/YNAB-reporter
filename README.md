# YNAB reporter: a simple YNAB monthly reporting system
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
8. Do the same with the `config/email.toml` file. The example contained in this repository has the settings for gmail pre-filled in.
9. Activate the environment with `source .venv/bin/activate`.
10. Run `python main.py -y <report-year> -m <report-month>` to generate a report for the specified date.


It might be useful to set up a crontab to run the system every month. In my case, I run it the 5th day of every month, for calculating the report corresponding with the previous month. The crontab entry is shown below as an example.

```
0 9 5 * *     cd ~/projects/ynab-reporter && .venv/bin/python main.py -m `date +\%-m --date="1 month ago"` -y `date +\%Y --date="1 month ago"` -e my.email@gmail.com my.partner.email@gmail.com
```

## Contribution
Pull requests and issues will be tackled upon availability.

## License
This repository is licensed under MIT license. More info in the LICENSE file. Copyright (c) 2020 Iván Vallés Pérez