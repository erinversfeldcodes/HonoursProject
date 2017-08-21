from Myo.data_processing.processing import *

import logging
from mlxtend.classifier import EnsembleVoteClassifier
from mlxtend.feature_selection import ColumnSelector
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def voting_ensemble_classifier(imu_classifier, emg_classifier):

    msg = "Training with both spatial and gesture data."
    print(msg)
    logging.info(msg)

    spatial_pipe = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)),
                                 imu_classifier)
    gestural_pipe = make_pipeline(ColumnSelector(cols=(9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)),
                                  emg_classifier)

    data = read_emg_and_imu()
    X = data[0]
    X = np.array(X)
    x_nsamples, x_nx, x_ny = X.shape
    X = X.reshape((x_nsamples, x_nx*x_ny))

    Y = data[1]
    Y = np.array(Y)
    Y = np.array(Y)
    y_nsamples, _ = Y.shape
    Y = Y.reshape((y_nsamples,))
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

    ensemble = EnsembleVoteClassifier(clfs=[spatial_pipe, gestural_pipe])
    ensemble.fit(x_train, y_train)
    accuracy = float(ensemble.score(x_test, y_test))

    return accuracy
