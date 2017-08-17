from Myo.data_processing.processing import *
from Myo.data_processing.utils import *
from Myo.ensemble_classifiers.voting import *
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

    gyro_regex = os.path.join(path_to_data_files, "*-gyro-*.csv")
    gyro_files = glob.glob(gyro_regex)

    orientation_regex = os.path.join(path_to_data_files, "*-orientation-*.csv")
    orientation_files = glob.glob(orientation_regex)

    orientation_euler_regex = os.path.join(path_to_data_files, "*-orientationEuler-*.csv")
    orientation_euler_files = glob.glob(orientation_euler_regex)

    best_spatial_classifier, spatial_params, spatial_accuracy = train_spatial_only(accelerometer_files, gyro_files,
                                                                                   orientation_files,
                                                                                   orientation_euler_files)

    print("Best spatial classifier was: " + str(best_spatial_classifier) + ' with parameters ' + str(spatial_params) + ' achieving an accuracy of ' + str(spatial_accuracy))

    # the gestural data
    emg_regex = os.path.join(path_to_data_files, "*-emg-*.csv")
    emg_files = glob.glob(emg_regex)
    best_gestural_classifier, gestural_params, gestural_accuracy = train_gestural_only(emg_files)
    print("Best gestural classifier was: " + str(best_gestural_classifier) + ' with parameters ' + str(gestural_params) + ' achieving an accuracy of ' + str(spatial_accuracy))

    spatial_msg = 'Spatial classifier ' + str(best_spatial_classifier) + ' with params ' + str(
        spatial_params) + 'performed best with accuracy score of ' + str(spatial_accuracy)
    gestural_msg = 'Gestural classifier ' + str(best_gestural_classifier) + ' with params ' + str(
        gestural_params) + 'performed best with accuracy score of ' + str(gestural_accuracy)
    best_data_classifier_combo = spatial_msg if spatial_accuracy > gestural_accuracy else gestural_msg
    print(best_data_classifier_combo)

    ensemble = voting_ensemble_classifier(best_spatial_classifier, spatial_params, best_gestural_classifier,
                                          gestural_params)
    print("Ensemble accuracy: " + ensemble)


def train_ann(x_train, x_test, y_train, y_test):
    max_accuracy = 0
    best_algorithm = None
    best_combo = None

    # for i in range(10, 100):
    #     print(str(i) + " of 100.")

    ann_accuracy, algorithm, combo = ann.train(list(x_train), list(x_test), list(y_train), list(y_test))

    if ann_accuracy > max_accuracy:
        max_accuracy = ann_accuracy
        best_algorithm = algorithm
        best_combo = combo

    logging.info(str(time.time()) + ": ANN accuracy: " + str(max_accuracy) + ", with combination: " + str(best_combo))
    return max_accuracy, best_algorithm, best_combo


def train_knn(x_train, x_test, y_train, y_test):
    max_accuracy = 0
    best_algorithm = None
    best_combo = None

    knn_accuracy, algorithm, combo = knn.train(list(x_train), list(x_test), list(y_train), list(y_test))

    if knn_accuracy > max_accuracy:
        max_accuracy = knn_accuracy
        best_algorithm = algorithm
        best_combo = combo

    logging.info(str(time.time()) + ": KNN accuracy: " + str(max_accuracy) + ", with combination: " + str(best_combo))
    return max_accuracy, best_algorithm, best_combo


def train_gestural_only(emg_files):
    max_accuracy = 0
    best_algorithm = None
    best_params = None

    emg_data = read_emg_data(emg_files, step=80)
    X = emg_data[0]
    Y = emg_data[1]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0)

    ann_results = train_ann(x_train, x_test, y_train, y_test)
    knn_results = train_knn(x_train, x_test, y_train, y_test)

    if ann_results[0] > max_accuracy:
        max_accuracy = ann_results[0]
        best_algorithm = ann_results[1]
        best_params = ann_results[2]


    if knn_results[0] > max_accuracy:
        max_accuracy = knn_results[0]
        best_algorithm = knn_results[1]
        best_params = knn_results[2]

    # hmm_results = train_hmm(emg_files)

    logging.info(str(time.time()) + ": Best performance was: " + str(max_accuracy) + " from: " + str(best_algorithm))

    return best_algorithm, best_params, max_accuracy


def train_spatial_only(acc_files, gyro_files, orientation_files, orientation_euler_files):
    max_accuracy = 0
    best_algorithm = None
    best_params = None

    spatial_data = read_spatial_data(acc_files, gyro_files, orientation_files, orientation_euler_files, step=40)
    X = spatial_data[0]
    Y = spatial_data[1]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0)

    ann_results = train_ann(x_train, x_test, y_train, y_test)
    knn_results = train_knn(x_train, x_test, y_train, y_test)

    if ann_results[0] > max_accuracy:
        max_accuracy = ann_results[0]
        best_algorithm = ann_results[1]
        best_params = ann_results[2]

    if knn_results[0] > max_accuracy:
        max_accuracy = knn_results[0]
        best_algorithm = knn_results[1]
        best_params = knn_results[2]

    # hmm_results = train_hmm(emg_files)
    #     max_accuracy = knn_results[0]
    #     best_algorithm = knn_results[1]
    #     best_params = knn[2]

    logging.info(str(time.time()) + ": Best performance was: " + str(max_accuracy) + " from: " + str(best_algorithm))

    return best_algorithm, best_params, max_accuracy


if __name__ == "__main__":
    set_up()
