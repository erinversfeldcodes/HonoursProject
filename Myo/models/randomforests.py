import datetime
import logging

from sklearn.ensemble import RandomForestClassifier

from models.utils import get_parameters


def train(x_train, x_test, y_train, y_test, sensor_data, return_values):
    parameter_options = {
        'n_estimators': [26, 52],
        'criterion': ['gini', 'entropy'],
    }
    fitted_rf, method_params_found = get_parameters(parameter_options, RandomForestClassifier(), x_train, y_train)
    best_params = fitted_rf.best_params_
    max_accuracy = fitted_rf.score(x_test, y_test)
    y_score = fitted_rf.predict(x_test)

    date_time = datetime.now()
    msg = '{0}: The best RF classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    print(msg)
    logging.info(msg)

    return_values[1] = {'model': fitted_rf,
                        'model_type': 'RF',
                        'max_accuracy': max_accuracy,
                        'best_params': best_params,
                        'method': method_params_found,
                        'y_score': y_score,
                        'y_test': y_test
                        }
