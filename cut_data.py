# Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# data path = where we store the data, plots and catalogue
data_path = "./data/lunar/training/"
raw_data_path = data_path + "data/S12_GradeA/"
catalogue_path = data_path + "catalogs/apollo12_catalog_GradeA_final.csv"

df = pd.read_csv(catalogue_path)
filenames = df["filename"]

dfs = []
for i in filenames.to_list():
    if os.path.exists(raw_data_path+i+".csv"):
        dfs.append(pd.read_csv(raw_data_path + i + ".csv"))
        tmp = pd.read_csv(raw_data_path + i + ".csv")
        print(tmp.head())
        tmp = tmp[tmp["velocity(m/s)"] > 0]

        tmp = tmp.reset_index()
        tmp["a"] = tmp["velocity(m/s)"].rolling(window=1000).mean()        # tmp["velocity(m/s)"].rolling(window=10000).mean().plot(color="g")

        med = tmp["velocity(m/s)"].median() * 4
        tmp["velocity(m/s)extra"] = tmp["velocity(m/s)"].apply(lambda x: x+med)

        tmp["b"] = tmp["velocity(m/s)extra"].rolling(window=20000).mean()
        this = tmp[tmp.a > tmp.b]

        tmp["velocity(m/s)"].plot(color="y")
        tmp["a"].plot(color="r")
        tmp["b"].plot(color="b")
        plt.show()

        dif = this.idxmax().iloc[0] - this.idxmin().iloc[0]
        start = this.idxmin().iloc[0] - dif
        end = this.idxmax().iloc[0] + (dif*2)
        tmp = tmp.iloc[start:end]
 
        tmp["velocity(m/s)"].plot(color="y")
        tmp["a"].plot(color="r")
        tmp["b"].plot(color="b")

        print(dif, start, end)
        plt.show()
        quit()
