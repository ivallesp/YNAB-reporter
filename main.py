import os
import argparse
import logging.config
from src.paths import get_log_config_filepath
from src.reporting import MONTHS, generate_latex_report

logging.config.fileConfig(get_log_config_filepath(), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YNAB personal finance PDF report generation. Run the program "
        "to connect to a YNAB account, download all the transactions available in "
        "the specified report and sumarise it in a monthly PDF document."
    )

    parser.add_argument(
        "-m",
        action="store",
        dest="month",
        required=True,
        help="Month to generate a summary of",
    )

    parser.add_argument(
        "-y",
        action="store",
        dest="year",
        required=True,
        help="Year to generate a summary of",
    )

    results = parser.parse_args()

    # Run the update process
    logger.info(
        f"Requested 💰 LaTeX report generation for month "
        f"{MONTHS[int(results.month)]} and year {int(results.year)}"
    )
    generate_latex_report(year=int(results.year), month=int(results.month))
    os.system("cd assets && pdflatex report.tex")
    logger.info(f"YNAB report generated successfully! 🎉🎊🥳")
