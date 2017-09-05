from Myo.data_processing.utils import *
from Myo.data_processing.emg import *
import biosppy.signals.emg.emg as emg
import numpy as np
import pandas as pd
from pandas import Series, read_csv
from pandas.errors import EmptyDataError
from scipy.signal import medfilt
from sklearn.preprocessing import normalize, scale

preprocessed_folder = os.path.abspath('data\\preprocessed_data')


def preprocess(preprocessing_dict):
    data = None

    if 'cancui' in data:
        filter = EMG_filter()
        file_path = preprocessing_dict.get('cancui')
        raw_data = read_csv(file_path)
        data = filter.filter(raw_data)
        return data

    if 'biosspy' in data:
        file_path = preprocessing_dict.get('cancui')
        raw_data = read_csv(file_path)
        _, data, _ = emg(signal=raw_data)
        return data

    elif 'median_filter' in preprocessing_dict:
        file_path = preprocessing_dict.get('median_filter')
        data = median_filter(file_path)

    if 'normalise_data' in preprocessing_dict:
        if data is None:
            file_path = preprocessing_dict.get('normalise_data')
            data = normalise_data(file_path)
        else:
            data = normalise_data(data)

    if 'scale' in preprocessing_dict:
        axis = preprocessing_dict.get('scale')[1]
        with_mean = preprocessing_dict.get('scale')[2]
        if with_mean == 'default':
            with_mean = True
        with_std = preprocessing_dict.get('scale')[3]
        if with_std == 'default':
            with_std = True
        copy = preprocessing_dict.get('scale')[4]
        if copy == 'default':
            copy = True
        if data is None:
            file_path = preprocessing_dict.get('scale')[0]
            data = scale_data(file_path, axis, with_mean, with_std, copy)
        else:
            data = scale_data(file_path, axis, with_mean, with_std, copy)

    if data is None:
        data = np.zeros((1,), dtype=np.float64)

    return data


def normalise_data(data):
    data_type = type(data)
    if data_type == str:
        try:
            data = read_csv(data)
            normalised = normalize(data)
            return normalised
        except EmptyDataError:
            empty = np.zeros((1,), dtype=np.float64)
            return empty
    else:
        try:
            normalised = normalize(data)
            return normalised
        except EmptyDataError:
            empty = np.zeros((1,), dtype=np.float64)
            return empty


def median_filter(file_path):
    try:
        data = read_csv(file_path)
        filtered = medfilt(data)
        return filtered
    except EmptyDataError:
        empty = np.zeros((1,), dtype=np.float64)
        return empty


def scale_data(data, axis, with_mean, with_std, copy):
    data = scale(data, axis=axis, with_mean=with_mean, with_std=with_std, copy=copy)
    return data


def get_preprocessed_data(file, max_num_lines, columns, preproc=False, feat_extr=False):
    data = None

    if preproc:
        if feat_extr is False:  # if not feature processing, things don't get reduced to a uniform size
            if check_sufficient_data(file):
                if file in reduced_folder:
                    reduced_file = os.path.join(reduced_folder, file)
                else:
                    reduced_file = reduce_file(file, max_num_lines)  # therefore resize to the first 200 lines only
                data = preprocess(reduced_file)
        else:
            data = preprocess(file)
    else:
        if check_sufficient_data(file) is True:
            data = pd.read_csv(file, skiprows=1, nrows=max_num_lines, header=None).as_matrix(columns)

    return data
