from Myo.data_processing.utils import *

import numpy as np
import os
import pandas as pd
from pandas import read_csv
from pandas.errors import EmptyDataError
from scipy.signal import medfilt
from sklearn.preprocessing import normalize, scale

preprocessed_folder = os.path.abspath('data\\preprocessed_data')


def preprocess(preprocessing_dict):
    data = None

    if 'mav' in preprocessing_dict:
        if data is None:
            file_path = preprocessing_dict.get('mav')
            raw_data = read_csv(file_path)
            data = moving_average(raw_data)
        else:
            data = moving_average(data)

    elif 'median_filter' in preprocessing_dict:
        if data is None:
            file_path = preprocessing_dict.get('median_filter')
            raw_data = read_csv(file_path)
            data = median_filter(raw_data)
        else:
            data = median_filter(data)

    if 'normalise_data' in preprocessing_dict:
        if data is None:
            file_path = preprocessing_dict.get('normalise_data')
            raw_data = read_csv(file_path)
            data = normalise_data(raw_data)
        else:
            data = normalise_data(data)

    if 'scale' in preprocessing_dict:
        if data is None:
            file_path = preprocessing_dict.get('scale')
            raw_data = read_csv(file_path)
            data = scale_data(raw_data)
        else:
            data = scale_data(data)

    if data is None:
        data = np.zeros((1,), dtype=np.float64)

    return data


def normalise_data(data):
    try:
        normalised = normalize(data)
        return normalised
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty


def moving_average(data):
    window_len = 10
    window = 'hanning'  # add support for flat, hamming, bartlett and blackman

    if np.array(data).ndim != 1:
        raise ValueError("Moving average cannot be calculated for multidimensional data")

    s = np.r_[data[window_len-1:0:-1], data, data[-2:-window_len-1:-1]]
    w = eval('np.' + window + '(window_len)')
    y = np.convolve(w/w.sum(), s, mode='valid')

    return y


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


def get_preprocessed_data(file, max_num_lines, columns, preproc=False, feat_extr=False):
    # print(file)
    data = None

    if check_file_not_empty(file) is False:
        return data

    if preproc:
        if feat_extr is False:  # if not feature processing, things don't get reduced to a uniform size
            if check_sufficient_data(file):
                if file in reduced_folder:
                    reduced_file = os.path.join(reduced_folder, file)
                else:
                    reduced_file = reduce_file(file, max_num_lines)  # therefore resize to the first 200 lines only

                preprocessing_options_1 = {'median_filter': reduced_file}
            else:
                return data
        else:
            preprocessing_options_1 = {'median_filter': file}

        data = preprocess(preprocessing_options_1)
    else:
        if check_sufficient_data(file) is True:
            data = pd.read_csv(file, skiprows=1, nrows=max_num_lines, header=None).as_matrix(columns)

    return data
