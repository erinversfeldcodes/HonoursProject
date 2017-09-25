from multiprocessing import Process

from data_processing.feature_extraction import *
from data_processing.utils import check_file_not_empty
from data_processing.pre_processing import *

import glob
import os
import pandas as pd
from pandas import DataFrame

myo_data_folder = "..\\data\\vanilla\\Participant *"
processed_emg_data = "..\\data\\preprocessed\\emg"
processed_imu_data = "..\\data\\preprocessed\\imu"
feat_extr_emg_data = "..\\data\\feature_extracted\\emg"
feat_extr_imu_data = "..\\data\\feature_extracted\\imu"
feat_extr_preproc_emg_data = "..\\data\\feature_extracted_preprocessed\\emg"
feat_extr_preproc_imu_data = "..\\data\\feature_extracted_preprocessed\\imu"
conll_folder = os.path.abspath('..\\data\\conll')
reduced_folder = os.path.abspath('..\\data\\reduced')


def preprocess_emg_data(p_num, emg_files):
    for file in emg_files:
        if check_file_not_empty(file) is True:
            name = os.path.basename(file)
            new_name = "-".join([str(p_num), name])
            new_path = os.path.join(processed_emg_data, new_name)

            data = pd.read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3, 4, 5, 6, 7, 8])
            median_filtered_data = median_filter(data)
            normalised_data = normalise_data(median_filtered_data)
            scaled_data = scale_data(normalised_data)
            rectified_data = full_wave_rectification(scaled_data)
            if contains_nans(rectified_data):
                rectified_data = remove_nans(rectified_data)
                if len(rectified_data) > 0:
                    pass
                else:
                    break
            df = DataFrame(rectified_data)
            df.to_csv(new_path)
            print(new_path)

        else:
            pass


def preprocess_imu_data(p_num, imu_files):
    for file in imu_files:
        if check_file_not_empty(file) is True:
            name = os.path.basename(file)
            new_name = "-".join([str(p_num), name])
            new_path = os.path.join(processed_imu_data, new_name)

            if 'orientationEuler' in file or 'orientation' not in file:
                data = pd.read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3])
            else:
                data = pd.read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3, 4])
            if contains_nans(data):
                data = remove_nans(data)
                if len(data) > 0:
                    pass
                else:
                    break
            normalised_data = normalise_data(data)
            scaled_data = scale_data(normalised_data)
            df = DataFrame(scaled_data)
            df.to_csv(new_path)
            print(new_path)

        else:
            pass


def feature_extract_emg_data(p_num, preproc=True):
    if preproc is True:
        path_prefix = processed_emg_data
        regex_prefix = str(p_num) + "-"
        path_out = feat_extr_preproc_emg_data
    else:
        path_prefix = os.path.abspath(myo_data_folder.replace("*", str(p_num)))
        regex_prefix = ''
        path_out = feat_extr_emg_data

    emg_regex = os.path.join(path_prefix, regex_prefix + "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)

    for file in emg_files:
        if check_sufficient_data(file):
            name = os.path.basename(file)
            new_path = os.path.join(path_out, str(p_num) + '-' + name)
            features = []
            data = read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3, 4, 5, 6, 7, 8])
            for i in range(0, len(data), 100):  # TODO: Rerun feat_extr_preproc with step set to 100
                window_features = []
                current_window = data[i:i+200]
                if len(current_window) < 200:
                    break
                else:
                    mav = mean_absolute_value(current_window)
                    moving_av = moving_average(current_window, 200, 'hamming')
                    sd = standard_deviation(current_window)
                    ar_coeffs = ar_coefficients(data)
                    zero_x = zero_crossings(data)

                    for i in range(len(mav)):
                        window_features.append(mav[i])
                        window_features.append(moving_av[i])
                        window_features.append(sd[i])
                    window_features += ar_coeffs
                    window_features += zero_x
                if window_features:
                    features.append(window_features)
                else:
                    pass

            write_csv(new_path, len(features), features)
            print(new_path)
        else:
            pass


def feature_extract_imu_data(p_num, preproc=True):
    imu_files = []
    if preproc is True:
        path_prefix = processed_imu_data
        regex_prefix = str(p_num) + "-"
        path_out = feat_extr_preproc_imu_data
    else:
        path_prefix = os.path.abspath(myo_data_folder.replace("*", str(p_num)))
        regex_prefix = ''
        path_out = feat_extr_imu_data

    acc_regex = os.path.join(path_prefix, regex_prefix + "*-accelerometer-*.csv")
    imu_files += glob.glob(acc_regex)
    gyro_regex = os.path.join(path_prefix, regex_prefix + "*-gyro-*.csv")
    imu_files += glob.glob(gyro_regex)
    o_regex = os.path.join(path_prefix, regex_prefix + "*-orientation-*.csv")
    imu_files += glob.glob(o_regex)
    oe_regex = os.path.join(path_prefix, regex_prefix + "*-orientationEuler-*.csv")
    imu_files += glob.glob(oe_regex)

    for file in imu_files:
        if check_file_not_empty(file) is True:
            features = []
            name = os.path.basename(file)
            new_path = os.path.join(path_out, str(p_num) + '-' + name)

            if 'orientationEuler' in file or 'orientation' not in file:
                data = pd.read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3])
            else:
                data = pd.read_csv(file, skiprows=1, header=None).as_matrix([1, 2, 3, 4])
            for i in range(0, len(data), 25):
                window_features = []
                current_window = data[i:i+50]
                if len(current_window) < 50:
                    break
                else:
                    mav = mean_absolute_value(current_window)
                    sd = standard_deviation(current_window)

                    for i in range(len(mav)):
                        window_features.append(mav[i])
                        window_features.append(sd[i])
                if window_features:
                    features.append(window_features)
                else:
                    pass

            write_csv(new_path, len(features), features)
            print(new_path)
        else:
            pass


def feature_extract_with_preproc(p_num):
    feature_extract_emg_data(p_num)
    feature_extract_imu_data(p_num)


def feature_extract(p_num):
    feature_extract_emg_data(p_num, preproc=False)
    feature_extract_imu_data(p_num, preproc=False)


if __name__ == "__main__":

    participant_numbers = [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                           35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48]

    for p_num in participant_numbers:
        p_folder = os.path.abspath(myo_data_folder.replace("*", str(p_num)))
        emg_regex = os.path.join(p_folder, "*-emg-*.csv")
        emg_files = glob.glob(emg_regex)

        imu_files = []
        acc_regex = os.path.join(p_folder, "*-accelerometer-*.csv")
        imu_files += glob.glob(acc_regex)
        gyro_regex = os.path.join(p_folder, "*-gyro-*.csv")
        imu_files += glob.glob(gyro_regex)
        o_regex = os.path.join(p_folder, "*-orientation-*.csv")
        imu_files += glob.glob(o_regex)
        oe_regex = os.path.join(p_folder, "*-orientationEuler-*.csv")
        imu_files += glob.glob(oe_regex)

        pe_thread = Process(target=preprocess_emg_data, args=(p_num, emg_files))
        pi_thread = Process(target=preprocess_imu_data, args=(p_num, imu_files))
        fe_thread = Process(target=feature_extract, args=(p_num))
        pe_thread.start()
        pi_thread.start()
        fe_thread.start()
        pe_thread.join()
        pi_thread.join()
        fe_thread.join()
        feature_extract_with_preproc(p_num)
        pe_thread.terminate()
        pi_thread.terminate()
        fe_thread.terminate()
