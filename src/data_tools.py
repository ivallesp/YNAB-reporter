import pandas as pd


def cartesian_pair(df1, df2, **kwargs):
    """
    Make a cross join (cartesian product) between two dataframes by using a constant temporary key.
    Also sets a MultiIndex which is the cartesian product of the indices of the input dataframes.
    See: https://github.com/pydata/pandas/issues/5401
    :param df1 dataframe 1
    :param df2 dataframe 2
    :param kwargs keyword arguments that will be passed to pd.merge()
    :return cross join of df1 and df2
    """
    df1["_tmpkey"] = 1
    df2["_tmpkey"] = 1

    res = pd.merge(df1, df2, on="_tmpkey", **kwargs).drop("_tmpkey", axis=1)

    df1.drop("_tmpkey", axis=1, inplace=True)
    df2.drop("_tmpkey", axis=1, inplace=True)

    return res


def cartesian_multiple(df, columns):
    df_cartesian = df.loc[:, [columns[0]]].drop_duplicates()
    for i in range(1, len(columns)):
        df_cartesian = cartesian_pair(
            df_cartesian, df.loc[:, [columns[i]]].drop_duplicates()
        )
    return df_cartesian
