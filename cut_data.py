# Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

def get_seismic_events(df: pd.DataFrame, velocity_col: str) -> pd.DataFrame:
    df = df[df[velocity_col] > 0]
    df = df.reset_index()
    df["STA"] = df[velocity_col].rolling(window=1000).mean()        # df["velocity(m/s)"].rolling(window=10000).mean().plot(color="g")
    median = df[velocity_col].median() * 4
    df[velocity_col + " and median"] = df[velocity_col].apply(lambda x: x+median)
    df["LTA"] = df[velocity_col + " and median"].rolling(window=20000).mean()
    sta_over_lta = df[df["STA"] > df["LTA"]]
    start = sta_over_lta.idxmin().iloc[0] - 5000
    end = sta_over_lta.idxmax().iloc[0] + 20000
    df = df.iloc[start:end]
    return df

# data path = where we store the data, plots and catalogue
data_path = "./data/lunar/training/"
raw_data_path = data_path + "data/S12_GradeA/"
catalogue_path = data_path + "catalogs/apollo12_catalog_GradeA_final.csv"

df = pd.read_csv(catalogue_path)
filenames = df["filename"]

for i in range(10):
    temp = pd.read_csv(raw_data_path + filenames.to_list()[i] + ".csv")
    str_name = "velocity(m/s)"

    get_seismic_events(temp, str_name)

