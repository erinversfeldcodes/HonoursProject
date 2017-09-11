from biosppy.signals.tools import zero_cross as zero_crossings
import numpy as np
import os
from seqlearn.datasets import load_conll
from statsmodels.tsa.ar_model import AR

conll_folder = os.path.abspath('data\\conll')


def zero_crossing_coefficients(data):
    zero_x_list = list(zero_crossings(data)[0])
    selected_zeros = [zero_x_list[0], zero_x_list[1], zero_x_list[2], zero_x_list[8]]
    return selected_zeros


def calculate_ar_coefficients(data):
    # try:
    one_D = np.array(np.array(data).flat)
    model = AR(one_D, missing='drop')
    nobs = one_D.shape[0]
    maxlag = nobs - 1
    fitted_model = model.fit(maxlag=maxlag)
    coefficients = fitted_model.params

    try:
        third, fourth, fifth, sixth = coefficients[2], coefficients[3], coefficients[4], coefficients[5]
        return [third, fourth, fifth, sixth]
    except IndexError:
        coeffs = []

        for i in range(3, 6):
            try:
                coeffs.append(coefficients[i])
            except IndexError:
                coeffs.append(0.0)

        return coeffs


def get_features(feature_options_dict):
    features = []

    if 'AR' in feature_options_dict:
        raw_data = feature_options_dict.get('AR')
        data = calculate_ar_coefficients(raw_data)
        features += data

    if 'zero-x' in feature_options_dict:
        raw_data = feature_options_dict.get('zero-x')
        data = zero_crossing_coefficients(raw_data)
        features += data

    return features


def extract_features(sequence, i):
    yield sequence[i]


def write_conll_file(file_name, data, data_labels):
    path_to_conll_file = os.path.join(conll_folder, file_name)
    with open(path_to_conll_file, "w+") as file:
        for i in range(len(data)):
            feature_set = data[i]
            line = ''
            for feature in feature_set:
                line += str(feature) + ' '
            line += data_labels[i] + '\n'
            file.write(line)

    return path_to_conll_file


def gesture_to_conll(train_data, test_data, train_labels, test_labels):
    path_to_train_file = write_conll_file("train_gestures.txt", train_data, train_labels)
    path_to_test_file = write_conll_file("test_gestures.txt", test_data, test_labels)

    x_train, y_train, train_lengths = load_conll(path_to_train_file, extract_features)
    x_test, y_test, test_lengths = load_conll(path_to_test_file, extract_features)
    return x_train, y_train, x_test, y_test, train_lengths, test_lengths


def get_data_features(data, feat_extr):
    gesture = None

    if feat_extr is not False:
        if data is not None:  # the file had insufficient data and should be ignored
            feature_options = {'AR': data, 'zero-x': data}
            gesture = get_features(feature_options)
    else:
        if data is not None:
            gesture = data.flatten()

    return gesture
