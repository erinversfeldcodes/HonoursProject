from Myo.data_processing.processing import get_data

import logging
import os
from sklearn.neighbors import KNeighborsClassifier
import time

filename = "knn_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded the Myo directory's __init__ script")


def train(x_train, x_test, y_train, y_test):

    msg = str(time.time()) + ": Experimenting with KNNs"
    print(msg)
    logging.info(msg)

    weights_options = {'uniform', 'distance'}

    max_accuracy = 0
    best_params = None
    classifier = "KNN"
    classifier_obj = None

    # experiment with parameters
    # TODO: establish how to vary the 'algorithm' parameter
    for weight in weights_options:
        for neighbour in range(2, 3):  # :10):
            for leaves in range(3, 4):  # 50):

                # create, train, fit
                knn = KNeighborsClassifier(weights=weight, n_neighbors=neighbour, leaf_size=leaves)
                knn.fit(list(x_train), list(y_train))
                knn_accuracy = knn.score(list(x_test), list(y_test))

                # document results
                msg = str(time.time()) + ': Trained a KNN with the parameters' + str(("Weight: " + str(weight),
                                                                                      "num neighbours: " +
                                                                                      str(neighbour), "leaves: "
                                                                                      + str(leaves) +
                                                                                      " and it produced an accuracy"
                                                                                      " score of " + str(knn_accuracy)))
                logging.info(msg)

                if knn_accuracy > max_accuracy:
                    max_accuracy = knn_accuracy
                    best_params = {"Weight": weight, "Num neighbours":  neighbour, "Leaves": leaves}
                    classifier_obj = knn
                    msg = str(time.time()) + ': The best KNN thus far is one trained with the parameters' +\
                          str(best_params) + ' which produced an accuracy score of: ' + str(max_accuracy)
                    logging.info(msg)

    msg = str(time.time()) + ': The best KNN was one trained with the parameters ' + str(best_params) +\
          ' which produced an accuracy score of: ' + str(max_accuracy)
    print(msg)
    logging.info(msg)

    return {'Accuracy': max_accuracy, 'Classifier type': classifier, 'Params': best_params,
            'Classifier obj': classifier_obj}

