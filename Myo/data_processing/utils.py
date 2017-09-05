import csv
import glob
import os
import pandas as pd
import re

processed_folder = os.path.abspath('data\\processed_data')
reduced_folder = os.path.abspath('data\\reduced')


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


def get_imu_data_files(folders, emg=False):
    if type(folders) != list:
        folders = [folders]
    accelerometer_files, gyro_files, orientation_files, orientation_euler_files = [], [], [], []
    for folder in folders:
        folder = os.path.abspath(folder)
        acc_regex = os.path.join(folder, "*-accelerometer-*.csv")
        accelerometer_files += glob.glob(acc_regex)
        gyro_regex = os.path.join(folder, "*-gyro-*.csv")
        gyro_files += glob.glob(gyro_regex)
        orientation_regex = os.path.join(folder, "*-orientation-*.csv")
        orientation_files += glob.glob(orientation_regex)
        orientation_euler_regex = os.path.join(folder, "*-orientationEuler-*.csv")
        orientation_euler_files += glob.glob(orientation_euler_regex)

    if emg is True:
        emg_files = []
        for folder in folders:
            folder = os.path.abspath(folder)
            emg_regex = os.path.join(folder, "*-emg-*.csv")
            emg_files += glob.glob(emg_regex)
        return accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files

    return accelerometer_files, gyro_files, orientation_files, orientation_euler_files


def get_emg_data_files(folders):
    file_paths = []
    base_regex = "*-emg-*.csv"
    for folder in folders:
        regex = os.path.join(folder, base_regex)
        files = glob.glob(regex)
        file_paths += files

    return file_paths


def read_csv(file, max_num_lines):
    contents = []
    row_num = 0
    with open(file, newline='') as f:
        file_reader = csv.reader(f)
        for row in file_reader:
            if row_num < max_num_lines:
                contents.append(row)
            else:
                break

    return contents


def write_csv(title, max_num_lines, contents_1, contents_2=None):
    row_num = 0
    with open(title, 'w+', newline='') as output:
        for i in range(0, max_num_lines):
            if contents_2:
                line = contents_1[i] + contents_2[row_num][1:]
            else:
                line = contents_1[i] + contents_1[row_num][1:]
            writer = csv.writer(output)
            writer.writerow(line)
            if i % 4 == 0:
                row_num += 1


def merge_imu_files(a, g, o, oe):
    file_basename = os.path.basename(a)
    letter = file_basename[0]
    timestamp = file_basename[-14:-4]
    title = letter + ' ' + timestamp
    title_path = os.path.join(processed_folder, title)

    if title in os.listdir(processed_folder):
        pass
    else:
        a = pd.read_csv(a)
        g = pd.read_csv(g)
        o = pd.read_csv(o)
        oe = pd.read_csv(oe)

        merged_data_file = ((a.merge(g, on='timestamp')).merge(o, on='timestamp')).merge(oe, on='timestamp')
        merged_data_file.to_csv(title_path, index=False)

    return title_path


def combine_emg_and_imu(merged_imu_data_file, emg_data_file):
    output_title = str(merged_imu_data_file) + ' emg and imu.csv'
    imu_rows = []
    emg_rows = []

    with open(merged_imu_data_file) as imu_data_file:
        imu_reader = csv.reader(imu_data_file)
        for row in imu_reader:
            imu_rows.append(row)

    with open(emg_data_file) as emg_data_file:
        emg_reader = csv.reader(emg_data_file)
        for row in emg_reader:
            emg_rows.append(row)

    write_csv(output_title, contents_1=emg_rows, contents_2=imu_rows, max_num_lines=200)

    return output_title


def check_sufficient_data(file):
    with open(file) as f:
        contents = f.read()
        lines = contents.split("\n")
        try:
            lines.remove("")
        except ValueError:
            pass
        if "emg" in file:
            if len(lines) < 200:
                return False
        else:
            if len(lines) < 50:
                return False
    return True


def reduce_file(file, max_num_lines):
    contents = read_csv(file, max_num_lines)
    file_name = os.path.basename(file)
    output_title = os.path.join(reduced_folder, file_name)
    write_csv(output_title, contents_1=contents, max_num_lines=max_num_lines)

    return output_title
