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
        a = accelerometer_files[i]
        g = a.replace('accelerometer', 'gyro')
        o = a.replace('accelerometer', 'orientation')
        oe = a.replace('accelerometer', 'orientationEuler')
        letter = ''
        for c in a[:5]:
            if c in string.ascii_lowercase:
                letter = c
            break
        if fp_flag is False:
            file = merge_imu_files(a, g, o, oe, letter, max_num_lines=50)
        else:
            file = merge_imu_files(a, g, o, oe, letter)

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


def get_x_y(files):
    X = []
    Y = []

    no_columns = len(read_csv(files[0], 2)[0])
    columns = list(range(no_columns))
    no_rows = 2
    skip = 0

    for file in files:
        letter = os.path.basename(file)[0]
        gesture = pd.read_csv(file, skiprows=skip, nrows=no_rows, header=None).as_matrix(columns)
        if gesture is None or gesture == []:
            pass
        else:
            X.append(gesture)
            Y.append(letter)

    X, Y = np.array(X), np.array(Y)
    if X.ndim == 3:
        n_samples, n_row, n_features = X.shape
        X = X.reshape((n_samples, n_row * n_features))

    return (X, Y)

def merge_files(emg, accelerometer, gyro, orientation, orientation_euler):
    basename = os.path.basename(emg)
    letter_search = basename[0:4]
    letter = ''
    for c in letter_search:
        if c in string.ascii_lowercase:
            letter = c
            break

    fp_merged_path = os.path.abspath('data/feature_extracted_preprocessed/merged')
    imu_file = merge_imu_files(accelerometer, gyro, orientation, orientation_euler, letter, path=fp_merged_path)
    if imu_file:
        merged = combine_emg_and_imu(imu_file, emg)
        return merged
    else:
        return imu_file


def get_pf_data_both(test_user):
    test_data = []
    train_data = []

    path = os.path.abspath('data/feature_extracted_preprocessed')
    emg_dir = os.path.join(path, 'emg')
    imu_dir = os.path.join(path, 'imu')

    emg_files = os.listdir(emg_dir)
    imu_files = os.listdir(imu_dir)

    emg_train = []
    emg_test = []
    imu_train = []
    imu_test = []

    for file in emg_files:
        if file[:len(str(test_user))].isdigit() and int(file[:len(str(test_user))]) == test_user:
            if file[:len(str(test_user)) + 1].isdigit():
                emg_train.append(file)
            else:
                emg_test.append(file)
        else:
            emg_train.append(file)
    for file in imu_files:
        if file[:len(str(test_user))].isdigit() and int(file[:len(str(test_user))]) == test_user:
            if file[:len(str(test_user)) + 1].isdigit():
                imu_train.append(file)
            else:
                imu_test.append(file)
        else:
            imu_train.append(file)

    for file in emg_test:
        if file in emg_train:
            print('emg FUCK WHY')
            break

    for file in imu_test:
        if file in imu_train:
            print('imu FUCK WHY')
            break

    for file in emg_test:
        a_file = file.replace('emg', 'accelerometer')
        g_file = file.replace('emg', 'gyro')
        o_file = file.replace('emg', 'orientation')
        oe_file = file.replace('emg', 'orientationEuler')
        e_path = os.path.join(emg_dir, file)
        a_path = os.path.join(imu_dir, a_file)
        g_path = os.path.join(imu_dir, g_file)
        o_path = os.path.join(imu_dir, o_file)
        oe_path = os.path.join(imu_dir, oe_file)
        test_gesture = merge_files(e_path, a_path, g_path, o_path, oe_path)

        if test_gesture:
            test_data.append(test_gesture)

    for file in emg_train:
        a_file = file.replace('emg', 'accelerometer')
        g_file = file.replace('emg', 'gyro')
        o_file = file.replace('emg', 'orientation')
        oe_file = file.replace('emg', 'orientationEuler')
        e_path = os.path.join(emg_dir, file)
        a_path = os.path.join(imu_dir, a_file)
        g_path = os.path.join(imu_dir, g_file)
        o_path = os.path.join(imu_dir, o_file)
        oe_path = os.path.join(imu_dir, oe_file)
        gesture = merge_files(e_path, a_path, g_path, o_path, oe_path)

        if gesture:
            train_data.append(gesture)

    for file in test_data:
        if file in train_data:
            print('FUCK WHY merged')

    x_test, y_test = get_x_y(test_data)
    x_train, y_train = get_x_y(train_data)

    return x_train, x_test, y_train, y_test

if __name__ == '__main__':
    get_pf_data_both(2)
