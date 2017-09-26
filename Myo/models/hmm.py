import datetime
import logging
import seqlearn.hmm as hmm

import numpy as np


def train(x_train, x_test, y_train, y_test, train_lengths, test_lengths, sensor_data):
    # algorithm_options = {"bestfirst", "viterbi"}
    # alpha_options = [x / 1000.0 for x in range(5000, 10000)]

    default_model = hmm.MultinomialHMM()
    default_model.fit(np.array(x_train), y_train, train_lengths)
    max_accuracy = default_model.score(np.array(x_test), y_test, test_lengths)
    best_params = 'Default'
    method_params_found = 'Default'
    y_score = default_model.predict(np.array(x_test), lengths=test_lengths)

    best_model = default_model

    # for algorithm in algorithm_options:
    #     for alpha in alpha_options:
    #         mnhmm = hmm.MultinomialHMM(decode=algorithm, alpha=alpha)
    #         mnhmm.fit(x_train, y_train, train_lengths)
    #
    #         accuracy = mnhmm.score(x_test, y_test)
    #
    #         if accuracy > max_accuracy:
    #             max_accuracy = accuracy
    #             best_params = {"Decoder": algorithm, "Alpha": alpha}
    #             y_score = mnhmm.predict(x_test, test_lengths)
    #             method_params_found = 'Brute force'
    #             best_model = mnhmm

    date_time = datetime.datetime.now()
    msg = '{0}: The best MNHMM classifier was trained with the parameters {1} which produced an accuracy score of: {2}' \
          'for {3} data. These parameters were found using the {4} method.'.format(str(date_time), str(best_params),
                                                                                   str(max_accuracy), str(sensor_data),
                                                                                   str(method_params_found))
    logging.info(msg)
    print(msg)

    return {'model': best_model,
            'model_type': 'MNHMM',
            'max_accuracy': max_accuracy,
            'best_params': best_params,
            'method': method_params_found,
            'y_score': y_score,
            'y_test': y_test
            }
    # return_values[4] = {'model': best_model,
    #                     'model_type': 'MNHMM',
    # 'sensor_data': sensor_data,
    #                     'max_accuracy': max_accuracy,
    #                     'best_params': best_params,
    #                     'method': method_params_found,
    #                     'y_score': y_score,
    #                     'y_test': y_test
    #                     }
#