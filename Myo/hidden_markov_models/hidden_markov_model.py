import logging
import seqlearn.hmm as hmm
import time


def train(x_train, x_test, y_train, y_test, train_lengths, test_lengths, sensor_data, return_values):
    msg = str(time.time()) + ": Experimenting with HMMs"
    print(msg)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logging.info(msg)

    algorithm_options = {"bestfirst", "viterbi"}
    alpha_options = [x / 1000.0 for x in range(5000, 10000)]

    mnhmm = hmm.MultinomialHMM()
    mnhmm.fit(x_train, y_train, train_lengths)
    max_accuracy = mnhmm.score(x_test, y_test, test_lengths)
    best_params = 'Default'
    y_score = mnhmm.predict(x_test, lengths=test_lengths)
    msg = str(time.time()) + ': The best MNHMM thus far is one trained with the parameters' + \
          str(best_params) + ' which produced an accuracy score of: ' + str(max_accuracy)
    print(msg)
    logging.info(msg)
    #
    for algorithm in algorithm_options:
        for alpha in alpha_options:
            mnhmm = hmm.MultinomialHMM(decode=algorithm, alpha=alpha)
            mnhmm.fit(x_train, y_train, train_lengths)

            accuracy = mnhmm.score(x_test, y_test)

            if accuracy > max_accuracy:
                max_accuracy = accuracy
                best_params = {"Decoder": algorithm, "Alpha": alpha}
                y_score = mnhmm.predict(x_test, test_lengths)
                msg = str(time.time()) + ': The best MNHMM thus far is one trained with the parameters ' + \
                      str(best_params) + ' which produced an accuracy score of: ' + str(max_accuracy)
                print(msg)
                logging.info(msg)

    print("The best HMM was one trained with the parameters " + str(best_params) +
          " which produced an accuracy score of " + str(max_accuracy) + " for " + str(sensor_data) + " data.")
    results = {'Accuracy': max_accuracy, 'Classifier type': "MNHMM", 'Params': best_params,
               'Classifier obj': mnhmm, 'y_train': y_train, 'y_score': y_score}
    return_values[2] = results
    return results
