import logging
import os
import re
import time

filename = "pre_processing.log"
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info(str(time.time()) + ": Loaded pre_processing.py")


def undo_renaming(path=None):
    if path:
        path_to_data = path
    else:
        path_to_data = os.path.abspath("data\\myo_data")

    for file in os.listdir(path_to_data):
        filename = os.path.basename(file)
        if filename[1] == "-":
            original_filename = os.path.join(path_to_data, file)
            new_filename = os.path.join(path_to_data, filename[2:])
            os.rename(original_filename, new_filename)


def generate_order_of_gestures(path_to_files=None, total_participants=50, total_rounds=26):
    # construct ordered list of gestures
    gestures = []
    for participant_number in range(0, total_participants):
        for round_number in range(0, total_rounds):
            filename = str(participant_number) + "-" + str(round_number) + ".txt"
            if path_to_files:
                path_to_file = os.path.join(path_to_files, filename)
                with open(path_to_file) as data_file:
                    file_contents = data_file.read()
                    gestures += file_contents.split(',')
                    gestures[:] = [gesture for gesture in gestures if gesture != '']
            else:
                path = os.path.abspath("data/gesture_orders/")
                path_to_file = os.path.join(path, filename)
                with open(path_to_file) as data_file:
                    file_contents = data_file.read()
                    gestures += file_contents.split(',')
                    gestures[:] = [gesture for gesture in gestures if gesture != '']

    return gestures


def rename_data_file(time_stamp, gesture, data_type, path_to_file=None): # TODO: Come back and fix this function, then retest
    original_data_filename = data_type + "-" + str(time_stamp) + ".csv"
    new_filename = str(gesture) + "-" + str(original_data_filename)

    if path_to_file:
        path = path_to_file
    else:
        path = os.path.abspath("data/myo_data/")

    original_path = os.path.join(path, original_data_filename)
    new_path = os.path.join(path, new_filename)
    #
    os.rename(original_path, new_path)

    return new_filename


def rename_data_files(time_stamps, order_of_gestures, path_to_file=None):
    new_filenames = []

    for i in range(0, len(time_stamps)):
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


def get_performance_time_stamps(path_to_files=None):
    time_stamps = set()

    if path_to_files:
        data_files_list = os.listdir(path_to_files)
    else:
        path = os.path.abspath("data\\myo_data\\")
        data_files_list = os.listdir(path)
    regex = '[.*abcdefghijklmnopqrstuvwxyzE-]+'

    for filename in data_files_list:
        time_stamp = re.sub(regex, '', filename)
        time_stamps.add(time_stamp)

    return list(time_stamps)

