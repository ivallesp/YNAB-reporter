import toml
from src.paths import get_ynab_config_filepath, get_email_config_filepath


def load_ynab_config():
    path = get_ynab_config_filepath()
    config = toml.load(path)
    return config


def load_email_config():
    path = get_email_config_filepath()
    config = toml.load(path)
    return config["email"]
