import calendar
import locale
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

from src.wrangling import calculate_daily_balances, get_ynab_dataset

import matplotlib as mpl

COLORS = [
    "da4450",
    "643a71",
    "91acca",
    "b964a4",
    "0d6b96",
    "06a77d",
    "ff9d58",
    "536b38",
]

# Use seaborn style
plt.style.use("seaborn")
# Set colors
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=COLORS)
# Enable the legend frame
mpl.rcParams["legend.frameon"] = "True"
# Prevent matplotlib from cutting labels at export time
mpl.rcParams.update({"figure.autolayout": True})

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_top_flows(year, month, n_rows):
    df = get_ynab_dataset()
    df = df.loc[lambda d: (d.date.dt.month == month) & (d.date.dt.year == year)]
    df = df[df.transfer_transaction_id.isnull()]
    # Separate inflows and outflows
    df_in = df.loc[lambda d: d.amount >= 0]
    df_out = df.loc[lambda d: d.amount < 0]
    # Date format adjustment
    df_in["date"] = df_in.date.dt.strftime("%b-%d")
    df_out["date"] = df_out.date.dt.strftime("%b-%d")
    # Limit the length of the memo text
    df_in["memo"] = df_in["memo"].str.slice(0, 20)
    df_out["memo"] = df_out["memo"].str.slice(0, 20)
    # Define the original column names and the desired ones
    columns = ["date", "account_name", "amount", "memo"]
    fancy_colnames = ["Date", "Account", "Amount", "Memo"]
    # Select columns and sort by amount
    df_in = df_in[columns].sort_values(by="amount", ascending=False)
    df_out = df_out[columns].sort_values(by="amount", ascending=True)
    # Take the first N rows
    df_in = df_in.head(n_rows)
    df_out = df_out.head(n_rows)
    # Rename the columns
    df_in.columns = fancy_colnames
    df_out.columns = fancy_colnames
    return df_in, df_out


def calculate_financial_snapshot(year, month):
    eom_day = calendar.monthrange(year, month)[1]
    eom_date = datetime(year, month, eom_day)
    # Load data and calculate daily balances
    df_ynab = get_ynab_dataset()
    df = calculate_daily_balances(df=df_ynab)
    # Get the end of month balances
    df = df[lambda d: d.date == eom_date]
    # Aggregate at account level
    df = df.groupby(["account_name"]).amount.sum()
    # Sort accounts by decreasing balance
    df = df.sort_values(ascending=False).reset_index()
    # Remove accounts with 0€
    df = df[lambda d: d.amount != 0]
    # Add total
    total = {"account_name": ["Total"], "amount": [df.amount.sum()]}
    df_total = pd.DataFrame(total)
    df = pd.concat([df, df_total], axis=0)
    # Add fancy column names
    df.columns = ["Account", "Amount"]
    # Transpose
    df = df.set_index("Account").transpose()
    return df


def generate_evolution_plot(year, month):
    df_ynab = get_ynab_dataset()
    df = calculate_daily_balances(df=df_ynab)
    df = df.loc[(df.date.dt.year <= year) & (df.date.dt.month <= month)]
    # Aggregate at account level
    df = df.groupby(["date", "account_name"]).amount.sum().reset_index()
    # Pivot the account dimension
    df = pd.pivot_table(df, index="date", columns="account_name", aggfunc="sum")
    # Drop the accounts that have always had 0 balance
    for col in df.columns:
        if df[col].max() == 0:
            df = df.drop(col, axis=1)
    # Sort columns by average amount
    df = df[df.sum(axis=0).sort_values(ascending=False).index]
    # Build list of histories per account
    histories = list(zip(*df.values.clip(0, None).tolist()))
    # Calculate the histories for every account
    yticks_freq = 5000  # Frequency of the y ticks
    # Get the limits for the Y axis
    top = yticks_freq * math.ceil(df.values.sum(axis=1).max() / yticks_freq)
    bot = -top * 0.025
    # Generate a new figure
    fig = plt.figure(figsize=(10, 2))
    ax = plt.gca()
    # Plot the histories
    ax.stackplot(df.index.tolist(), *histories, labels=df["amount"].columns)
    # Add a horizontal line at zero
    ax.axhline(0, color="k", linewidth=1)
    # Plot the legend
    ax.legend(loc="upper left", facecolor="white")
    # Add the grid on top the graph
    ax.set_axisbelow(False)
    ax.grid(which="both", color="#DDDDDD", linestyle="-", linewidth=0.7)
    # Background to white
    ax.set_facecolor((1, 1, 1))
    # Configure the axis
    ax.set_yticks(np.arange(0, top + 1, yticks_freq))
    ax.set_ylim(None, top)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    monthsFmt = mdates.DateFormatter("%b")
    yearsFmt = mdates.DateFormatter("\n\n%Y")  # add some space for the year label
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(monthsFmt)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)

    # Make the layout tight (lower margins)
    fig.tight_layout()
    # Rotate 90 degrees the minor labels in the X axis
    labels = ax.get_xticklabels(minor=True)
    ax.set_xticklabels(labels, minor=True, rotation=90)
    return fig, ax


def generate_categories_detail_plot(year, month):
    df = get_ynab_dataset()
    df = df.loc[(df.date.dt.year <= year) & (df.date.dt.month <= month)]
    df = df[df.transfer_transaction_id.isnull()]
    df["month"] = df.date.dt.month
    df["year"] = df.date.dt.year
    df = df.groupby(["year", "month", "category_name"]).amount.sum()
    df = df.sort_values()[year, month]
    # Remove the income category. We want to analyse the rest
    df = df.drop("Immediate Income SubCategory")
    # Separate the category names from the values
    cats = df.index.tolist()
    vals = df.values
    # Shorten category names by removing the annotations between parentheses
    cats = [x.split("(")[0].strip() for x in cats]
    # Distinguish possitive and negative values with colors
    colors = ["#" + COLORS[0] + "FF" if x < 0 else "#" + COLORS[5] + "FF" for x in vals]
    # Calculate the histories for every account
    yticks_freq = 250  # Frequency of the y ticks
    # Get the max value for the Y axis
    top = yticks_freq * math.ceil((-vals).max() / yticks_freq)
    bot = yticks_freq * math.floor((-vals).min() / yticks_freq)
    # Generate a new figure
    fig = plt.figure(figsize=[10, 2.5])
    ax = plt.gca()
    # Plot the bars
    bars = plt.bar(cats, -vals, color=colors)
    # Set the frequency of the yticks
    ax.set_yticks(np.arange(0, top + 1, yticks_freq))
    # Add a horizontal line at zero
    ax.axhline(0, color="k", linewidth=0.7)
    # Background to white
    ax.set_facecolor((1, 1, 1))
    # Gridlines to grey
    ax.grid(color="#DDDDDD", linestyle="-", linewidth=0.7)
    # ax.grid(False)
    for bar in bars:
        height = bar.get_height()
        perc = (
            str(round(100 * height / -vals[vals < 0].sum(), 1)) + "%"
            if height > 0
            else ""
        )
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 20,
            "%s" % perc,
            ha="center",
            va="bottom",
        )
    plt.ylim(bot, top)
    # Make the layout tight (lower margins)
    fig.tight_layout()
    ax.xaxis.set_tick_params(rotation=30)
    return fig, ax


def calculate_monthly_flows(year, month):
    # Load data
    df = get_ynab_dataset()
    df = df.loc[(df.date.dt.year <= year) & (df.date.dt.month <= month)]
    # Filter out the transfers
    df = df[df.transfer_transaction_id.isnull()]
    # Add month column
    month_col = pd.Series(np.array(MONTHS)[df.date.dt.month.values - 1], index=df.index)
    month_col = month_col + " " + df.date.dt.year.astype(str)
    df["month"] = month_col.values
    # Calculate inflows and outflows
    df["inflow"] = 0
    df["outflow"] = 0
    inflow_f = lambda d: d.amount > 0
    outflow_f = lambda d: d.amount <= 0
    df.loc[inflow_f, "inflow"] = df.loc[inflow_f, "amount"]
    df.loc[outflow_f, "outflow"] = -df.loc[outflow_f, "amount"]
    # Aggregate at month level
    agg_dict = {"date": np.max, "inflow": np.sum, "outflow": np.sum}
    df = df.groupby("month").agg(agg_dict)
    df = df.sort_values(by="date").reset_index()
    # Calculate savings
    df["savings"] = df.inflow - df.outflow
    # Filter and arrange columns
    df = df[["month", "inflow", "outflow", "savings"]]
    # Remove first row (initial balance is counted as inflow)
    df = df.iloc[1:]
    return df


def calculate_financial_evolution(year, month):
    # Load data and calculate daily balances
    df_ynab = get_ynab_dataset()
    df = calculate_daily_balances(df=df_ynab)
    df = df.loc[(df.date.dt.year <= year) & (df.date.dt.month <= month)]
    # Get the end of month balances
    df = df[lambda d: d.date.dt.is_month_end]
    # Aggregate at date level
    df = df.groupby(["date"]).amount.sum()
    # Sort accounts by decreasing balance
    df = df.sort_values(ascending=False).reset_index()
    # Add month column
    month_col = pd.Series(np.array(MONTHS)[df.date.dt.month - 1])
    month_col = month_col + " " + df.date.dt.year.astype(str)
    df["month"] = month_col
    # Calculate flows
    df_flows = calculate_monthly_flows(year=year, month=month)
    df = df.merge(df_flows, how="left")
    # Filter and arrange columns
    df = df[["month", "inflow", "outflow", "savings", "amount"]]
    # Add fancy column names
    df.columns = ["Month", "Inflow", "Outflow", "Savings", "Amount"]
    return df


def generate_latex_report(year, month):
    locale.setlocale(locale.LC_ALL, "en_us.utf-8")
    float_format = lambda x: locale.format("%.2f", x, grouping=True)
    with open("assets/template.tex", "r") as f:
        template = f.read()

    title = f"Financial report – {MONTHS[month-1]} {year}"

    df_financial_snapshot = calculate_financial_snapshot(year=year, month=month)
    financial_snapshot = df_financial_snapshot.to_latex(
        index=False, float_format=float_format
    )

    df_financial_evolution = calculate_financial_evolution(year=year, month=month)
    financial_evolution = df_financial_evolution.to_latex(
        index=False, float_format=float_format
    )

    template = template.format(
        title=title,
        financial_snapshot=financial_snapshot,
        financial_evolution=financial_evolution,
    )
    # + monthly inflows and outflows, with initial and final balance and savings
    # + biggest transactions

    # Change colors
    # Add grid
    # Set xlim
    fig, ax = generate_evolution_plot(year=year, month=month)
    fig.savefig("assets/evolution.eps")

    with open("assets/report.tex", "w") as f:
        f.write(template)
