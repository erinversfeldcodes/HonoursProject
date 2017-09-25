import datetime
import logging

from sklearn.ensemble import ExtraTreesClassifier

from models.utils import get_parameters


def train(x_train, x_test, y_train, y_test, sensor_data, return_values):
    parameter_options = {
        'n_estimators': [200, 400],
        'criterion': ['gini', 'entropy']
    }
    fitted_et, method_params_found = get_parameters(parameter_options, ExtraTreesClassifier(), x_train, y_train)
    best_params = fitted_et.best_params_
    max_accuracy = fitted_et.score(x_test, y_test)
    y_score = fitted_et.predict(x_test)

    date_time = datetime.now()
    msg = '{0}: The best MLP classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    logging.info(msg)
    print(msg)

    return_values[3] = {'model': fitted_et,
                        'model_type': 'KNN',
                        'max_accuracy': max_accuracy,
                        'best_params': best_params,
                        'method': method_params_found,
                        'y_score': y_score,
                        'y_test': y_test
                        }
