# Import libraries
import numpy as np
import pandas as pd
# from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os as os

# data path = where we store the data, plots and catalogue
data_path = "./data/lunar/training/"
raw_data_path = data_path + "data/S12_GradeA/"
catalogue_path = data_path + "catalogs/apollo12_catalog_GradeA_final.csv"
print(catalogue_path)

df = pd.read_csv(catalogue_path)

filenames = df["filename"]

def applyScale(data):
    top = data.max()
    bottom = data.min()
    data = data - bottom # remove the minimum value from all data points
    data = data / (top - bottom) # divide by the range
    
    # output_path = raw_data_path + "scaletest" + ".csv"
    # data.to_csv(output_path, index=False)

    return [data, bottom, top - bottom]

def removeScale(data):
    data[0] = (data[0]*data[1]) + data[2]
    return data[0]

def computeError(originalData, decompressedData):
    residuals = originalData - decompressedData
    print(residuals)
    residualErrorPercentage = 100*(residuals / originalData)
    print(residualErrorPercentage.mean())
    return residualErrorPercentage.mean()

for i in filenames.to_list():
    if os.path.exists(raw_data_path+i+".csv"):
        # dfs.append(pd.read_csv(raw_data_path + i + ".csv"))
        data = pd.read_csv(raw_data_path + i + ".csv")
        data["velocity(m/s)"].plot()
        #plt.show()
        
        compData = applyScale(data["velocity(m/s)"])
        originalData = data["velocity(m/s)"]
        counter = 1
        # rewrite this function for optimization pls
        while(computeError(originalData, removeScale(compData) < 0.0475)):
            compData[0] = compData[0].round(64 - counter)
            counter += 1

        print("final error: ",computeError(originalData, removeScale(compData)))

        decimalPlaces = 64 - counter + 1
        print("decimals is: ", decimalPlaces)

        compData[0] *= 10**(decimalPlaces)
        
        finalData = pd.concat([data["time_rel(sec)"], pd.Series(compData[0])], axis=1)
        timestamp = data["time_abs(%Y-%m-%dT%H:%M:%S.%f)"].iloc[0]


        with open("metadata_", i, ".txt", 'w') as file:
            file.write(data[1],"\n")
            file.write(data[2],"\n")
            file.write(str(decimalPlaces), "\n")
        finalData.to_csv(raw_data_path + "Compressed_" + i + "_"+ timestamp + ".csv", sep=',', index=False)
        
        break

        
