import logging
import numpy as np
import os
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
import time

filename = "knn_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def train_knn(x_train, x_test, y_train, y_test, sensor_data):
    msg = str(time.time()) + ": Experimenting with KNNs"
    print(msg)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logging.info(msg)

    default_knn = KNeighborsClassifier()
    default_knn.fit(x_train, y_train)
    max_accuracy = default_knn.score(x_test, y_test)
    classifier_obj = default_knn
    best_params = "default"
    y_score = default_knn.predict(x_test)


    parameters = {
        'n_neighbors': [26, 52],
        'weights': ('uniform', 'distance'),
        'algorithm': ('auto', 'ball_tree','kd_tree', 'brute'),
        'leaf_size': [x for x in range(5, 27)]
    }
    fitted_knn = get_parameters(parameters, x_train, y_train)
    if fitted_knn.score(x_test, y_test) > max_accuracy:
        classifier_obj = fitted_knn
        best_params = fitted_knn.best_params_
        y_score = fitted_knn.predict(x_test)
        max_accuracy = fitted_knn.score(x_test, y_test)

    msg = '{0}: The best KNN was one trained with the parameters {1} which produced an accuracy score of: ' \
          '{2} for {3} data'.format(str(time.time()), str(best_params), str(max_accuracy), str(sensor_data))
    print(msg)
    logging.info(msg)

    return {'Accuracy': max_accuracy, 'Classifier type': 'KNN', 'Params': best_params,
            'Classifier obj': classifier_obj, 'y_train': y_test, 'y_score': y_score}


def best_knn(x_train, x_test, y_train, y_test, sensor_data, return_values):
    best_classifier = train_knn(x_train, x_test, y_train, y_test, sensor_data)
    return_values[1] = best_classifier
    return return_values


def get_parameters(parameters, x_train, y_train):
    try:
        randomised = RandomizedSearchCV(KNeighborsClassifier(), parameters, n_iter=40, n_jobs=-1)
        return randomised.fit(x_train, y_train)
    except ValueError:
        grid = GridSearchCV(KNeighborsClassifier(), parameters)
    return grid.fit(x_train, y_train)

