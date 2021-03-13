import sys
from src.reporting import get_ynab_dataset


def export_ynab_dataset():
    get_ynab_dataset().to_csv(sys.argv[1], index=False)


if __name__=="__main__":
    export_ynab_dataset()