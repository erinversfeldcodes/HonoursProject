import glob
import logging
import numpy as np
import os
import pandas as pd
import time

filename = "processing_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded processing.py")


def read_emg_data(path_to_emg_files_list=None, step=180):

    X = []
    Y = []
    processed_data_path = os.path.abspath("data/processed_data")

    for path_to_file in path_to_emg_files_list:  # TODO: include checks for empty files
        if check_gesture_contents(path_to_file) is False:
            pass

        else:
            emg_filename = os.path.basename(path_to_file)

            for i in range(0, 1000, step):
                gesture = pd.read_csv(path_to_file, skiprows=[i], nrows=step, header=None).as_matrix(
                [1, 2, 3, 4, 5, 6, 7, 8])  # returns a numpy array, which I can use in train_split

                gesture = gesture.flatten()

                if len(gesture) == step * 8:
                    gesture = gesture[8:]
                    X.append(gesture)
                    gesture_name = emg_filename[0]
                    Y.append(gesture_name)

    X_path = os.path.join(processed_data_path, "X.npy")
    Y_path = os.path.join(processed_data_path, "Y.npy")
    np.save(X_path, X)
    np.save(Y_path, Y)

    return X, Y


def files_match(acc_filename, gyro_filename, orientation_filename, orientation_euler_filename):
    gyro_replacement = acc_filename.replace("accelerometer", "gyro")
    orientation_replacement = acc_filename.replace("accelerometer", "orientation")
    orientation_euler_replacement = acc_filename.replace("accelerometer", "orientationEuler")

    match = (gyro_replacement == gyro_filename) and (orientation_replacement == orientation_filename) and (orientation_euler_replacement == orientation_euler_filename)

    return match


def check_gesture_contents(emg_file):
    with open(emg_file) as file:
        contents = file.read()

        try:
            lines = contents.split('\n')

            try:
                lines.remove('')
            except Exception:
                pass
            if len(lines) <= 1:
                return False

        except Exception:
            return False

    return True


def check_spatial_contents(acc_filename, gyro_filename, orientation_filename, orientation_euler_filename):
    with open(acc_filename) as file:
        contents = file.read()

        try:
            lines = contents.split('\n')
            try:
                lines.remove('')
            except Exception:
                pass
            if len(lines) <= 1:
                return False

        except Exception:
            return False

    with open(gyro_filename) as file:
        contents = file.read()

        try:
            lines = contents.split('\n')
            if len(lines) <= 1:
                return False

        except Exception:
            return False

    with open(orientation_filename) as file:
        contents = file.read()

        try:
            lines = contents.split('\n')
            if len(lines) <= 1:
                return False

        except Exception:
            return False

    with open(orientation_euler_filename) as file:
        contents = file.read()

        try:
            lines = contents.split('\n')
            if len(lines) <= 1:
                return False

        except Exception:
            return False

    return True


def read_spatial_data(acc_files, gyro_files, orientation_files, orientation_euler_files, step):
    X = []
    Y = []

    for i in range(0, len(acc_files)):

        acc_filename = acc_files[i]
        gyro_filename = gyro_files[i]
        orientation_filename = orientation_files[i]
        orientation_euler_filename = orientation_euler_files[i]

        if check_spatial_contents(acc_filename, gyro_filename, orientation_filename, orientation_euler_filename) is False:
            pass  # for whatever reason no data was recorded, so ignore it

        else:
            title = os.path.basename(acc_filename)[0] + ' ' + os.path.basename(acc_filename)[-14:-4]
            title_path = os.path.join('data/processed_data', title)

            a = pd.read_csv(acc_filename)
            g = pd.read_csv(gyro_filename)
            o = pd.read_csv(orientation_filename)
            oe = pd.read_csv(orientation_filename)

            merged_data = ((a.merge(g, on='timestamp')).merge(o, on='timestamp')).merge(oe, on='timestamp')
            merged_csv = merged_data.to_csv(title_path, index=False)

            for j in range(0, 1000, step):
                gesture = pd.read_csv(title_path, skiprows=[j], nrows=step, header=None).as_matrix(
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

                gesture = gesture.flatten()

                if len(gesture) == step * 14:
                    gesture = gesture[14:]
                    X.append(gesture)
                    gesture_name = title[0]
                    Y.append(gesture_name)

    X_path = os.path.join('data/processed_data', "X.npy")
    Y_path = os.path.join('data/processed_data', "Y.npy")
    np.save(X_path, X)
    np.save(Y_path, Y)

    return X, Y


def read_data(step):
    X = []
    Y = []

    path_to_data_files = os.path.abspath('data/myo_data')
    path_to_merged_files = os.path.abspath('data/processed_data')

    emg_regex = os.path.join(path_to_data_files, "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)

    for i in range(0, len(emg_files)):

        emg_file_path = emg_files[i]
        emg_filename = os.path.basename(emg_file_path)
        letter = emg_filename[0]
        time_stamp = emg_filename[-14:-4]

        merged_regex = os.path.join(path_to_merged_files, str(letter) + ' ' + str(time_stamp))
        merged_file = glob.glob(merged_regex)

        if check_gesture_contents(emg_file_path) is False:
            pass  # for whatever reason no data was recorded, so ignore it

        else:

            title = os.path.basename(merged_file) + ' with emg'
            title_path = os.path.join('data/processed_data', title)

            m = pd.read_csv(merged_file)
            e = pd.read_csv(emg_file_path)

            merged_data = m.merge(e, on='timestamp')
            merged_csv = merged_data.to_csv(title_path, index=False)

            for j in range(0, 1000, step):
                gesture = pd.read_csv(title_path, skiprows=[j], nrows=step, header=None).as_matrix(
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

                gesture = gesture.flatten()

                if len(gesture) == step * 22:
                    gesture = gesture[22:]
                    X.append(gesture)
                    gesture_name = title[0]
                    Y.append(gesture_name)

    X_path = os.path.join('data/processed_data', "X.npy")
    Y_path = os.path.join('data/processed_data', "Y.npy")
    np.save(X_path, X)
    np.save(Y_path, Y)

    return X, Y
