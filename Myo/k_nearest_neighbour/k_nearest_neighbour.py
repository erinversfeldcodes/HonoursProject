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
    # maybe use some smexy EC to optimise the number of neighbours?

    weights_options = {'uniform', 'distance'}

    # p
    # leaf size
    # n_neighbours
    # number_of_neighbours = 3

    max_accuracy = 0
    best_combo = None

    for weight in weights_options:
        # # for algorithm in algorithm_options:
        # #     for metric in metric_options:
        #         if metric in {'seuclidean', 'mahalanobis'}:
        #             metric_params = {'V': np.cov(X)}
        #         else:
        #             metric_params = None
        for neighbour in range(3, 16):
            for leaves in range(30, 50):
                knn = KNeighborsClassifier(weights=weight, n_neighbors=neighbour, leaf_size=leaves)

                knn.fit(list(x_train), list(y_train))
                knn_accuracy = knn.score(list(x_test), list(y_test))

                msg = str(time.time()) + ': Trained a KNN with the parameters' + str(("Weight: " + str(weight), "num neighbours: " + str(neighbour), "leaves: " + str(leaves)))
                logging.info(msg)

                if knn_accuracy > max_accuracy:
                    max_accuracy = knn_accuracy
                    algorithm = "KNN"
                    best_combo = {"Weight": weight, "Num neighbours":  neighbour, "Leaves": leaves}
                    msg = str(time.time()) + ': The best KNN thus far is one trained with the parameters' + str(best_combo) + ' which produced an accuracy score of: ' + str(max_accuracy)
                    logging.info(msg)

    msg = str(time.time()) + ': The best KNN was one trained with the parameters' + str(best_combo) + ' which produced an accuracy score of: ' + str(max_accuracy)
    print(msg)
    logging.info(msg)

    return [max_accuracy, algorithm, best_combo]
