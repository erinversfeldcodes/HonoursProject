from Myo.data_processing.feature_extraction import *
from Myo.data_processing.pre_processing import *
from Myo.data_processing.utils import *

import glob
import logging
from sklearn.model_selection import train_test_split
import os
import time

filename = "processing_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded processing.py")

myo_data_folder = "data\\Participant *\\Myo"
conll_folder = os.path.abspath('data\\conll')
reduced_folder = os.path.abspath('data\\reduced')
processed_folder = os.path.abspath('data\\processed_data')

def test_user_emg(test_user, preproc=False, feat_extr=False):
    participant_data_folder = os.path.abspath(myo_data_folder.replace("*", str(test_user)))
    emg_regex = os.path.join(os.path.abspath(participant_data_folder), "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)

    X, Y = get_emg_x_y(emg_files, preproc=preproc, feat_extr=feat_extr)

    return [X, Y]


def test_user_imu(test_user, preproc=False, feat_extr=False):
    participant_data_folder = os.path.abspath(myo_data_folder.replace("*", str(test_user)))
    accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(participant_data_folder)

    X, Y = get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files, preproc=preproc,
                       feat_extr=feat_extr)

    return X, Y


def test_user_emg_and_imu(test_user, preproc=False, feat_extr=False):
    X, Y = [], []
    participant_data_folder = os.path.abspath(myo_data_folder.replace("*", str(test_user)))
    accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_imu_data_files(participant_data_folder, emg=True)

    for i in range(len(accelerometer_files)):
        title_path = merge_imu_files(accelerometer_files[i], gyro_files[i], orientation_files[i],
                                     orientation_euler_files[i])
        if check_sufficient_data(title_path) and check_sufficient_data(emg_files[i]):
            combined_data = combine_emg_and_imu(title_path, emg_files[i])
            gesture, label = get_emg_imu_x_y(combined_data, preproc=preproc, feat_extr=feat_extr)
            X += gesture
            Y += label
        else:
            pass

    return X, Y


def get_emg_x_y(files, preproc=False, feat_extr=False):
    X, Y = [], []

    for file in files:
        # TODO: If I've loaded the data before, just read that file and return it.
        data = get_preprocessed_data(file, max_num_lines=200, columns=[1, 2, 3, 4, 5, 6, 7, 8], preproc=preproc,
                                     feat_extr=feat_extr)
        gesture = get_data_features(data, feat_extr=feat_extr)

        if gesture is None:
            pass
        else:
            letter = os.path.basename(file)[0]
            X.append(gesture)
            Y.append(letter)

    return X, Y


def get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files, preproc=False, feat_extr=False):
    X, Y = [], []

    for i in range(len(accelerometer_files)):

        file = merge_imu_files(accelerometer_files[i], gyro_files[i], orientation_files[i], orientation_euler_files[i])
        data = get_preprocessed_data(file, max_num_lines=50, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                     preproc=preproc, feat_extr=feat_extr)
        gesture = get_data_features(data, feat_extr)

        if gesture is None:
            pass
        else:
            letter = os.path.basename(file)[0]
            X.append(gesture)
            Y.append(letter)

    return X, Y


def get_emg_imu_x_y(merged_files, preproc=False, feat_extr=False):
    if type(merged_files) != list:
        merged_files = [merged_files]
    X, Y = [], []

    for file in merged_files:
        data = get_preprocessed_data(file, max_num_lines=200,
                                     columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                                     preproc=preproc, feat_extr=feat_extr)
        gesture = get_data_features(data, feat_extr)
        if gesture is None:
            pass
        else:
            letter = os.path.basename(file)[0]
            X.append(gesture)
            Y.append(letter)

    return (X, Y)


def read_emg_data(test_user=None, preproc=False, feat_extr=False):
    msg = "Reading EMG data"
    print(msg)
    logging.info(msg)

    if test_user:
        x_test, y_test = test_user_emg(test_user, preproc=preproc, feat_extr=feat_extr)

        participant_folders = glob.glob(myo_data_folder)
        test_user_path = myo_data_folder.replace("*", str(test_user))
        participant_folders.remove(test_user_path)
        emg_file_paths = get_emg_data_files(participant_folders)

        x_train, y_train = get_emg_x_y(emg_file_paths, preproc=preproc, feat_extr=feat_extr)

    else:
        participant_folders = glob.glob(myo_data_folder)
        emg_file_paths = get_emg_data_files(participant_folders)

        X, Y = get_emg_x_y(emg_file_paths, preproc=preproc, feat_extr=feat_extr)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, 0.1)

    return [x_train, x_test, y_train, y_test]


def read_imu_data(test_user=None, preproc=False, feat_extr=False):
    msg = "Reading IMU data"
    print(msg)
    logging.info(msg)

    if test_user:
        x_test, y_test = test_user_imu(test_user, preproc=preproc, feat_extr=feat_extr)

        participant_folders = glob.glob(myo_data_folder)
        test_user_path = myo_data_folder.replace("*", str(test_user))
        participant_folders.remove(test_user_path)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(participant_folders)

        x_train, y_train = get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files,
                                       preproc=preproc, feat_extr=feat_extr)

    else:
        participant_folders = glob.glob(myo_data_folder)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(participant_folders)

        X, Y = get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files,
                           preproc=preproc, feat_extr=feat_extr)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, 0.1)

    return [x_train, x_test, y_train, y_test]


def read_emg_and_imu_data(test_user=None, preproc=False, feat_extr=False):
    msg = "Reading EMG and IMU data"
    print(msg)
    logging.info(msg)

    if test_user:
        participant_folders = glob.glob(myo_data_folder)
        test_user_path = myo_data_folder.replace("*", str(test_user))
        participant_folders.remove(test_user_path)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_imu_data_files(participant_folders, emg=True)

    else:
        participant_folders = glob.glob(myo_data_folder)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_imu_data_files(participant_folders, emg=True)

    merged_files = []
    for i in range(len(accelerometer_files)):
        print(i)
        title_path = merge_imu_files(accelerometer_files[i], gyro_files[i], orientation_files[i],
                                     orientation_euler_files[i])
        if check_sufficient_data(title_path) and check_sufficient_data(emg_files[i]):
            merged_file = combine_emg_and_imu(title_path, emg_files[i])
            merged_files.append(merged_file)
        else:
            pass

    X, Y = get_emg_imu_x_y(merged_files, preproc, feat_extr)

    if test_user:
        x_train, y_train = X, Y
        x_test, y_test = test_user_emg_and_imu(test_user=test_user, preproc=preproc, feat_extr=feat_extr)

    else:
        x_train, x_test, y_train, y_test = train_test_split(X, Y)
    return x_train, x_test, y_train, y_test


def read_emg_data_conll(test_user=None, preproc=False, feat_extr=False):
    x_train, x_test, y_train, y_test = read_emg_data(test_user, preproc, feat_extr)
    x_train, y_train, x_test, y_test, lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, lengths


def read_imu_data_conll(test_user=None, preproc=False, feat_extr=False):
    x_train, x_test, y_train, y_test = read_imu_data(test_user, preproc, feat_extr)
    x_train, y_train, x_test, y_test, lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, lengths


def read_emg_and_imu_data_conll(test_user=None, preproc=False, feat_extr=False):
    x_train, x_test, y_train, y_test = read_emg_and_imu_data(test_user, preproc, feat_extr)
    x_train, y_train, x_test, y_test, lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, lengths


def get_data(sensor_data="both", test_user=None, preproc=False, feat_extr=False):
    if sensor_data == "both":
        return read_emg_and_imu_data(test_user=test_user, preproc=preproc, feat_extr=feat_extr)

    elif sensor_data == "emg":
        return read_emg_data(test_user=test_user, preproc=preproc, feat_extr=feat_extr)

    elif sensor_data == "imu":
        return read_imu_data(test_user=test_user, preproc=preproc, feat_extr=feat_extr)


def get_data_conll(sensor_data="both", test_user=None, preproc=False, feat_extr=False):
    if sensor_data == "both":
        return read_emg_and_imu_data_conll(test_user=test_user, preproc=preproc, feat_extr=feat_extr)

    elif sensor_data == "emg":
        return read_emg_data_conll(test_user=test_user, preproc=preproc, feat_extr=feat_extr)

    elif sensor_data == "imu":
        return read_imu_data_conll(test_user=test_user, preproc=preproc, feat_extr=feat_extr)
