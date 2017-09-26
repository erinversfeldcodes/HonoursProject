from globals import number_of_classes, alpha
from models.utils import get_parameters

import logging
from sklearn.neural_network import MLPClassifier
import datetime

def train(x_train, x_test, y_train, y_test, sensor_data, return_values):
    default_ann = MLPClassifier()
    default_ann.fit(x_train, y_train)
    best_ann = default_ann
    max_accuracy = default_ann.score(x_test, y_test)
    best_params = 'Default'
    method_params_found = 'Default'
    y_score = default_ann.predict(x_test)

    # if number_of_classes > len(x_train):
    #     nodes_per_layer_range = range(len(x_train), number_of_classes)
    # else:
    #     nodes_per_layer_range = range(number_of_classes, len(x_train))
    #
    # parameters = {'hidden_layer_sizes': [(num_nodes,) for num_nodes in nodes_per_layer_range],
    #               'activation': ('logistic', 'relu', 'identity'),
    #               'max_iter': [1000, 1500, 2000],
    #               'learning_rate': ['constant', 'invscaling', 'adaptive'],
    #               'alpha': alpha}
    #
    # ann, ann_method_params_found = get_parameters(parameters, MLPClassifier(), x_train, y_train)
    # ann_accuracy = ann.score(x_test, y_test)
    #
    # if ann_accuracy > max_accuracy:
    #     best_ann = ann
    #     max_accuracy = ann_accuracy
    #     best_params = ann.best_params_
    #     y_score = ann.score(x_test)
    #     method_params_found = ann_method_params_found

    date_time = datetime.datetime.now()
    msg = '{0}: The best MLP classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    print(msg)
    logging.info(msg)

    return_values[0] = {'model': best_ann,
                        'model_type': 'MLP',
                        'sensor_data': sensor_data,
                        'max_accuracy': max_accuracy,
                        'best_params': best_params,
                        'method': method_params_found,
                        'y_score': y_score,
                        'y_test': y_test
                        }
