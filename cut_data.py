import pandas as pd


def get_seismic_events(df: pd.DataFrame, velocity_col: str) -> pd.DataFrame:
    df = df[df[velocity_col] > 0]
    df = df.reset_index()
    df["STA"] = (
        df[velocity_col].rolling(window=1000).mean()
    )  # make the short term average
    # add median to velocitys
    median = df[velocity_col].median() * 4
    df[velocity_col +
        " and median"] = df[velocity_col].apply(lambda x: x + median)
    df["LTA"] = (
        df[velocity_col + " and median"].rolling(window=20000).mean()
    )  # make the long term average
    # select part of datafram
    sta_over_lta = df[df["STA"] > df["LTA"]]
    if len(sta_over_lta) == 0:
        return pd.Series([])
    start = sta_over_lta.idxmin().iloc[0] - 5000
    end = sta_over_lta.idxmax().iloc[0] + 20000
    df = df.iloc[start:end]
    return df.drop(["index", "STA", "LTA", velocity_col + " and median"], axis=1)
