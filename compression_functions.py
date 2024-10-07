# Import libraries
import pandas as pd


def apply_scale(data) -> list:
    top = data.max()
    bottom = data.min()
    data = data - bottom  # remove the minimum value from all data points
    data = data / (top - bottom)  # divide by the range

    # output_path = raw_data_path + "scaletest" + ".csv"
    # data.to_csv(output_path, index=False)

    return [data, bottom, top - bottom]


def remove_scale(data, flat, middle):
    return (data * middle) + flat


def compute_error(original_data: pd.Series, decompressed_data):
    # percentage_change = (
    # (original_data - decompressed_data) / original_data) * 100
    residuals = original_data - decompressed_data
    residual_error_percentage = 100 * (residuals / original_data)
    return residual_error_percentage.mean()


def compress_file(
        file_address: str, output_dir: str, velocity_col: str) -> None:
    print("Now trying to compress:", file_address)
    data = pd.read_csv(file_address)
    compressed_data = apply_scale(data[velocity_col])
    original_data = data[velocity_col]

    counter = 1
    # rewrite this function for optimization pls
    while (
        compute_error(
            original_data,
            remove_scale(compressed_data[0],
                         compressed_data[1], compressed_data[2]),
        )
        < 0.0475
    ):
        compressed_data[0] = compressed_data[0].round(32 - counter)
        counter += 1

    print(
        "MSE:",
        compute_error(
            original_data,
            remove_scale(compressed_data[0],
                         compressed_data[1], compressed_data[2]),
        )
    )

    decimal_places = 32 - counter + 1
    print("Decimal multiplication is:", decimal_places)

    compressed_data[0] *= 10 ** (decimal_places)

    final_data = pd.concat(
        [data["time_rel(sec)"], pd.Series(compressed_data[0])], axis=1
    )
    timestamp = data["time_abs(%Y-%m-%dT%H:%M:%S.%f)"].iloc[0]

    file_start_name = file_address.split("/")[-1][:-4]

    with open(output_dir + file_start_name + "_METADATA", "w") as meta:
        meta.write(str(compressed_data[1]) + "\n" + str(compressed_data[2]))
        # Metadata file contents:
        # 1: value of lowest value on the decompressed data set
        # 2: data set normalisation factor

    print("metadata written")
    final_data.to_csv(
        output_dir
        + "Compressed_"
        + file_start_name
        + "_"
        + str(decimal_places)
        + "_"
        + timestamp
        + ".csv",
        sep=",",
        index=False,
    )
    print("Compressing complete")


# This function takes in the name of the compressed file (with the .csv at the end)
# looks for the metadata and uses them to regain the original data
def decompress_file(file, velocity_col):
    print(file)
    compressed_data = pd.read_csv(file)
    print(compressed_data)
    meta_data = open(file[:-4] + "_METADATA", "r")
    meta_data = meta_data.read()
    flat = float(meta_data.split("\n")[0])
    scale = float(meta_data.split("\n")[1])
    print(flat, " ", scale)
    compressed_data[velocity_col] = (
        compressed_data[velocity_col] * scale) + flat
    return compressed_data


# for i in filenames.to_list():
#     if os.path.exists(raw_data_path + i + ".csv"):
#         # dfs.append(pd.read_csv(raw_data_path + i + ".csv"))
#         print("Now compressing file: " + raw_data_path + i + ".csv")
#         data = pd.read_csv(raw_data_path + i + ".csv")
#         compress_file(raw_data_path + i + ".csv")
#         decomp = decompress_file(raw_data_path + i)
#         decomp.plot()
#         plt.show()
#
#         continue
#         data["velocity(m/s)"].plot()
#         # plt.show()
#
#         compressed_data = apply_scale(data["velocity(m/s)"])
#         original_data = data["velocity(m/s)"]
#
#         counter = 1
#         # rewrite this function for optimization pls
#         while (
#             compute_error(
#                 original_data,
#                 remove_scale(
#                     compressed_data[0], compressed_data[1], compressed_data[2]
#                 ),
#             )
#             < 0.0475
#         ):
#             compressed_data[0] = compressed_data[0].round(32 - counter)
#             counter += 1
#
#         print(
#             "MSE: ",
#             compute_error(
#                 original_data,
#                 remove_scale(
#                     compressed_data[0], compressed_data[1], compressed_data[2]
#                 ),
#             ),
#         )
#
#         decimal_places = 32 - counter + 1
#         print("Decimal multiplication is: ", decimal_places)
#
#         compressed_data[0] *= 10 ** (decimal_places)
#
#         final_data = pd.concat(
#             [data["time_rel(sec)"], pd.Series(compressed_data[0])], axis=1
#         )
#         timestamp = data["time_abs(%Y-%m-%dT%H:%M:%S.%f)"].iloc[0]
#
#         final_data.to_csv(
#             raw_data_path
#             + "Metadata_"
#             + i
#             + "_"
#             + str(decimal_places)
#             + "_"
#             + timestamp
#             + ".csv",
#             sep=",",
#             index=False,
#         )
#         print("Compressing complete"
