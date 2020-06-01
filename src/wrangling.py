import pandas as pd

from src.config import load_ynab_config
from src.api import fetch_transactions, get_ynab_client
from src.data_tools import cartesian_pair, cartesian_multiple


def get_ynab_dataset(min_date=None, max_date=None):
    ynab_cli = get_ynab_client()
    ynab_conf = load_ynab_config()["ynab"]
    data = fetch_transactions(ynab_cli, ynab_conf["budget_name"])
    df = pd.DataFrame(data)
    df = df[lambda d: d.deleted == False]  # Remove the deleted transactions
    df = df[lambda d: d.approved == True]  # Remove the non-approved transactions
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d")
    if min_date:
        df = df[lambda d: d.date >= min_date]
    if max_date:
        df = df[lambda d: d.date <= max_date]
    df = df.assign(amount=lambda d: d.amount / 1000)
    return df


def calculate_daily_balances(df):
    pks = ["account_name", "category_name"]
    df_date = pd.DataFrame({"date": pd.date_range(df.date.min(), df.date.max())})
    df_pks = cartesian_multiple(df[pks], pks)
    df_base = cartesian_pair(df_date, df_pks)
    df = df_base.merge(df[pks + ["date", "amount"]], how="left").fillna(0)
    df = df.sort_values(by="date")
    df = df.assign(
        amount=lambda d: d.groupby(pks).amount.transform(lambda x: x.cumsum())
    )
    return df
