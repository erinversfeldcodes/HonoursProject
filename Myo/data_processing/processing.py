import string

from data_processing.feature_extraction import *
from data_processing.pre_processing import *
from data_processing.utils import *

import glob
import logging
from sklearn.model_selection import train_test_split
import os
import pandas as pd
import time

filename = "processing_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded processing.py")

myo_data_folder = os.path.abspath("data/Participant *")
conll_folder = os.path.abspath('data/conll')
feat_extr_preproc_folder = os.path.abspath('data/preproc_feat_extr')
preproc_folder = os.path.abspath('data/preprocessed')
feat_extr_folder = os.path.abspath('data/feature_extracted')


def get_emg_x_y(files, fp_flag=False):
    X, Y = [], []

    if fp_flag:
        no_columns = len(read_csv(files[0], max_num_lines=2)[0])
        columns = list(range(0, no_columns))
        no_rows = 2
        skip = 0
        files_to_read = files
    else:
        columns = [1, 2, 3, 4, 5, 6, 7, 8]
        no_rows = 200
        skip = 1
        files_to_read = []
        for file in files:
            if check_sufficient_data(file):
                files_to_read.append(file)

    # t = pd.read_csv(files_to_read[0], skiprows=skip, nrows=no_rows, header=None).as_matrix(columns)
    # l = len(t)
    # print(str(l) + ': ' + files_to_read[0])
    for file in files_to_read:
        try:
            gesture = pd.read_csv(file, skiprows=skip, nrows=no_rows, header=None).as_matrix(columns)
            gesture.flags.writeable = True
            # if len(gesture) != l:
            #     print(str(len(gesture)) + ': ' + file)
            #     i = input('proceed?')
            #     raise Exception

            if contains_nans(gesture):
                gesture = remove_nans(gesture, delete=False)

            if gesture is None or len(gesture) < no_rows:
                pass
            else:
                file_name = os.path.basename(file)
                if fp_flag is False:
                    letter = file_name[0]
                else:
                    if file_name[2] != '-':
                        letter = file_name[2]
                    else:
                        letter = file_name[3]
                X.append(gesture)
                Y.append(letter)
        except EmptyDataError:
            pass

    X, Y = np.array(X), np.array(Y)
    if X.ndim == 3:
        n_samples, n_row, n_features = X.shape
        X = X.reshape((n_samples, n_row * n_features))

    return X, Y


def get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files, fp_flag=False):
    X, Y = [], []

    for i in range(len(accelerometer_files)):
        file_name = os.path.basename(accelerometer_files[i])
        letter = ''
        for c in file_name[:5]:
            if c in string.ascii_lowercase:
                letter = c
            break
        if fp_flag is False:
            file = merge_imu_files(accelerometer_files[i], gyro_files[i], orientation_files[i], orientation_euler_files[i], letter, max_num_lines=50)
        else:
            file = merge_imu_files(accelerometer_files[i], gyro_files[i], orientation_files[i], orientation_euler_files[i], letter)

        if file:
            if fp_flag:
                no_columns = len(read_csv(file, max_num_lines=2)[0])
                columns = list(range(no_columns))
                no_rows = 2
                skip = 0
            else:
                columns = [1, 2, 3, 4, 5, 6, 7, 8]
                no_rows = 50
                skip = 1

            gesture = pd.read_csv(file, skiprows=skip, nrows=no_rows, header=None).as_matrix(columns)
            gesture.flags.writeable = True

            if contains_nans(gesture):
                gesture = remove_nans(gesture, delete=False)

            if gesture is None or gesture == []:
                pass
            else:
                letter = os.path.basename(file)[0]
                X.append(gesture)
                Y.append(letter)

    X, Y = np.array(X), np.array(Y)
    if X.ndim == 3:
        n_samples, n_row, n_features = X.shape
        X = X.reshape((n_samples, n_row * n_features))

    return X, Y


def get_emg_imu_x_y(merged_files, fp_flag=False):
    if type(merged_files) != list:
        merged_files = [merged_files]
    X, Y = [], []

    if fp_flag:
        no_columns = len(read_csv(merged_files[0], 2)[0])
        columns = list(range(no_columns))
        no_rows = 2
        skip = 0
    else:
        columns = [1, 2, 3, 4, 5, 6, 7, 8]
        no_rows = 50
        skip = 1

    for file in merged_files:
        gesture = pd.read_csv(file, skiprows=skip, nrows=no_rows, header=None).as_matrix(columns)
        if gesture is None or gesture == []:
            pass
        else:
            letter = os.path.basename(file)[0]
            X.append(gesture)
            Y.append(letter)

    X, Y = np.array(X), np.array(Y)
    if X.ndim == 3:
        n_samples, n_row, n_features = X.shape
        X = X.reshape((n_samples, n_row * n_features))

    return (X, Y)


def read_emg_data(test_user=None, fp_flag=False):
    msg = str(time.time()) + ": Reading EMG data"
    print(msg)
    logging.info(str(time.time()) + ": " + msg)

    if fp_flag == 'fp':
        emg_folder = os.path.join(feat_extr_preproc_folder, 'emg')
        emg_file_paths = get_emg_data_files(emg_folder, fp_flag=fp_flag)
    elif fp_flag == 'p':
        emg_folder = os.path.join(preproc_folder, 'emg')
        emg_file_paths = get_emg_data_files(emg_folder, fp_flag=fp_flag)
    elif fp_flag == 'f':
        emg_folder = os.path.join(feat_extr_folder, 'emg')
        emg_file_paths = get_emg_data_files(emg_folder, fp_flag=fp_flag)
    else:
        emg_folder = glob.glob(myo_data_folder)
        emg_file_paths = get_emg_data_files(emg_folder, fp_flag=fp_flag)
        if test_user:
            emg_folder = myo_data_folder.replace('*', str(test_user))

    if test_user is not None:
        # print(emg_file_paths)
        test_user_emg_file_paths = get_emg_data_files(emg_folder, test_user=test_user, fp_flag=fp_flag)
        emg_file_paths = remove_test_user_files(emg_file_paths, test_user=test_user, fp_flag=fp_flag)
        # print(test_user_emg_file_paths)
        x_test, y_test = get_emg_x_y(test_user_emg_file_paths, fp_flag=fp_flag)
        x_train, y_train = get_emg_x_y(emg_file_paths, fp_flag=fp_flag)

    else:
        X, Y = get_emg_x_y(emg_file_paths, fp_flag=fp_flag)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

    return [x_train, x_test, y_train, y_test]


def read_imu_data(test_user=None, fp_flag=False):
    msg = str(time.time()) + ": Reading IMU data"
    print(msg)
    logging.info(msg)

    if fp_flag == 'fp':
        imu_folder = os.path.join(feat_extr_preproc_folder, 'imu')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(imu_folder,
                                                                                                         fp_flag=fp_flag)
    elif fp_flag == 'p':
        imu_folder = os.path.join(preproc_folder, 'imu')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(imu_folder,
                                                                                                         fp_flag=fp_flag)
    elif fp_flag == 'f':
        imu_folder = os.path.join(feat_extr_folder, 'imu')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(imu_folder,
                                                                                                         fp_flag=fp_flag)
    else:
        imu_folder = glob.glob(myo_data_folder)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(imu_folder,
                                                                                                         fp_flag=fp_flag)
        if test_user:
            imu_folder = myo_data_folder.replace('*', str(test_user))

    if test_user is not None:
        test_user_accelerometer_files, test_user_gyro_files, test_user_orientation_files,\
        test_user_orientation_euler_files = get_imu_data_files(imu_folder, test_user=test_user, fp_flag=fp_flag)
        accelerometer_files = remove_test_user_files(accelerometer_files, test_user, fp_flag)
        gyro_files = remove_test_user_files(gyro_files, test_user, fp_flag)
        orientation_files = remove_test_user_files(orientation_files, test_user, fp_flag)
        orientation_euler_files = remove_test_user_files(orientation_euler_files, test_user, fp_flag)
        x_test, y_test = get_imu_x_y(test_user_accelerometer_files, test_user_gyro_files, test_user_orientation_files,
                                     test_user_orientation_euler_files, fp_flag=fp_flag)
        x_train, y_train = get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files,
                                       fp_flag=fp_flag)
        # print(test_user_accelerometer_files)
        # print(accelerometer_files)

    else:
        X, Y = get_imu_x_y(accelerometer_files, gyro_files, orientation_files, orientation_euler_files, fp_flag=fp_flag)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

    return [x_train, x_test, y_train, y_test]


def read_emg_and_imu_data(test_user=None, fp_flag=False):
    msg = str(time.time()) + ": Reading EMG and IMU data"
    print(msg)
    logging.info(msg)

    if fp_flag == 'fp':
        imu_folder = os.path.join(feat_extr_preproc_folder, 'imu')
        emg_folder = os.path.join(feat_extr_preproc_folder, 'emg')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_emg_and_imu_data_files(
            imu_folder, emg_folder)
    elif fp_flag == 'p':
        imu_folder = os.path.join(preproc_folder, 'imu')
        emg_folder = os.path.join(preproc_folder, 'emg')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_emg_and_imu_data_files(
            imu_folder, emg_folder)
    elif fp_flag == 'f':
        imu_folder = os.path.join(feat_extr_folder, 'imu')
        emg_folder = os.path.join(feat_extr_folder, 'emg')
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_emg_and_imu_data_files(
            imu_folder, emg_folder)
    else:
        imu_folder = glob.glob(myo_data_folder)
        emg_folder = glob.glob(myo_data_folder)
        accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files = get_emg_and_imu_data_files(
            imu_folder, emg_folder)
        if test_user:
            imu_folder = myo_data_folder.replace('*', str(test_user))
            emg_folder = myo_data_folder.replace('*', str(test_user))

    merged_files = []
    if test_user is not None:
        accelerometer_files = remove_test_user_files(accelerometer_files, test_user, fp_flag)
        emg_files = remove_test_user_files(emg_files, test_user, fp_flag)
    for i in range(len(emg_files)):
        if fp_flag:
            file_name = os.path.basename(accelerometer_files[i])
            search_segment = file_name[:4]
            letter = ''
            for c in search_segment:
                if c in string.ascii_lowercase:
                    letter = c
                    break
            if letter == '':
                print('letter not found')
                print(accelerometer_files[i])
                raise Exception
        else:
            letter = os.path.basename(accelerometer_files[i])[0]
        a = accelerometer_files[i]
        g = a.replace('accelerometer', 'gyro')
        o = a.replace('accelerometer', 'orientation')
        oe = a.replace('accelerometer', 'orientationEuler')
        e = a.replace('accelerometer', 'emg').replace('\\imu\\', '\\emg\\')
        if fp_flag:
            title_path = merge_imu_files(a, g, o, oe, letter)
        else:
            title_path = merge_imu_files(a, g, o, oe, letter, max_num_lines=50)

        if title_path:
            merged_file = combine_emg_and_imu(title_path, e)
            if merged_file:
                merged_files.append(merged_file)
        else:
            pass

    X, Y = get_emg_imu_x_y(merged_files, fp_flag=fp_flag)
    if test_user is not None:
        test_user_accelerometer_files, test_user_gyro_files, test_user_orientation_files, \
        test_user_orientation_euler_files, test_user_emg_files = get_emg_and_imu_data_files(imu_folder, emg_folder,
                                                                                            test_user=test_user)

        test_user_merged_files = []
        for i in range(len(test_user_emg_files)):
            if fp_flag:
                file_name = os.path.basename(test_user_accelerometer_files[i])
                search_segment = file_name[:4]
                letter = ''
                for c in search_segment:
                    if c in string.ascii_lowercase:
                        letter = c
                        break
                if letter == '':
                    print('letter not found')
                    print(test_user_accelerometer_files[i])
                    raise Exception
            a = test_user_accelerometer_files[i]
            g = a.replace('accelerometer', 'gyro')
            o = a.replace('accelerometer', 'orientation')
            oe = a.replace('accelerometer', 'orientationEuler')
            e = a.replace('accelerometer', 'emg').replace('\\imu\\', '\\emg\\')
            if fp_flag:
                title_path = merge_imu_files(a, g, o, oe, letter)
            else:
                title_path = merge_imu_files(a, g, o, oe, letter, max_num_lines=50)

            if title_path:
                merged_file = combine_emg_and_imu(title_path, e)
                if merged_file:
                    test_user_merged_files.append(merged_file)
            else:
                pass
        x_test, y_test = get_emg_imu_x_y(test_user_merged_files, fp_flag=fp_flag)
        x_train, y_train = X, Y

    else:
        x_train, x_test, y_train, y_test = train_test_split(X, Y)
    return x_train, x_test, y_train, y_test


def read_emg_data_conll(test_user=None, fp_flag=False):
    x_train, x_test, y_train, y_test = read_emg_data(test_user, fp_flag=fp_flag)
    x_train, y_train, x_test, y_test, train_lengths, test_lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, train_lengths, test_lengths


def read_imu_data_conll(test_user=None, fp_flag=False):
    x_train, x_test, y_train, y_test = read_imu_data(test_user, fp_flag=fp_flag)
    x_train, y_train, x_test, y_test, train_lengths, test_lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, train_lengths, test_lengths


def read_emg_and_imu_data_conll(test_user=None, fp_flag=False):
    x_train, x_test, y_train, y_test = read_emg_and_imu_data(test_user, fp_flag=fp_flag)
    x_train, y_train, x_test, y_test, train_lengths, test_lengths = gesture_to_conll(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test, train_lengths, test_lengths


def get_data(sensor_data="both", test_user=None, fp_flag=False):
    if sensor_data == "both":
        return read_emg_and_imu_data(test_user=test_user, fp_flag=fp_flag)

    elif sensor_data == "emg":
        return read_emg_data(test_user=test_user, fp_flag=fp_flag)

    elif sensor_data == "imu":
        return read_imu_data(test_user=test_user, fp_flag=fp_flag)


def get_data_conll(sensor_data="both", test_user=None, fp_flag=False):
    if sensor_data == "both":
        return read_emg_and_imu_data_conll(test_user=test_user, fp_flag=fp_flag)

    elif sensor_data == "emg":
        return read_emg_data_conll(test_user=test_user, fp_flag=fp_flag)

    elif sensor_data == "imu":
        return read_imu_data_conll(test_user=test_user, fp_flag=fp_flag)
