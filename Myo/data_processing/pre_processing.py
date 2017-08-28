import glob
import logging
import os
from matplotlib import pyplot
import numpy as np
from pandas import Series, read_csv
from pandas.errors import EmptyDataError
from sklearn.preprocessing import normalize
import time

def preprocess_emg(emg_file):
    file_name = os.path.basename(emg_file)
    file_path = os.path.join("C:\\Users\\Erin\\Code\\HonoursProject\\Myo\\data\\preprocessed", file_name)

    gesture_series = Series.from_csv(emg_file, header=0)
    rolling_window = gesture_series.rolling(window=4)
    rolling_mean = rolling_window.mean()
    rolling_mean.to_csv(path=file_path, na_rep=0)

    try:
        data = read_csv(file_path)
        normalised = normalize(data)
        return normalised
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty
