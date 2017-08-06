import numpy as np
import os
import re
import sys

# if sys.argv[1] or (sys.argv[1] and sys.argv[2]):
#     sys.path.append(sys.argv[1])
#     if sys.argv[2]:
#         sys.path.append(sys.argv[2])
# else:
#     sys.path.append("C:\\Users\\Erin\\Downloads\\WinPython-64bit-2.7.10.3\\python-2.7.10.amd64\\Lib\\site-packages\\scipy\\")
#     sys.path.append("C:\\Users\\Erin\\Downloads\\WinPython-64bit-2.7.10.3\\python-2.7.10.amd64\\Lib\\site-packages\\sklearn")

from scipy import signal


def generate_order_of_gestures(path_to_files=None, total_participants=50, total_rounds=26):
    # construct ordered list of gestures
    gestures = []
    for participant_number in range(0, total_participants):
        for round_number in range(0, total_rounds):
            filename = str(participant_number) + "-" + str(round_number) + ".txt"
            if path_to_files:
                with open(str(path_to_files) + "/" + filename) as data_file:
                    file_contents = data_file.read()
                    gestures += file_contents.split(',')
                    gestures[:] = [gesture for gesture in gestures if gesture != '']
            else:
                path = os.path.abspath("DataGathering/orders/")
                with open(path + "/" + filename) as data_file:
                    file_contents = data_file.read()
                    gestures += file_contents.split(',')
                    gestures[:] = [gesture for gesture in gestures if gesture != '']

    return gestures


def rename_data_file(time_stamp, gesture, data_type, path_to_file=None):
    original_data_filename = data_type + "-" + str(time_stamp) + ".csv"
    new_filename = str(gesture) + "-" + str(original_data_filename)

    if path_to_file:
        path = path_to_file
    else:
        path = os.path.abspath("data/myo_data/")
    os.rename(path + "/" + original_data_filename, path + "/" + new_filename)

    return new_filename


def rename_data_files(time_stamps, order_of_gestures, path_to_file=None):
    new_filenames = []
    number_of_files = len(time_stamps) * 5

    for i in range(0, number_of_files):
        time_stamp = time_stamps[i]
        gesture = order_of_gestures[i]

        new_filenames.append(rename_data_file(time_stamp=time_stamp, gesture=gesture, data_type="accelerometer",
                                              path_to_file=path_to_file))
        new_filenames.append(rename_data_file(time_stamp=time_stamp, gesture=gesture, data_type="emg",
                                              path_to_file=path_to_file))
        new_filenames.append(rename_data_file(time_stamp=time_stamp, gesture=gesture, data_type="gyro",
                                              path_to_file=path_to_file))
        new_filenames.append(rename_data_file(time_stamp=time_stamp, gesture=gesture, data_type="orientation",
                                              path_to_file=path_to_file))
        new_filenames.append(rename_data_file(time_stamp=time_stamp, gesture=gesture, data_type="orientationEuler",
                                              path_to_file=path_to_file))

    return new_filenames


def condense_data(time_stamp, path_to_files=None):
    if path_to_files:
        path = path_to_files
    else:
        path = os.path.abspath("data/myo_data/")

    acc_data_file = path + "/" + "(.*accelerometer-" + str(time_stamp) + ".csv)"
    emg_data_file = path + "/" + "(.*emg-" + str(time_stamp) + ".csv)"
    gyro_data_file = path + "/" + "(.*gyro-" + str(time_stamp) + ".csv)"
    orientation_data_file = path + "/" + "(.*orientation-" + str(time_stamp) + ".csv)"
    orientationEuler_data_file = path + "/" + "(.*orientationEuler-" + str(time_stamp) + ".csv)"

    files = [acc_data_file, emg_data_file, gyro_data_file, orientation_data_file, orientationEuler_data_file]
    condensed_data = []

    for data_file in files:
        with open(data_file) as file:
            file_contents = file.read()
            lines = file_contents.split('\n')

            file_data = lines[1].split(',')

            for line in range(2, len(lines)):
                line_contents = line.split(',')

                if file != emg_data_file:
                    for index in range(0, len(line_contents)):
                        file_data[index] += line_contents[index]

                    for variable_measured in file_data:
                        variable_measured = variable_measured / len(lines)

                    condensed_data += file_data
                else:
                    t = np.linespace(-1, 1, 200, endpoint=False)
                    sig = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)
                    widths = np.arrange(1, 31)
                    continuous_wavelet_matrix = signal.cwt(sig, signal.ricker, widths)

                    condensed_data += continuous_wavelet_matrix[0]
                    condensed_data += continuous_wavelet_matrix[1]

    return condensed_data


def get_performance_time_stamps(path_to_files=None):
    time_stamps = []

    if path_to_files:
        data_files_list = os.listdir(path_to_files)
    else:
        path = os.path.abspath("data/myo_data/")
        data_files_list = os.listdir(path)
    regex = '[.*acgmleurioyntsvE-]+'

    for filename in data_files_list:
        time_stamp = re.sub(regex, '', filename)
        time_stamps.append(time_stamp)

    return time_stamps


def generate_gesture_data(path_to_files=None):
    performance_time_stamps = get_performance_time_stamps()
    gesture_data = []

    for time_stamp in performance_time_stamps:
        gesture_data += condense_data(time_stamp=time_stamp, path_to_files=path_to_files)

    return gesture_data
