import logging
import numpy
import os
import string
import time

from Myo.hmmlearn import hmm
filename = "hmm_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")

def train(x_train, x_test, y_train, y_test):

    states = list(string.asciilowercase)
    n_components = len(states)

    max_accuracy = 0
    algorithm = None
    best_combo = None

    numpy.random.seed(42)

    number_of_states = None

    gaussian = hmm.GaussianHMM(n_components=number_of_states)
    gaussian.fit(list(x_train), list(y_train))
    gaussian_accuracy = gaussian.score(list(x_test), list(y_test))

    if gaussian_accuracy > max_accuracy:
        max_accuracy = gaussian_accuracy
        algorithm = "Gaussian"

    gmm = hmm.GMMHMM(n_components=number_of_states)
    gmm.fit(list(x_train), list(y_train))
    gmm_accuracy = gmm.score(list(x_test), list(y_test))

    if gmm_accuracy > max_accuracy:
        max_accuracy = gmm_accuracy
        algorithm = "GMM"

    mn = hmm.MultinomialHMM(n_components=number_of_states)
    mn.fit(list(x_train), list(y_train))
    mn_accuracy = gmm.score(list(x_test), list(y_test))

    if mn > max_accuracy:
        max_accuracy = mn_accuracy
        algorithm = "Multinomial"

    return max_accuracy, algorithm, best_combo
