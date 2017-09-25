from models.utils import get_parameters

import logging
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import datetime

def train(x_train, y_train, x_test, y_test, sensor_data, return_values):
    default_knn = KNeighborsClassifier()
    default_knn.fit(x_train, y_train)
    best_knn = default_knn
    max_accuracy = default_knn.score(x_test, y_test)
    best_params = 'Default'
    method_params_found = 'Default'
    y_score = default_knn.predict(x_test)

    n_samples = np.array(x_train).shape[0]
    n = n_samples if n_samples < 200 else 200
    n_neighbours = list(range(1, n))
    parameters = {'n_neighbors': n_neighbours,
                  'weights': ('uniform', 'distance'),
                  'algorithm': ('auto', 'ball_tree', 'kd_tree', 'brute'),
                  'leaf_size': [no_leaves for no_leaves in range(5, 27)]
                  }

    knn, knn_method_params_found = get_parameters(parameters, KNeighborsClassifier(), x_train, y_train)
    knn_accuracy = knn.score(x_test, y_test)

    if knn_accuracy > max_accuracy:
        best_knn = knn
        max_accuracy = knn_accuracy
        best_params = knn.best_params_
        y_score = knn.score(x_test)
        method_params_found = knn_method_params_found

    date_time = datetime.now()
    msg = '{0}: The best MLP classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    logging.info(msg)
    print(msg)

    return_values[2] = {'model': best_knn,
                        'model_type': 'KNN',
                        'max_accuracy': max_accuracy,
                        'best_params': best_params,
                        'method': method_params_found,
                        'y_score': y_score,
                        'y_test': y_test
                        }
