import pandas as pd
import glob
import matplotlib.pyplot as plt
from cut_data import get_seismic_events
from compressionFunctions import compressFile

# where we store the data, plots and catalogue
lunar_test_data_path = "./data/lunar/test/data/S12_GradeB/"
mars_test_data_path = "./data/mars/test/data/"

for test_data_filename in glob.glob(lunar_test_data_path + "*.csv") + glob.glob(mars_test_data_path + "*.csv"):
    print(test_data_filename, lunar_test_data_path[2:])
    df = pd.read_csv(test_data_filename)
    str_name = "velocity(m/s)"
    sample = get_seismic_events(df, str_name)
    if len(sample) > 0:
        sample_file_name = ""
        if lunar_test_data_path[2:] in test_data_filename:
            sample_file_name = test_data_filename.replace(lunar_test_data_path, "output/")
        if mars_test_data_path[2:] in test_data_filename:
            sample_file_name = test_data_filename.replace(mars_test_data_path, "output/")

        sample.to_csv(sample_file_name, index=False)
        sample[str_name].plot()
        plt.show()
        
        compressFile(sample_file_name)

