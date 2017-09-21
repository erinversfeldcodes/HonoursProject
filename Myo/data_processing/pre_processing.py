from utils import *

import numpy as np
import os
from pandas.errors import EmptyDataError
from scipy.signal import medfilt, butter, lfilter
from sklearn.preprocessing import normalize, scale

preprocessed_folder = os.path.abspath('data\\preprocessed_data')


def normalise_data(data):
    try:
        normalised = normalize(data)
        return normalised
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty


def median_filter(data):
    try:
        filtered = medfilt(data)
        return filtered
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty


def scale_data(data):
    try:
        scaled = scale(data)
        return scaled
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty


def full_wave_rectification(data):
    rectified_data = data
    rectified_data.flags.writeable = True
    for row in range(len(rectified_data)):
        r = data[row]
        for column_entry in range(len(r)):
            entry = r[column_entry]
            if entry < 0:
                r[column_entry] = abs(entry)

    return rectified_data


def butterworth_bandpass(cut, sampling_rate, order):
    nyq = 0.5 * sampling_rate
    cut_off = cut/nyq

    b, a = butter(order, cut_off, btype='highpass')
    return b, a


def butterworth_filter(data):
    b, a = butterworth_bandpass(0.1, 2000, order=1)
    filtered_data = lfilter(b, a, data)
    return filtered_data
