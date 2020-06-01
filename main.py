import argparse
import logging.config
from src.api import update_ynab
from src.paths import get_log_config_filepath

logging.config.fileConfig(get_log_config_filepath(), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="N26 to YNAB bridge. Run the program to download the transactions "
        "from the N26 account and upload the into the YNAB budget account. "
        "Example: python main.py -a my_account_name"
    )

    parser.add_argument(
        "-a",
        action="store",
        dest="account",
        required=True,
        help="Name of the account to update. Has to be defined in config/n26.toml",
    )

    results = parser.parse_args()

    # Run the update process
    logger.info(f"Requested 💰 YNAB update for account name: {results.account}")
    update_ynab(results.account)
    logger.info(f"YNAB update performed successfully! 🎉🎊🥳")
