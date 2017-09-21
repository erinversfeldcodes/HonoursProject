from artificial_neural_networks.artificial_neural_network import best_ann
from ensemble_classifiers.voting import *
import hidden_markov_models.hidden_markov_model as hidden_markov_model
from k_nearest_neighbour.k_nearest_neighbour import best_knn
from data_processing.processing import *
from model_statistics.utils import generate_statistics

import itertools
import logging
import numpy as np
from multiprocessing import Manager, Process
import os
from operator import itemgetter
import random
import seqlearn
import time
import winsound

filename = "init_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def find_best_classifier(sensor_data="both", test_user=None, fp_flag=False):
    msg = str(time.time()) + ": Finding best " + sensor_data + " data classifier"
    print(msg)
    logging.info(msg)
    print("----------------------------------------------------")
    logging.info("----------------------------------------------------")
    x_train, x_test, y_train, y_test = get_data(test_user=test_user, fp_flag=fp_flag, sensor_data=sensor_data)
    if fp_flag:
        x_train = remove_nans(x_train, delete=False)
        x_test = remove_nans(x_test, delete=False)

    manager = Manager()
    return_values = manager.list([None, None, None])
    ann_thread = Process(target=best_ann, args=(x_train, x_test, y_train, y_test, sensor_data, return_values,))
    ann_thread.start()
    knn_thread = Process(target=best_knn, args=(x_train, x_test, y_train, y_test, sensor_data, return_values))
    knn_thread.start()
    x_train, x_test, y_train, y_test, train_lengths, test_lengths = get_data_conll(sensor_data=sensor_data,
                                                                                   test_user=test_user, fp_flag=fp_flag)
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

    return sorted_list


def find_best_ensemble(best_emg, best_imu, best_emg_and_imu, test_user=None, fp_flag=False):
    # TODO: Adapt for sensor specific experimentation
    msg = str(time.time()) + ": Finding best ensemble method"
    print(msg)
    logging.info(msg)
    print("-------------------------------------------")
    logging.info("-------------------------------------------")

    x_train, x_test, y_train, y_test = get_data(sensor_data="both", test_user=test_user, fp_flag=fp_flag)

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
                                             fp_flag=fp_flag)

    return best_ensemble


def compare_sensors(test_user=None, fp_flag=False):
    msg = str(time.time()) + ": Experimenting with sensors"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------")
    logging.info("---------------------------------------------------")

    # emg_classifiers = find_best_classifier(sensor_data="emg", test_user=test_user, fp_flag=fp_flag)
    # imu_classifiers = find_best_classifier(sensor_data="imu", test_user=test_user, fp_flag=fp_flag)
    emg_and_imu_classifiers = find_best_classifier(sensor_data="both", test_user=test_user, fp_flag=fp_flag)
    # best_emg = emg_classifiers[-1]
    # best_imu = imu_classifiers[-1]
    best_emg_and_imu = emg_and_imu_classifiers[-1]

    # best_ensemble = find_best_ensemble(best_emg, best_imu, best_emg_and_imu)

    # generate_statistics(best_emg, best_imu, best_emg_and_imu)  #, best_ensemble[-1])
    generate_statistics(best_emg_and_imu)
    # result = "The best EMG classifier is " + str(best_emg.get('Classifier type')) + ", the best IMU classifier is " + \
    #          str(best_imu.get('Classifier type')) + ", the best classifier for IMU and EMG is " + \
    #          str(best_emg_and_imu.get('Classifier type'))# + ", and the best ensemble is for " + \
             # str(best_ensemble.get('Classifier type'))
    result = "Winning"

    return result


def with_preprocessing(test_user=None):
    result = compare_sensors(fp_flag='p', test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def with_feature_extraction(test_user=None):
    result = compare_sensors(fp_flag='f', test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def with_preprocessing_and_feature_extraction(test_user=None):
    result = compare_sensors(fp_flag='fp', test_user=test_user)
    msg = str(time.time()) + ": Experiment result is: " + str(result)
    print(msg)
    logging.info(msg)


def user_dependent_experiments(test_user):

    msg = str(time.time()) + ": Experimenting with preprocessing and feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_preprocessing_and_feature_extraction(test_user=test_user)

    # msg = str(time.time()) + ": Experimenting without preprocessing or feature extraction"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # compare_sensors(test_user=test_user)
    #
    # msg = str(time.time()) + ": Experimenting with preprocessing only"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # with_preprocessing(test_user=test_user)

    # msg = str(time.time()) + ": Experimenting with feature extraction only"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # with_feature_extraction(test_user=test_user)


def user_independent_experiments():

    msg = str(time.time()) + ": Experimenting with preprocessing and feature extraction"
    print(msg)
    logging.info(msg)
    print("---------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------")
    with_preprocessing_and_feature_extraction()

    # msg = str(time.time()) + ": Experimenting without preprocessing or feature extraction"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # compare_sensors()
    # msg = str(time.time()) + ": Experimenting with preprocessing only"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # with_preprocessing()

    # msg = str(time.time()) + ": Experimenting with feature extraction only"
    # print(msg)
    # logging.info(msg)
    # print("---------------------------------------------------------------------------------------")
    # logging.info("---------------------------------------------------------------------------------------")
    # with_feature_extraction()


def run_experiments():
    # test_users = [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
    #               37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48]
    # user_number = test_users[random.randint(0, len(test_users)-1)]
    user_number = 22
    msg = str(time.time()) + ": User dependent experiments with Participant " + str(user_number) + " as test user"
    print(msg)
    logging.info(msg)
    print("=============================================================================")
    logging.info("=============================================================================")
    user_dependent_experiments(test_user=user_number)
    #
    # msg = str(time.time()) + ": User independent experiments"
    # print(msg)
    # logging.info(msg)
    # print("=============================")
    # logging.info("=============================")
    # user_independent_experiments()


if __name__ == "__main__":
    try:
        run_experiments()
        winsound.Beep(1000, 250)
    except Exception as e:
        winsound.Beep(1000, 250)
        winsound.Beep(1000, 250)
        winsound.Beep(1000, 250)
        winsound.Beep(1000, 250)
        raise e
