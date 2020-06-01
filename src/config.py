import toml
from src.paths import get_ynab_config_filepath


def load_ynab_config():
    path = get_ynab_config_filepath()
    config = toml.load(path)
    return config
