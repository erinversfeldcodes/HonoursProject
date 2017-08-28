from Myo.data_processing.processing import *
from Myo.data_processing.utils import *
from Myo.ensemble_classifiers.voting import *
import Myo.k_nearest_neighbour.k_nearest_neighbour as nearest_neighbour
import Myo.artificial_neural_networks.artificial_neural_network as neural_network
import Myo.discriminant_analysis.linear_discriminant_analysis as linear_discriminant_analysis
import Myo.hidden_markov_models.hidden_markov_model as hmm

import logging
import os
from sklearn.model_selection import train_test_split
import time

filename = "init_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def set_up():
    emg_data = read_emg_data()
    emg_x_train, emg_x_test, emg_y_train, emg_y_test = train_test_split(emg_data[0], emg_data[1])
    hmm.train(emg_x_train, emg_x_test, emg_y_train, emg_y_test)
    # imu_data = read_imu_data()
    # emg_and_imu_data = read_emg_and_imu()

    # TODO: accomodate for 2+ classifiers producing the same value
    print("=========================================================================================")
    # find the best classifier of imu data
    msg = str(time.time()) + ": Find best IMU classifier"
    print(msg)
    logging.info(msg)
    best_imu_classifier, imu_accuracy, best_imu_classifier_params, best_imu_classifier_obj = find_best_classifier(imu_data)
    # find_best_classifier(imu_data)
    # best_imu_classifier = 'none'
    # imu_accuracy = 'none'
    # best_imu_classifier_params = 'none'
    # best_imu_classifier_obj = 'none'
    msg = str(time.time()) + ": The best IMU classifier was a " + str(best_imu_classifier) + " with parameters " + str(best_imu_classifier_params) + " which produced an accuracy score of " + str(imu_accuracy)
    print(msg)
    logging.info(msg)
    best_classifier = ('IMU data only', best_imu_classifier, imu_accuracy, best_imu_classifier_params)
    print("=========================================================================================")

    # find the best classifier of emg data
    msg = str(time.time()) + ": Find best EMG classifier"
    print(msg)
    logging.info(msg)
    best_emg_classifier, emg_accuracy, best_emg_classifier_params, best_emg_classifier_obj = find_best_classifier(emg_data)
    # find_best_classifier(emg_data)
    # best_emg_classifier = 'none'
    # emg_accuracy = 'none'
    # best_emg_classifier_params = 'none'
    # best_emg_classifier_obj = 'none'
    msg = str(time.time()) + ": The best EMG classifier was a " + str(best_emg_classifier) + " with parameters " + str(best_emg_classifier_params) + " which produced an accuracy score of " + str(emg_accuracy)
    print(msg)
    logging.info(msg)
    if emg_accuracy > best_classifier[2]:
        best_classifier = ('EMG data only', best_emg_classifier, emg_accuracy, best_emg_classifier_params)
    print("=========================================================================================")

    # find the best classifier for the combination of the emg and imu data
    msg = str(time.time()) + ": Find best combined data classifier"
    print(msg)
    logging.info(msg)
    best_combo_classifier, combo_accuracy, best_combo_classifier_params, best_combo_classifier_obj = find_best_classifier(emg_and_imu_data, combined=True)
    # find_best_classifier(emg_and_imu_data)
    # best_combo_classifier = 'none'
    # combo_accuracy = 'none'
    # best_combo_classifier_params = 'none'
    # best_combo_classifier_obj = 'none'
    msg = str(time.time()) + ": The best combined data classifier was a " + str(best_combo_classifier) + " with parameters " + str(best_combo_classifier_params) + " which produced an accuracy score of " + str(combo_accuracy)
    print(msg)
    logging.info(msg)
    if combo_accuracy > best_classifier[2]:
        best_classifier = ('IMU and EMG data', best_combo_classifier, combo_accuracy, best_combo_classifier_params)
    print("=========================================================================================")

    # find the best ensemble method
    # TODO: add ensemble for data combo and emg, and data combo and imu
    msg = str(time.time()) + ': Find best combination of classifiers for ensemble'
    print(msg)
    logging.info(msg)
    ensemble_accuracy = voting_ensemble_classifier(best_imu_classifier_obj, best_emg_classifier_obj)
    msg = str(time.time()) + ': Best ensemble produced an accuracy score of ' + str(ensemble_accuracy)
    print(msg)
    logging.info(msg)
    print("=========================================================================================")

    if ensemble_accuracy > best_classifier[2]:
        msg = str(time.time()) + ': An ensemble of ' + str(best_imu_classifier) + ' trained only on IMU data with params ' + str(best_imu_classifier_params) + ' and a ' + str(best_emg_classifier) + ' trained only on EMG data with params ' + str(best_emg_classifier_params) + ' performed best and produced an accuracy score of ' + str(ensemble_accuracy) + '.'
        print(msg)
        logging.info(msg)

    else:
        msg = str(time.time()) + ': A ' + str(best_classifier[1]) + ' trained on ' + str(best_classifier[0]) + ' with params ' + str(best_classifier[3]) + ' performed best and produced an accuracy score of ' + str(best_classifier[2])
        print(msg)
        logging.info(msg)
    print("=========================================================================================")


def find_best_classifier(data, combined=False):

    if combined:
        X = data[0]
        X = np.array(X)
        nsamples, nx, ny = X.shape
        X = X.reshape((nsamples, nx*ny))

        Y = data[1]
        Y = np.array(Y)
        nsamples, _ = Y.shape
        Y = Y.reshape((nsamples,))

    else:
        X = data[0]
        Y = data[1]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

    ann = neural_network.train(x_train, x_test, y_train, y_test)
    knn = nearest_neighbour.train(x_train, x_test, y_train, y_test)
    lda = linear_discriminant_analysis.train(x_train, x_test, y_train, y_test)

    best_classifier = ann.get('Classifier type')  # it doesn't really matter what we initialise these values to, but this saves a check
    max_accuracy = ann.get('Accuracy')
    classifier_params = ann.get('Params')
    classifier_obj = ann.get('Classifier obj')

    if knn.get('Accuracy') > max_accuracy:
        best_classifier = knn.get('Classifier type')
        max_accuracy = knn.get('Accuracy')
        classifier_params = knn.get('Params')
        classifier_obj = knn.get('Classifier obj')

    if lda.get('Accuracy') > max_accuracy:
        best_classifier = lda.get('Classifier type')
        max_accuracy = lda.get('Accuracy')
        classifier_params = lda.get('Params')
        classifier_obj = lda.get('Classifier obj')

    # if hmm.get('Accuracy') > max_accuracy:
    # best_classifier = lda.get('Classifier type')
    # max_accuracy = lda.get('Accuracy')
    # classifier_params = lda.get('Params')
    # classifier_obj = lda.get('Classifier obj')

    return best_classifier, max_accuracy, classifier_params, classifier_obj

if __name__ == "__main__":
    set_up()
