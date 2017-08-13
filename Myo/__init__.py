from Myo.data_processing.pre_processing import *
from Myo.data_processing.processing import *
from Myo.data_processing.utils import *
import k_nearest_neighbour.k_nearest_neighbour as knn
import artificial_neural_networks.artificial_neural_network as ann
# import hidden_markov_models

import logging
import glob
import os
from sklearn.model_selection import train_test_split
import time


filename = "init_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def set_up():
    # path_to_gesture_order = os.path.abspath("data/small_set/gesture_orders/")
    # gesture_order = generate_order_of_gestures(path_to_files=path_to_gesture_order, total_participants=1, total_rounds=1)
    gesture_order = generate_order_of_gestures(total_participants=1)
    logging.info(str(time.time()) + "Generated order of gestures: " + str(gesture_order))

    # path_to_data_files = os.path.abspath("data/small_set/myo_data/")
    path_to_data_files = os.path.abspath("data/myo_data/")
    # time_stamps = get_performance_time_stamps(path_to_files=path_to_data_files)
    time_stamps = get_performance_time_stamps()

    undo_renaming(path=path_to_data_files)
    rename_data_files(time_stamps, gesture_order, path_to_data_files)

    # the spatial data
    acc_regex = os.path.join(path_to_data_files, "*-accelerometer-*.csv")
    accelerometer_files = glob.glob(acc_regex)
    acc_data = None

    gyro_regex = os.path.join(path_to_data_files, "*-gyro-*.csv")
    gyro_files = glob.glob(gyro_regex)
    gyro_data = None

    orientation_regex = os.path.join(path_to_data_files, "*-orientation-*.csv")
    orientation_files = glob.glob(orientation_regex)
    orientation_data = None

    orientation_euler_regex = os.path.join(path_to_data_files, "*-orientationEuler-*.csv")
    orientation_euler_files = glob.glob(orientation_euler_regex)
    orientation_euler_data = None

    # the gestural data
    logging.info(str(time.time()) + "beginning to process and train with emg data.")
    emg_regex = os.path.join(path_to_data_files, "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)
    train_gestural_only(emg_files)

    return acc_data, gyro_data, orientation_data, orientation_euler_data


def train_ann(x_train, x_test, y_train, y_test):
    max_accuracy = 0
    # best_algorithm = None
    best_combo = None

    # for i in range(10, 100):
    #     print(str(i) + " of 100.")

    ann_accuracy, combo = ann.train(list(x_train), list(x_test), list(y_train), list(y_test))

    if ann_accuracy > max_accuracy:
        max_accuracy = ann_accuracy
        # best_algorithm = algorithm
        best_combo = combo

    logging.info(str(time.time()) + ": ANN accuracy: " + str(max_accuracy) + ", with combination: " + str(best_combo))
    return max_accuracy, best_combo


def train_knn(x_train, x_test, y_train, y_test):
    max_accuracy = 0
    best_combo = None

    knn_accuracy, combo = knn.train(list(x_train), list(x_test), list(y_train), list(y_test))

    if knn_accuracy > max_accuracy:
        max_accuracy = knn_accuracy
        best_combo = combo

    logging.info(str(time.time()) + ": KNN accuracy: " + str(max_accuracy) + ", with combination: " + str(best_combo))
    return max_accuracy, best_combo


def train_gestural_only(emg_files):

    max_accuracy = 0
    best_algorithm = None

    emg_data = read_emg_data(emg_files, step=80)
    X = emg_data[0]
    Y = emg_data[1]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0)

    # ann_results = train_ann(x_train, x_test, y_train, y_test)
    #
    # if ann_results[0] > max_accuracy:
    #     max_accuracy = ann_results[0]
    #     best_algorithm = ("ANN", ann_results[1])

    knn_results = train_knn(x_train, x_test, y_train, y_test)

    if knn_results[0] > max_accuracy:
        max_accuracy = knn_results[0]
        best_algorithm = ("KNN", knn_results[1])

    # hmm_results = train_hmm(emg_files)

    logging.info(str(time.time()) + ": Best performance was: " + str(max_accuracy) + " from: " + str(best_algorithm))


def train_spatial_only(acc_data, gyro_data, orientation_data, orientation_euler_data):
    pass


if __name__ == "__main__":
    set_up()
