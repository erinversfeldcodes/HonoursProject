from Myo.data_processing.processing import get_data

import logging
import numpy as np
import random
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import time


def train(x_train, x_test, y_train, y_test):
    print("Experimenting with LDAs")

    solvers = {'svd', 'lsqr', 'eigen'}
    shrink = {0, 1, 2}


    max_accuracy = 0
    best_params = None
    classifier = "LDA"
    classifier_obj = None

    for solver in solvers:
        if solver == 'lsqr' or solver == 'eigen':
            for s in shrink:
                try:
                    if s == 0:
                        s = None
                    elif s == 1:
                        s = 'auto'
                    else:
                        s = random.uniform(0, 1)

                    lda = LinearDiscriminantAnalysis(solver=solver, shrinkage=s)
                    lda.fit(x_train, y_train)
                    accuracy = lda.score(x_test, y_test)

                    msg = str(time.time()) + ": Trained an LDA with options solver " + str(solver) + ", shrinkage " +\
                          str(s) + ", and it produced an accuracy score of " + str(accuracy) + '.'
                    logging.info(msg)

                    if accuracy > max_accuracy:
                        max_accuracy = accuracy
                        best_params = {"Solver": solver, "Shrinkage": s}
                        classifier = "LDA"
                        classifier_obj = lda

                except np.linalg.linalg.LinAlgError:
                    print("No eigenvalues or eigenvectors can be computed")
                    pass

        else:
            lda = LinearDiscriminantAnalysis(solver=solver)
            lda.fit(x_train, y_train)
            accuracy = lda.score(x_test, y_test)

            msg = str(time.time()) + ": Trained an LDA with options solver " + str(solver) + ", and it produced an" \
                                                                                             " accuracy score of " +\
                  str(accuracy) + '.'
            logging.info(msg)

            if accuracy > max_accuracy:
                max_accuracy = accuracy
                best_params = {"Solver": solver}
                classifier = "LDA"
                classifier_obj = lda

    print("The best LDA was one trained with the parameters " + str(best_params) + " which produced an accuracy score"
                                                                                   " of " + str(max_accuracy))
    return {'Accuracy': max_accuracy, 'Classifier type': classifier, 'Params': best_params,
            'Classifier obj': classifier_obj}

