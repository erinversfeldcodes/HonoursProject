import csv
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

path_to_data_files = 'data/myo_data'


def read_emg_data():
    msg = "Reading EMG data"
    print(msg)
    logging.info(msg)

    X = []
    Y = []

    emg_regex = os.path.join(path_to_data_files, "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)

    for emg_file in emg_files:

        if check_gesture_contents(emg_file) is False:
            pass

        else:
            file_basename = os.path.basename(emg_file)
            letter = file_basename[0]
            time_stamp = file_basename[-14:-4]
            title = letter + ' ' + time_stamp
            title_path = os.path.join('data/processed_data', title)

            # TODO: If I've loaded the data before, just read that file and return it.
            emg_data = pd.read_csv(emg_file, skiprows=1, nrows=400, header=None).as_matrix([1, 2, 3, 4, 5, 6, 7, 8])
            gesture = emg_data.flatten()
            gesture_name = letter
            X.append(gesture)
            Y.append(gesture_name)

    return (X, Y)


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
                msg = str(time.time()) + ': ' + str(emg_file) + ' contains no data and should be removed.'
                print(msg)
                logging.error(msg)
                return False

        except Exception:
            return False

    return True


def check_imu_contents(acc_filename, gyro_filename, orientation_filename, orientation_euler_filename):
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


def read_imu_data():
    msg = "Reading IMU data"
    print(msg)
    logging.info(msg)

    X = []
    Y = []

    acc_regex = os.path.join(path_to_data_files, "*-accelerometer-*.csv")
    accelerometer_files = glob.glob(acc_regex)
    gyro_regex = os.path.join(path_to_data_files, "*-gyro-*.csv")
    gyro_files = glob.glob(gyro_regex)
    orientation_regex = os.path.join(path_to_data_files, "*-orientation-*.csv")
    orientation_files = glob.glob(orientation_regex)
    orientation_euler_regex = os.path.join(path_to_data_files, "*-orientationEuler-*.csv")
    orientation_euler_files = glob.glob(orientation_euler_regex)

    for i in range(len(accelerometer_files)):

        a = accelerometer_files[i]
        g = gyro_files[i]
        o = orientation_files[i]
        oe = orientation_euler_files[i]

        if check_imu_contents(a, g, o, oe) is False:
            pass

        else:
            file_basename = os.path.basename(a)
            letter = file_basename[0]
            timestamp = file_basename[-14:-4]
            title = letter + ' ' + timestamp
            title_path = os.path.join('data/processed_data', title)

            a = pd.read_csv(a)
            g = pd.read_csv(g)
            o = pd.read_csv(o)
            oe = pd.read_csv(oe)

            merged_data_file = ((a.merge(g, on='timestamp')).merge(o, on='timestamp')).merge(oe, on='timestamp')
            merged_data_file.to_csv(title_path, index=False)

            imu_data = pd.read_csv(title_path, skiprows=1, nrows=100, header=None).as_matrix([1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                                                              10, 11, 12, 13])

            gesture = imu_data.flatten()
            X.append(gesture)
            gesture_name = title[0]
            Y.append(gesture_name)

    return (X, Y)


def combine_emg_and_imu(merged_imu_data_file, emg_data_file):
    X = []
    Y = []
    letter = os.path.basename(emg_data_file)[0]

    output_title = str(merged_imu_data_file) + ' emg and imu '
    imu_rows = []
    emg_rows = []
    combined_rows= []

    with open(merged_imu_data_file) as imu_data_file:
        imu_reader = csv.reader(imu_data_file)
        for row in imu_reader:
            imu_rows.append(row)

    with open(emg_data_file) as emg_data_file:
        emg_reader = csv.reader(emg_data_file)
        for row in emg_reader:
            emg_rows.append(row)

    imu_row_num = 0
    with open(output_title, 'w+') as output:
        for i in range(0, 401):
            if i % 4 == 0:
                line = emg_rows[i] + imu_rows[imu_row_num][1:]
                combined_rows.append(line)
                imu_row_num += 1
            else:
                line = emg_rows[i] + ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                combined_rows.append(line)
        writer = csv.writer(output, delimiter=',')
        for row in combined_rows:
            writer.writerow(row)

    emg_and_imu_data = pd.read_csv(output_title, skiprows=1, nrows=400, header=None).as_matrix([1, 2, 3, 4, 5, 6, 7, 8,
                                                                                                9, 10, 11, 12, 13, 14,
                                                                                                15, 16, 17, 18, 19, 20,
                                                                                                21])
    gesture = emg_and_imu_data.flatten()
    X.append(gesture)
    Y.append(letter)

    return (X, Y)


def read_emg_and_imu():
    msg = "Reading EMG and IMU data"
    print(msg)
    logging.info(msg)

    X = []
    Y = []

    acc_regex = os.path.join(path_to_data_files, "*-accelerometer-*.csv")
    accelerometer_files = glob.glob(acc_regex)
    emg_regex = os.path.join(path_to_data_files, "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)

    for i in range(len(accelerometer_files)):
        acc_file = accelerometer_files[i]
        emg_file = emg_files[i]
        file_basename = os.path.basename(acc_file)
        letter = file_basename[0]
        timestamp = file_basename[-14:-4]
        title = letter + ' ' + timestamp
        title_path = os.path.join('data/processed_data', title)

        if check_gesture_contents(emg_file) is False:
            pass

        else:
            try:
                gesture, target = combine_emg_and_imu(title_path, emg_file)
                X.append(gesture)
                Y.append(target)

            except Exception as e:
                logging.error(e.message)

                read_imu_data()
                gesture, target = combine_emg_and_imu(title_path, emg_file)
                X.append(gesture)
                Y.append(target)

    return (X, Y)




