import datetime
import logging

from sklearn.ensemble import ExtraTreesClassifier

from models.utils import get_parameters


def train(x_train, x_test, y_train, y_test, sensor_data, return_values):
    default_et = ExtraTreesClassifier()
    default_et.fit(x_train, y_train)
    best_et = default_et
    max_accuracy = default_et.score(x_test, y_test)
    best_params = 'Default'
    method_params_found = 'Default'
    y_score = default_et.predict(x_test)

    # parameter_options = {
    #     'n_estimators': [200, 400],
    #     'criterion': ['gini', 'entropy']
    # }
    # fitted_et, method = get_parameters(parameter_options, ExtraTreesClassifier(), x_train, y_train)
    # if fitted_et.score(x_test, y_test) > max_accuracy:
    #     best_et = fitted_et
    #     best_params = fitted_et.best_params_
    #     max_accuracy = fitted_et.score(x_test, y_test)
    #     y_score = fitted_et.predict(x_test)
    #     method_params_found = method

    date_time = datetime.datetime.now()
    msg = '{0}: The best ET classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    logging.info(msg)
    print(msg)

    return_values[3] = {'model': best_et,
                        'model_type': 'ET',
                        'sensor_data': sensor_data,
                        'max_accuracy': max_accuracy,
                        'best_params': best_params,
                        'method': method_params_found,
                        'y_score': y_score,
                        'y_test': y_test
                        }
