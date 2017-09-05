from Myo.ensemble_classifiers.voting import *
import Myo.k_nearest_neighbour.k_nearest_neighbour as nearest_neighbour
import Myo.artificial_neural_networks.artificial_neural_network as neural_network
import Myo.discriminant_analysis.linear_discriminant_analysis as linear_discriminant_analysis
import Myo.hidden_markov_models.hidden_markov_model as hidden_markov_model

import logging
import os
import time

filename = "init_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def find_best_classifier(sensor_data="both", test_user=None, preproc=False, feat_extr=False):
    print("Finding best classifier")
    print("-----------------------------")
    x_train, x_test, y_train, y_test = get_data(sensor_data=sensor_data, test_user=test_user, preproc=preproc,
                                                feat_extr=feat_extr)
    ann = neural_network.train(x_train, x_test, y_train, y_test)
    # knn = nearest_neighbour.train(x_train, x_test, y_train, y_test)
    # lda = linear_discriminant_analysis.train(x_train, x_test, y_train, y_test)
    # x_train, x_test, y_train, y_test, lengths = get_data_conll(sensor_data=sensor_data, test_user=test_user,
    #                                                            preproc=preproc, feat_extr=feat_extr)
    # hmm = hidden_markov_model.train(x_train, x_test, y_train, y_test, lengths)

    # max_accuracy = ann.get("Accuracy")
    classifier_vals = ann

    # if knn.get('Accuracy') > max_accuracy:
    #     max_accuracy = knn.get('Accuracy')
    #     classifier_vals = knn

    # if lda.get('Accuracy') > max_accuracy:
    #     max_accuracy = lda.get('Accuracy')
    #     classifier_vals = lda

    # if hmm.get('Accuracy') > max_accuracy:
    #    return hmm

    return classifier_vals


def find_best_ensemble(best_emg, best_imu, best_emg_and_imu, test_user=None, preproc=False, feat_extr=False):
    print("Finding best ensemble method")
    print("-----------------------------")
    best = None
    max_accuracy = 0

    x_train, x_test, y_train, y_test = get_data(sensor_data="both", test_user=test_user, preproc=preproc,
                                                feat_extr=feat_extr)

    x_train, x_test = np.array(x_train), np.array(x_test)
    y_train, y_test = np.array(y_train), np.array(y_test)

    emg_imu = voting_ensemble_classifier(best_emg, best_imu, x_train, x_test, y_train, y_test, feat_extr=feat_extr)
    # emg_emg_and_imu = voting_ensemble_classifier(best_emg, best_emg_and_imu)
    # imu_emg_and_imu = voting_ensemble_classifier(best_imu, best_emg_and_imu)

    if emg_imu > max_accuracy:
        best = "EMG and IMU ensemble"
        max_accuracy = emg_imu

    # if emg_emg_and_imu > max_accuracy:
    #     best = "EMG and EMG-IMU ensemble"
    #     max_accuracy = emg_emg_and_imu

    # if imu_emg_and_imu > max_accuracy:
    #     best = "IMU and EMG-IMU ensemble"
    #     max_accuracy = emg_emg_and_imu

    return {"Classifier": best, "Accuracy": max_accuracy}


def compare_sensors(test_user=None, preproc=False, feat_extr=False):
    print("Experimenting with sensors")
    print("---------------------------")
    best_emg = find_best_classifier(sensor_data="emg", test_user=test_user, preproc=preproc, feat_extr=feat_extr)
    best_imu = find_best_classifier(sensor_data="imu", test_user=test_user, preproc=preproc, feat_extr=feat_extr)
    best_emg_and_imu = find_best_classifier(sensor_data="both", test_user=test_user, preproc=preproc,
                                            feat_extr=feat_extr)
    best_ensemble = find_best_ensemble(best_emg.get("Classifier obj"), best_imu.get("Classifier obj"),
                                       best_emg_and_imu.get("Classifier obj"))

    result = "The best EMG classifier is " + str(best_emg) + ", the best IMU classifier is " + str(best_imu) + "and the best ensemble is for " + str(best_ensemble)
             # ", the best classifier for IMU and EMG is " + str(best_emg_and_imu) + ", and the best ensemble is for " +\
             # str(best_ensemble)

    return result


def with_preprocessing(test_user=None):
    result = compare_sensors(preproc=True, test_user=test_user)
    print("Experiment result is: " + str(result))


def with_feature_extraction(test_user=None):
    result = compare_sensors(feat_extr=True, test_user=test_user)
    print("Experiment result is: " + str(result))


def with_preprocessing_and_feature_extraction(test_user=None):
    result = compare_sensors(preproc=True, feat_extr=True, test_user=test_user)
    print("Experiment result is: " + str(result))


def user_dependent_experiments():
    # test_user = random.randint(0, 51)
    test_user = 14
    # print("Experimenting with preprocessing only")
    # print("-------------------------------------")
    # with_preprocessing(test_user=test_user)
    # print("Experimenting with feature extraction only")
    # print("-------------------------------------")
    # with_feature_extraction(test_user=test_user)
    print("Experimenting with preprocessing and feature extraction")
    print("-------------------------------------")
    with_preprocessing_and_feature_extraction(test_user=test_user)


def user_independent_experiments():
    print("Experimenting with preprocessing only")
    print("-------------------------------------")
    with_preprocessing()
    print("Experimenting with feature extraction only")
    print("-------------------------------------")
    with_feature_extraction()
    print("Experimenting with preprocessing and feature extraction")
    print("-------------------------------------")
    with_preprocessing_and_feature_extraction()


def run_experiments():
    print("User dependent experiments")
    print("===========================")
    user_dependent_experiments()
    print("User independent experiments")
    print("===========================")
    user_independent_experiments()


if __name__ == "__main__":
    run_experiments()
