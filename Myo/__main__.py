from Myo.artificial_neural_networks.artificial_neural_network import best_ann
from Myo.ensemble_classifiers.voting import *
import Myo.hidden_markov_models.hidden_markov_model as hidden_markov_model
from Myo.k_nearest_neighbour.k_nearest_neighbour import best_knn
from Myo.data_processing.processing import *
from Myo.statistics.utils import generate_statistics

import itertools
import logging
import numpy as np
from multiprocessing import Manager, Process
import os
from operator import itemgetter
import random
import seqlearn
import time
# import winsound

filename = "init_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def find_best_classifier(shared_list, index, sensor_data="both", test_user=None, preproc=False, feat_extr=False):
    msg = str(time.time()) + ": Finding best " + sensor_data + " data classifier"
    print(msg)
    logging.info(msg)
    print("----------------------------------------------------")
    logging.info("----------------------------------------------------")
    x_train, x_test, y_train, y_test = get_data(test_user=test_user, preproc=preproc,
                                                feat_extr=feat_extr, sensor_data=sensor_data)
    manager = Manager()
    return_values = manager.list([None, None, None])
    ann_thread = Process(target=best_ann, args=(x_train, x_test, y_train, y_test, sensor_data, return_values,))
    ann_thread.start()
    knn_thread = Process(target=best_knn, args=(x_train, x_test, y_train, y_test, sensor_data, return_values))
    knn_thread.start()
    x_train, x_test, y_train, y_test, train_lengths, test_lengths = get_data_conll(sensor_data=sensor_data,
                                                                                   test_user=test_user, preproc=preproc,
                                                                                   feat_extr=feat_extr)
    hmm_thread = Process(target=hidden_markov_model.train, args=(x_train, x_test, y_train, y_test, train_lengths,
                                                                 test_lengths, sensor_data, return_values,))
    hmm_thread.start()

    ann_thread.join()
    knn_thread.join()
    hmm_thread.join()

    sorted_list = list(sorted(return_values, key=itemgetter('Accuracy')))  # returns all three values in order of best to
    # worst
    ann_thread.terminate()
    knn_thread.terminate()
    hmm_thread.terminate()

    shared_list[index] = sorted_list


def find_best_ensemble(best_emg, best_imu, best_emg_and_imu, test_user=None, preproc=False, feat_extr=False):
    # TODO: Adapt for sensor specific experimentation
    msg = str(time.time()) + ": Finding best ensemble method"
    print(msg)
    logging.info(msg)
    print("-------------------------------------------")
    logging.info("-------------------------------------------")

    x_train, x_test, y_train, y_test = get_data(sensor_data="both", test_user=test_user, preproc=preproc,
                                                feat_extr=feat_extr)

    x_train, x_test = np.array(x_train), np.array(x_test)
    y_train, y_test = np.array(y_train), np.array(y_test)

    emg = best_emg[0].get('Classifier obj')  # mlxtend does not support classifiers which are constructed with more than
    # three parameters to be used in a voting ensemble, therefore we need to take the seccond best ones for their use
    if type(emg) == seqlearn.hmm.MultinomialHMM:
        emg = best_emg[1].get('Classifier obj')
    imu = best_emg[0].get('Classifier obj')
    if type(imu) == seqlearn.hmm.MultinomialHMM:
        imu = best_imu[1].get('Classifier obj')
    emg_and_imu = best_emg_and_imu[0].get('Classifier obj')
    if type(emg_and_imu) == seqlearn.hmm.MultinomialHMM:
        emg_and_imu = best_emg_and_imu[1].get('Classifier obj')

    best_ensemble = best_ensemble_classifier(emg, imu, emg_and_imu, x_train, x_test, y_train, y_test,
                                             feat_extr=feat_extr)

    return best_ensemble


def compare_sensors(test_user=None, preproc=False, feat_extr=False):
    msg = str(time.time()) + ": Experimenting with sensors"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------")
    logging.info("---------------------------------------------------")

    manager = Manager()
    return_values = manager.list([None, None, None])

    best_emg_thread = Process(target=find_best_classifier, args=(return_values, 0, "emg", test_user, preproc,
                                                                 feat_extr,))
    best_emg_thread.start()
    best_imu_thread = Process(target=find_best_classifier, args=(return_values, 1, "imu", test_user, preproc,
                                                                 feat_extr,))
    best_imu_thread.start()
    best_emg_and_imu_thread = Process(target=find_best_classifier, args=(return_values, 2, "both", test_user, preproc,
                                                                         feat_extr,))
    best_emg_and_imu_thread.start()

    best_emg_thread.join()
    best_imu_thread.join()
    best_emg_and_imu_thread.join()

    emg_classifiers = return_values[0]
    best_emg = emg_classifiers[-1]
    imu_classifiers = return_values[1]
    best_imu = imu_classifiers[-1]
    emg_and_imu_classifiers = return_values[2]
    best_emg_and_imu = emg_and_imu_classifiers[-1]

    best_ensemble = find_best_ensemble(best_emg, best_imu, best_emg_and_imu)

    generate_statistics(best_emg, best_imu, best_emg_and_imu, best_ensemble[-1])

    result = "The best EMG classifier is " + str(best_emg.get('Classifier type')) + ", the best IMU classifier is " + \
             str(best_imu.get('Classifier type')) + ", the best classifier for IMU and EMG is " + \
             str(best_emg_and_imu.get('Classifier type')) + ", and the best ensemble is for " + \
             str(best_ensemble.get('Classifier type'))

    return result


def with_preprocessing(test_user=None):
    pre_processing_options = ["mav", "median_filter", "normalise_data", "scale"]
    pre_processing_combinations = []

    for i in range(len(pre_processing_options) + 1):
        for combination in itertools.combinations(pre_processing_options, i):
            pre_processing_combinations.append(combination)

    print(pre_processing_combinations)

    result = compare_sensors(preproc=True, test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def with_feature_extraction(test_user=None):
    result = compare_sensors(feat_extr=True, test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def with_preprocessing_and_feature_extraction(test_user=None):
    pre_processing_options = ["mav", "median_filter", "normalise_data", "scale"]
    pre_processing_combinations = []

    for i in range(len(pre_processing_options) + 1):
        for combination in itertools.combinations(pre_processing_options, i):
            pre_processing_combinations.append(combination)

    result = compare_sensors(preproc=True, feat_extr=True, test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def user_dependent_experiments(test_user):

    msg = str(time.time()) + ": Experimenting with preprocessing and feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    Process(target=with_preprocessing_and_feature_extraction, args=test_user)

    msg = str(time.time()) + ": Experimenting without preprocessing or feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    Process(target=compare_sensors, args=test_user)

    msg = str(time.time()) + ": Experimenting with preprocessing only"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_preprocessing(test_user=test_user)

    msg = str(time.time()) + ": Experimenting with feature extraction only"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_feature_extraction(test_user=test_user)


def user_independent_experiments():

    msg = str(time.time()) + ": Experimenting with preprocessing and feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    Process(target=with_preprocessing_and_feature_extraction)

    msg = str(time.time()) + ": Experimenting without preprocessing or feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    Process(target=compare_sensors)
    msg = str(time.time()) + ": Experimenting with preprocessing only"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_preprocessing()

    msg = str(time.time()) + ": Experimenting with feature extraction only"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_feature_extraction()


def run_experiments():
    test_users = [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                  37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48]
    user_number = test_users[random.randint(0, len(test_users)-1)]
    msg = str(time.time()) + ": User dependent experiments with Participant " + str(user_number) + " as test user"
    print(msg)
    logging.info(msg)
    print("=============================================================================")
    logging.info("=============================================================================")
    Process(target=user_dependent_experiments, args=user_number)

    msg = str(time.time()) + ": User independent experiments"
    print(msg)
    logging.info(msg)
    print("=============================")
    logging.info("=============================")
    Process(target=user_independent_experiments)


if __name__ == "__main__":
    try:
        run_experiments()
        # winsound.Beep(1000, 250)
    except Exception as e:
        # winsound.Beep(1000, 250)
        # winsound.Beep(1000, 250)
        # winsound.Beep(1000, 250)
        # winsound.Beep(1000, 250)
        raise e
