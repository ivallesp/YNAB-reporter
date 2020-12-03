import os


def get_log_config_filepath():
    return "logging.ini"


def get_config_path():
    path = os.path.join("config")
    return path


def get_ynab_config_filepath():
    path = os.path.join("config", f"ynab.toml")
    if not os.path.exists(path):
        raise ValueError(f"YNAB not configured. File {path} not found!")
    return path


def get_email_config_filepath():
    path = os.path.join("config", f"email.toml")
    if not os.path.exists(path):
        raise ValueError(f"E-Mail not configured. File {path} not found!")
    return path
