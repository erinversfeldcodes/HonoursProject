import csv
import glob
import numpy as np
import os
import re
from seqlearn.datasets import load_conll

merged_folder = os.path.abspath('data/merged')
conll_folder = os.path.abspath('data/conll')


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
        time_stamp = re.sub(regex, '', filename)[-10:]
        time_stamps.add(time_stamp)

    return list(time_stamps)


def get_imu_data_files(folders, test_user=None, fp_flag=False):
    if type(folders) != list:
        folders = [folders]
    if fp_flag:
        if test_user:
            regex_prefix = str(test_user) + '-*'
        else:
            regex_prefix = ''
    else:
        regex_prefix = ''
    accelerometer_files, gyro_files, orientation_files, orientation_euler_files = [], [], [], []
    for folder in folders:
        folder = os.path.abspath(folder)
        acc_regex = os.path.join(folder, regex_prefix + "*-accelerometer-*.csv")
        accelerometer_files += glob.glob(acc_regex)
        gyro_regex = os.path.join(folder, regex_prefix + "*-gyro-*.csv")
        gyro_files += glob.glob(gyro_regex)
        orientation_regex = os.path.join(folder, regex_prefix + "*-orientation-*.csv")
        orientation_files += glob.glob(orientation_regex)
        orientation_euler_regex = os.path.join(folder, regex_prefix + "*-orientationEuler-*.csv")
        orientation_euler_files += glob.glob(orientation_euler_regex)

    return accelerometer_files, gyro_files, orientation_files, orientation_euler_files


def get_emg_data_files(folders, test_user=None, fp_flag=False):
    if type(folders) != list:
        folders = [folders]
    file_paths = []
    if fp_flag:
        if test_user:
            regex_prefix = str(test_user) + '-*'
        else:
            regex_prefix = ''
    else:
        regex_prefix = ''
    base_regex = regex_prefix + "*-emg-*.csv"
    for folder in folders:
        regex = os.path.join(folder, base_regex)
        files = glob.glob(regex)
        file_paths += files

    return file_paths


def get_emg_and_imu_data_files(imu_folders, emg_folders, test_user=None):
    if type(imu_folders) != list:
        imu_folders = [imu_folders]
    if type(emg_folders) != list:
        emg_folders = [emg_folders]
    imu_time_stamps = []
    for folder in imu_folders:
        time_stamps = get_performance_time_stamps(path_to_files=folder)
        imu_time_stamps += time_stamps
    emg_time_stamps = []
    for folder in emg_folders:
        time_stamps = get_performance_time_stamps(path_to_files=folder)
        emg_time_stamps += time_stamps

    emg_files = get_emg_data_files(emg_folders, test_user=test_user)
    time_stamps_to_remove = []
    for time_stamp in emg_time_stamps:
        if time_stamp not in imu_time_stamps:
            time_stamps_to_remove.append(time_stamp)

    files_to_remove = []
    for i in range(len(emg_files)):
        file = emg_files[i]
        file_name = os.path.basename(file)
        file_time_stamp = file_name[-14:-4]
        if file_time_stamp in time_stamps_to_remove:
            files_to_remove.append(file)

    for file in files_to_remove:
        emg_files.remove(file)
    accelerometer_files, gyro_files, orientation_files, orientation_euler_files = get_imu_data_files(imu_folders, test_user=test_user)

    return accelerometer_files, gyro_files, orientation_files, orientation_euler_files, emg_files


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


def write_csv(title, max_num_lines, contents):
    row_num = 0
    with open(title, 'w+', newline='') as output:
        for i in range(0, max_num_lines):
            line = contents[i]
            writer = csv.writer(output)
            writer.writerow(line)
            if i % 4 == 0:
                row_num += 1


def merge_imu_files(acc_file, g, o, oe, letter, max_num_lines=2):
    file_basename = os.path.basename(acc_file)
    timestamp = file_basename[-14:-4]
    title = letter + ' imu ' + timestamp + '.csv'
    title_path = os.path.join(merged_folder, title)
    sufficient_data = True

    # if title in os.listdir(merged_folder):
    #     return title_path
    # else:
    a = read_csv(acc_file, max_num_lines)
    g = read_csv(g, max_num_lines)
    o = read_csv(o, max_num_lines)
    oe = read_csv(oe, max_num_lines)

    contents = []
    for i in range(max_num_lines):
        try:
            line = a[i] + g[i] + o[i] + oe[i]
            contents.append(line)
        except IndexError:
            sufficient_data = False
            break

    if sufficient_data and contents:
        write_csv(title_path, 2, contents)

        return title_path
    else:
        return False


def combine_emg_and_imu(merged_imu_data_file, emg_data_file):
    sufficient_data = True
    imu_file_name = str(merged_imu_data_file)[:-4]
    title_path = imu_file_name.replace('imu', '') + ' emg and imu.csv'
    imu_rows = read_csv(merged_imu_data_file, 2)
    try:
        emg_rows = read_csv(emg_data_file, 2)
    except FileNotFoundError:
        print('Couldn\'t find corresponding emg file for timestamp: ' + emg_data_file)
        return False

    contents = []
    for i in range(2):
        try:
            line = imu_rows[i] + emg_rows[i]
            contents.append(line)
        except IndexError:
            sufficient_data = False
            break

    if sufficient_data and contents:
        write_csv(title_path, 2, contents)

        return title_path
    else:
        return False


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


def check_file_not_empty(file):
    with open(file) as f:
        contents = f.read()
        lines = contents.split("\n")
        lines.remove("")

        if len(lines) > 1:
            return True

        return False


def contains_nans(data):
    nan_values = {'[]', 'nan'}
    for row in range(len(data)):
        for column in range(len(data[row])):
            column_entry = data[row][column]

            if column_entry in nan_values or np.isnan(column_entry) is True:
                return True

    return False


def remove_nans(data, delete=True):
    nan_values = {'[]', 'nan'}
    cleaned_data = data
    cleaned_data.flags.writeable = True
    for row in range(len(data)):
        for column in range(len(data[row])):
            column_entry = data[row][column]
            if type(column_entry) == np.ndarray:
                break
            elif column_entry in nan_values or np.isnan(column_entry) is True:
                if delete is True:
                    cleaned_data = data.delete(data[row])
                else:
                    cleaned_data[row][column] = 0

    return cleaned_data


def write_conll_file(file_name, data, data_labels, preproc=False, feat_extr=False, sensor="both"):
    if preproc is True:
        if feat_extr is True:
            if sensor == "both":
                path_to_feat_extr_preproc = os.path.join(conll_folder, "feature_extracted_preprocessed")
                path = os.path.join(path_to_feat_extr_preproc, "emg_and_imu")
            elif sensor == "emg":
                path_to_feat_extr_preproc = os.path.join(conll_folder, "feature_extracted_preprocessed")
                path = os.path.join(path_to_feat_extr_preproc, "emg")
            else:
                path_to_feat_extr_preproc = os.path.join(conll_folder, "feature_extracted_preprocessed")
                path = os.path.join(path_to_feat_extr_preproc, "imu")
        else:
            if sensor == "both":
                path_to_preproc = os.path.join(conll_folder, "preprocessed")
                path = os.path.join(path_to_preproc, "emg_and_imu")
            elif sensor == "emg":
                path_to_preproc = os.path.join(conll_folder, "preprocessed")
                path = os.path.join(path_to_preproc, "emg")
            else:
                path_to_preproc = os.path.join(conll_folder, "preprocessed")
                path = os.path.join(path_to_preproc, "imu")
    elif feat_extr is True:
        if sensor == "both":
            path_to_feat_extr = os.path.join(conll_folder, "feature_extracted")
            path = os.path.join(path_to_feat_extr, "emg_and_imu")
        elif sensor == "emg":
            path_to_feat_extr = os.path.join(conll_folder, "feature_extracted")
            path = os.path.join(path_to_feat_extr, "emg")
        else:
            path_to_feat_extr = os.path.join(conll_folder, "feature_extracted")
            path = os.path.join(path_to_feat_extr, "imu")
    else:
        path = conll_folder


    path_to_conll_file = os.path.join(path, file_name)
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


def extract_features(sequence, i):
    yield sequence[i]


def remove_test_user_files(files, test_user, fp_flag):
    less_test_user = []

    for file in files:
        if fp_flag:
            test_user_regex = str(test_user) + '-'
            file_name = os.path.basename(file)
            file_user = file_name[:4]
            if test_user_regex in file_user:
                pass
            else:
                less_test_user.append(file)
        else:
            test_user_regex = 'Participant ' + str(test_user)
            if test_user_regex in file:
                pass
            else:
                less_test_user.append(file)

    return less_test_user

