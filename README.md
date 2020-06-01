# N26 to YNAB automation bridge
This is a minimalistic implementation of a process that bulks the transactions of a given N26 account to You Need A Budget; all through APIs.
The current implementation handles duplication through the YNAB internal functionality. It's way of working consists of calling the main module with an argument specifying an account name (previously configured). After that call, the system will retrieved all the N26 transactions, and it will push them to the YNAB budget and account specified in the configuration files.

Please keep in mind that this is a personal project meant to satisfy a personal necessity. It may not totally apply to your use-case. Feel free to fork the project or suggest any extra functionality.

## Getting started
Follow the next steps to have the project running in your system:

1. Install [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/) in your system following the linked official guides.
2. Open a terminal, clone this repository and `cd` to the cloned folder.
3. Run `pyenv install 3.6.1` in your terminal for installing the required python.
   version
4. Configure poetry with `poetry config virtualenvs.in-project true`
5. Create the virtual environment with `poetry install`
6. Create the `config/ynab.toml` file following the example in the same folder
7. Create the `config/n26.toml` file following the example in the same folder. Make sure you establish the links from each account configured here to the desired YNAB account name
8. Activate the environment with `source .venv/bin/activate`
9. Run `python main.py -a <n26-account-name>` to send the transactions from the n26 account specified to the YNAB account

## Contribution
Pull requests and issues will be tackled upon availability.

## License
This repository is licensed under MIT license. More info in the LICENSE file. Copyright (c) 2020 Iván Vallés Pérez