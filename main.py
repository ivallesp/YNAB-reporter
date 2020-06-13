import os
import argparse
import logging.config
from src.paths import get_log_config_filepath
from src.reporting import MONTHS, generate_latex_report
from src.email import send_mail

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

    parser.add_argument(
        "-e",
        action="store",
        dest="recipients",
        required=False,
        nargs="+",
        help="Recipients to send the report to",
    )

    results = parser.parse_args()

    month_name = MONTHS[int(results.month) - 1]

    # Run the update process
    logger.info(
        f"Requested 💰 LaTeX report generation for month "
        f"{month_name} and year {int(results.year)}"
    )
    generate_latex_report(year=int(results.year), month=int(results.month))
    os.system("cd assets && pdflatex report.tex")
    logger.info(f"YNAB report generated successfully! 🎉🎊🥳")
    report_path = os.path.join("assets", "report.pdf")
    report_name = f"{month_name}-{results.year}-report.pdf"
    if results.recipients:
        logger.info(
            f"Sending report by mail to the following recipients: {results.recipients}"
        )
        send_mail(
            send_to=results.recipients,
            subject=f"{month_name}-{results.year} financial report",
            message=f"Report corresponding to {month_name} {results.year} attached.",
            files=[(report_path, report_name)],
        )
        logger.info("Report sent successfully! ✉️")
