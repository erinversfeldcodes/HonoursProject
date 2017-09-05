from Myo.data_processing.processing import *

import logging
import os
import sklearn.neural_network as neural_network
import time

filename = "ann_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info(str(time.time()) + " Loaded ann.py")


def train(x_train, x_test, y_train, y_test):
    msg = str(time.time()) + ": Experimenting with ANNs"
    print(msg)
    logging.info(msg)

    activation_options = {'identity', 'logistic', 'tanh', 'relu'}
    solver_options = {'lbfgs', 'sgd', 'adam'}
    learning_rate_options = {'constant', 'invscaling', 'adaptive'}

    max_accuracy = 0
    best_params = None
    classifier = "MLP"
    classifier_obj = None
    alpha_options = [x / 1000.0 for x in range(10, 11)]  # 000)]

    for activation in activation_options:
        for solver in solver_options:
            for learning_rate in learning_rate_options:
                for hidden_layer_sizes in range(1, 2):  # 110):
                    for alpha in alpha_options:

                        # create, train, score
                        multilayer_perceptron = neural_network.MLPClassifier(hidden_layer_sizes=(hidden_layer_sizes,),
                                                                             activation=activation, solver=solver,
                                                                             alpha=alpha, learning_rate=learning_rate,
                                                                             early_stopping=True)
                        multilayer_perceptron.fit(list(x_train), list(y_train))
                        mlp_accuracy = multilayer_perceptron.score(list(x_test), list(y_test))

                        # establish if there was an improvement, and document if necessary
                        if mlp_accuracy > max_accuracy:
                            max_accuracy = mlp_accuracy
                            best_params = {"Layer sizes": hidden_layer_sizes, "Activation": activation,
                                           "Solver": solver, "Learning rate": learning_rate, "Alpha": alpha}
                            classifier = "MLP"
                            classifier_obj = multilayer_perceptron

    # document which was best
    msg = str(time.time()) + ': The best ANN was an MLP trained with the parameters' + str(best_params) + \
          ' which produced an accuracy score of: ' + str(max_accuracy)
    print(msg)
    logging.info(msg)

    return {'Accuracy': max_accuracy, 'Classifier type': classifier, 'Params': best_params,
            'Classifier obj': classifier_obj}
