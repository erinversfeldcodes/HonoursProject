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

    activation_options = {'identity', 'logistic', 'tanh', 'relu'}
    solver_options = {'lbfgs', 'sgd', 'adam'}
    learning_rate_options = {'constant', 'invscaling', 'adaptive'}
    # TODO: Experiment with different alpha and hidden layer values

    max_accuracy = 0
    # best_algorithm = None
    best_options = None

    for activation in activation_options:
        for solver in solver_options:
            for learning_rate in learning_rate_options:
                for hidden_layer_sizes in range(1, 20):

                    multilayer_perceptron = neural_network.MLPClassifier(hidden_layer_sizes=(hidden_layer_sizes,), activation=activation,
                                                                         solver=solver, alpha=1e-5,
                                                                         learning_rate=learning_rate, early_stopping=True)
                    multilayer_perceptron.fit(list(x_train), list(y_train))

                    mlp_accuracy = multilayer_perceptron.score(list(x_test), list(y_test))

                    # multilayer_regressor = neural_network.MLPRegressor(hidden_layer_sizes=(15,), activation=activation,
                    #                                                    solver=solver, alpha=1e-5,
                    #                                                    learning_rate=learning_rate, early_stopping=True)
                    #best_algorithm,i multilayer_regressor.fit(list(x_train), list(y_train))
                    #
                    # mlpr_accuracy = multilayer_regressor.score(list(x), list(y))
                    #
                    #
                    # if mlp_accuracy > mlpr_accuracy:
                    #     accuracy = mlpr_accuracy
                    #     algorithm = "MLP"
                    #
                    # else:
                    #     accuracy = mlp_accuracy
                    #     algorithm = "MLPR"

                    logging.info(str(time.time()) + ": Trained an ANN with options " + str(
                        {"Hidden layer sizes: " + str(hidden_layer_sizes), "activation: " + str(activation),
                         "solver: " + str(solver),
                         " learning rate: " + str(learning_rate) + ", and it produced an accuracy score of " + str(
                             mlp_accuracy) + '.'}))
                    if mlp_accuracy > max_accuracy:
                        max_accuracy = mlp_accuracy
                        # best_algorithm = algorithm
                        best_options = {activation, solver, learning_rate}


    return max_accuracy, best_options  # best_algorithm,
