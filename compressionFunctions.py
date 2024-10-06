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

def removeScale(data, flat, middle):
    return (data*middle) + flat

def computeError(originalData, decompressedData):
    percentageChange = ((originalData - decompressedData) / originalData) * 100
    residuals = originalData - decompressedData
    residualErrorPercentage = 100*(residuals / originalData)
    return residualErrorPercentage.mean()

def compressFile(fileAddress):
    print("Now trying to compress: ",fileAddress)
    data = pd.read_csv(fileAddress)
    compressedData = applyScale(data["velocity(m/s)"])
    originalData = data["velocity(m/s)"]
    
    counter = 1
    # rewrite this function for optimization pls
    while(computeError(originalData, removeScale(compressedData[0],compressedData[1],compressedData[2])) < 0.0475):
        compressedData[0] = compressedData[0].round(32 - counter)
        counter += 1

    print("MSE: ",computeError(originalData, removeScale(compressedData[0],compressedData[1],compressedData[2])))

    decimalPlaces = 32 - counter + 1
    print("Decimal multiplication is: ", decimalPlaces)

    compressedData[0] *= 10**(decimalPlaces)
    
    finalData = pd.concat([data["time_rel(sec)"], pd.Series(compressedData[0])], axis=1)
    timestamp = data["time_abs(%Y-%m-%dT%H:%M:%S.%f)"].iloc[0]

    meta = open(raw_data_path + i + "_METADATA", 'w')

    meta.write(str(compressedData[1]) + "\n" + str(compressedData[2]))
    # Metadata file contents:
    # 1: value of lowest value on the decompressed data set
    # 2: data set normalisation factor

    print("metadata folder written")
    finalData.to_csv(raw_data_path + "Compressed_" + i +"_" + str(decimalPlaces) + "_"+ timestamp + ".csv", sep=',', index=False)
    print("Compressing complete")

    
# This function takes in the name of the compressed file (without the .csv at the end!!!)
# looks for the metadata and uses them to regain the original data
def decompressFile(file):
    print(file)
    compressedData = pd.read_csv(file + ".csv")
    print(compressedData)
    metaData = open(file + "_METADATA", 'r')
    metaData = metaData.read()
    flat = float(metaData.split('\n')[0])
    scale = float(metaData.split('\n')[1])
    print(flat, " ", scale)
    return (compressedData * scale) + flat
    


for i in filenames.to_list():
    if os.path.exists(raw_data_path+i+".csv"):
        # dfs.append(pd.read_csv(raw_data_path + i + ".csv"))
        print("Now compressing file: " + raw_data_path + i + ".csv")
        data = pd.read_csv(raw_data_path + i + ".csv")
        compressFile(raw_data_path + i + ".csv")
        decomp = decompressFile(raw_data_path + i)
        decomp.plot()
        plt.show()

        continue
        data["velocity(m/s)"].plot()
        #plt.show()
        
        compressedData = applyScale(data["velocity(m/s)"])
        originalData = data["velocity(m/s)"]
        
        counter = 1
        # rewrite this function for optimization pls
        while(computeError(originalData, removeScale(compressedData[0],compressedData[1],compressedData[2])) < 0.0475):
            compressedData[0] = compressedData[0].round(32 - counter)
            counter += 1

        print("MSE: ",computeError(originalData, removeScale(compressedData[0],compressedData[1],compressedData[2])))

        decimalPlaces = 32 - counter + 1
        print("Decimal multiplication is: ", decimalPlaces)

        compressedData[0] *= 10**(decimalPlaces)
        
        finalData = pd.concat([data["time_rel(sec)"], pd.Series(compressedData[0])], axis=1)
        timestamp = data["time_abs(%Y-%m-%dT%H:%M:%S.%f)"].iloc[0]


        
        finalData.to_csv(raw_data_path + "Metadata_" + i +"_" + str(decimalPlaces) + "_"+ timestamp + ".csv", sep=',', index=False)
        print("Compressing complete")
        
