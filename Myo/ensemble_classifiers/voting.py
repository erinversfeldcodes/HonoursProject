from Myo.data_processing.processing import *

import logging
from mlxtend.classifier import EnsembleVoteClassifier
from mlxtend.feature_selection import ColumnSelector
from sklearn.pipeline import make_pipeline


def voting_ensemble_classifier(classifier_1, classifier_2, x_train, x_test, y_train, y_test, feat_extr=False):

    msg = "Training with both spatial and gesture data."
    print(msg)
    logging.info(msg)

    if feat_extr:
        spatial_pipe = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4)), classifier_1)
        gestural_pipe = make_pipeline(ColumnSelector(cols=(5, 6, 7, 8)), classifier_2)
    else:
        spatial_pipe = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)), classifier_1)
        gestural_pipe = make_pipeline(ColumnSelector(cols=(9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)),
                                      classifier_2)

    ensemble = EnsembleVoteClassifier(clfs=[spatial_pipe, gestural_pipe])
    ensemble.fit(x_train, y_train)
    accuracy = float(ensemble.score(x_test, y_test))

    return accuracy
