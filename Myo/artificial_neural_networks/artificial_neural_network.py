import logging
import os
import sklearn.neural_network as neural_network
import time

filename = "processing_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info(str(time.time()) + " Loaded processing.py")

def train(x_train, x_test, y_train, y_test):

    activation_options = {'identity', 'logistic', 'tanh', 'relu'}
    solver_options = {'lbfgs', 'sgd', 'adam'}
    learning_rate_options = {'constant', 'invscaling', 'adaptive'}

    max_accuracy = 0
    best_options = None

    for activation in activation_options:
        for solver in solver_options:
            for learning_rate in learning_rate_options:

                multilayer_perceptron = neural_network.MLPClassifier(hidden_layer_sizes=(15,), activation=activation,
                                                                     solver=solver, alpha=1e-5,
                                                                     learning_rate=learning_rate, early_stopping=True)
                multilayer_perceptron.fit(list(x_train), list(y_train))

                accuracy = multilayer_perceptron.score(list(x_test), list(y_test))

                if accuracy > max_accuracy:
                    max_accuracy = accuracy
                    best_options = {activation, solver, learning_rate}

    # logging.info(str(time.time()) + " Best performing combination of parameters was: " + str(best_options) + " at " + max_accuracy)
    return max_accuracy, best_options
