# Import libraries
import numpy as np
import pandas as pd
from scipy.io import wavfile

# data path = where we store the data, plots and catalogue
data_path = "./data/lunar/training/"
raw_data_path = data_path + "data/S12_GradeA/"
catalogue_path = data_path + "catalogs/apollo12_catalog_GradeA_final.csv"

df = pd.read_csv(catalogue_path)
filenames = df["filename"]

dfs = []
filename = filenames.to_list()[0]
tmp = pd.read_csv(raw_data_path + filename + ".csv").iloc[73400:74400]
# print(tmp.size)

points = tmp["velocity(m/s)"]
timer_original = np.array(tmp["time_rel(sec)"])

t_n = 0
timer = []
# print(len(timer_a))
# print(timer_a)

for i in range(len(timer_original) - 1):
    timer.append(timer_original[i + 1] - timer_original[i])
timer.append(0)
timer = np.array(timer)

scale = []
for k in range(35, 65):
    note = 440 * 2 ** ((k - 49) / 12)
    if k % 12 != 0 and k % 12 != 2 and k % 12 != 5 and k % 12 != 7 and k % 12 != 10:
        scale.append(note)  # add musical note (skip half tones)
n_notes = len(scale)  # number of musical notes

# frequency
y = np.array(points)
min = np.min(y)
max = np.max(y)
yf = 10 * (y - min) / (max - min)

# volume
v = np.array(points)
min = np.min(v)
max = np.max(v)
vf = 5000 + 5000 * (1 - (v - min) / (max - min))

# duration
zf = np.array(timer)


def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave


print(len(vf), len(yf), len(zf))

wave = []
for t in range(
    len(vf)
):  # loop over dataset observations, create one note per observation
    note = int(yf[t])
    duration = zf[t]
    frequency = scale[note]
    volume = vf[t]  # 2048
    new_wave = get_sine_wave(frequency, duration=zf[t], amplitude=vf[t])
    wave = np.concatenate((wave, new_wave))
wavfile.write("sound.wav", rate=44100, data=wave.astype(np.int16))
