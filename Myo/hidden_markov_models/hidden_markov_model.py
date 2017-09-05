from Myo.data_processing.processing import get_data_conll

import logging
import seqlearn.hmm as hmm
import time


def train(x_train, x_test, y_train, y_test, lengths):
    msg = str(time.time()) + ": Experimenting with HMMs"
    print(msg)
    logging.info(msg)

    algorithm_options = {"bestfirst", "viterbi"}
    alpha_options = [x / 1000.0 for x in range(10, 11)]  # 1000)]

    max_accuracy = 0
    best_params = None
    classifier = "MNHMM"
    classifier_obj = None


    for algorithm in algorithm_options:
        for alpha in alpha_options:
            mnhmm = hmm.MultinomialHMM(decode=algorithm, alpha=alpha)
            mnhmm.fit(x_train, y_train, lengths)

            accuracy = mnhmm.score(x_test, y_test)

            msg = str(time.time()) + ": Trained an MDHMM with options decode " + str(algorithm) +\
                  ", alpha " + str(alpha) + ", and it produced an accuracy score of " + str(accuracy) + '.'
            logging.info(msg)

            if accuracy > max_accuracy:
                max_accuracy = accuracy
                best_params = {"Decoder": algorithm, "Alpha": alpha}
                classifier = "MNHMM"
                classifier_obj = mnhmm

    print("The best HMM was one trained with the parameters " + str(best_params) +
          " which produced an accuracy score of " + str(max_accuracy))
    return {'Accuracy': max_accuracy, 'Classifier type': classifier, 'Params': best_params,
            'Classifier obj': classifier_obj}
