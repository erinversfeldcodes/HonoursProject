import logging
import os
import numpy as np
import sklearn.neural_network as neural_network
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import time

filename = "ann_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info(str(time.time()) + " Loaded ann.py")


def mlp(x_train, x_test, y_train, y_test, sensor_data):
    m = neural_network.MLPClassifier()
    m.fit(x_train, y_train)
    max_accuracy = m.score(x_test, y_test)
    best_params = "Default"
    y_score = m.predict(x_test)

    if 26 > len(x_train):
        nodes_per_layer_range = range(len(x_train), 26, 5)
    else:
        nodes_per_layer_range = range(26, len(x_train), 5)

    parameters = {'hidden_layer_sizes': [(x,) for x in nodes_per_layer_range],
                  'activation': ('logistic', 'relu', 'identity'),
                  'max_iter': [1000],
                  'learning_rate': ['constant', 'invscaling', 'adaptive'],
                  'alpha': np.logspace(-5, 3, 5)}
    mlp = get_parameters(parameters, x_train, y_train)
    if mlp.score(x_test, y_test) > max_accuracy:
        m = mlp
        max_accuracy = mlp.score(x_test, y_test)
        best_params = mlp.best_params_
        y_score = mlp.predict(x_test)

    msg = '{0}: The best MLP classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          ' for {3} data'.format(str(time.time()), str(best_params), str(max_accuracy), str(sensor_data))
    print(msg)
    logging.info(str(time.time()) + ": " + msg)

    return {'Accuracy': max_accuracy, 'Classifier type': 'MLP', 'Params': best_params,
            'Classifier obj': m, 'y_train': y_test, 'y_score': y_score}


def get_parameters(parameters, x_train, y_train):
    try:
        randomised = RandomizedSearchCV(neural_network.MLPClassifier(), parameters, n_iter=40, n_jobs=-1)
        return randomised.fit(x_train, y_train)
    except ValueError:
        grid = GridSearchCV(neural_network.MLPClassifier(), parameters)
    return grid.fit(x_train, y_train)


def best_ann(x_train, x_test, y_train, y_test, sensor_data, return_values):
    msg = str(time.time()) + ": Experimenting with ANNs"
    print(msg)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    logging.info(str(time.time()) + ": " + msg)
    m = mlp(x_train, x_test, y_train, y_test, sensor_data)
    return_values[0] = m

    return return_values
