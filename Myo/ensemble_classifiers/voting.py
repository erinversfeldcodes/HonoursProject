from Myo.data_processing.processing import read_data

from mlxtend.classifier import EnsembleVoteClassifier
from mlxtend.feature_selection import ColumnSelector
from sklearn.neighbors import KNeighborsClassifier
import sklearn.neural_network as neural_network
from sklearn.pipeline import make_pipeline


def voting_ensemble_classifier(spatial_classifier, spatial_params, gestural_classifier, gestural_params):
    if spatial_classifier == "KNN":

        weights = spatial_params.get("Weight")
        n_neighbours = spatial_params.get("Num neighbours")
        leaf_size = spatial_params.get("Leaves")

        spatial_classifier = KNeighborsClassifier(weights, n_neighbours, leaf_size)

    elif spatial_classifier == "MLP":

        hidden_layer_sizes = spatial_params.get("Layer sizes")
        activation = spatial_params.get("Activation")
        solver = spatial_params.get("Solver")
        learning_rate = spatial_params.get("Learning rate")

        spatial_classifier = neural_network.MLPClassifier(hidden_layer_sizes=(hidden_layer_sizes,),
                                                          activation=activation, solver=solver, alpha=1e-5,
                                                          learning_rate=learning_rate, early_stopping=True)
    else:
        print("Can't establish the spatial classifier type")

    if gestural_classifier == "KNN":

        weights = gestural_params.get("Weight")
        n_neighbours = gestural_params.get("Num neighbours")
        leaf_size = gestural_params.get("Leaves")

        gestural_classifier = KNeighborsClassifier(weights, n_neighbours, leaf_size)

    elif gestural_classifier == "MLP":

        hidden_layer_sizes = gestural_params.get("Layer sizes")
        activation = gestural_params.get("Activation")
        solver = gestural_params.get("Solver")
        learning_rate = gestural_params.get("Learning rate")

        gestural_classifier = neural_network.MLPClassifier(hidden_layer_sizes=(hidden_layer_sizes,),
                                                           activation=activation, solver=solver, alpha=1e-5,
                                                           learning_rate=learning_rate, early_stopping=True)
    else:
        print("Can't establish the gestural classifier type")

    spatial_pipe = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)),
                                 spatial_classifier)
    gestural_pipe = make_pipeline(ColumnSelector(cols=(15, 16, 17, 18, 19, 20, 21, 22)), gestural_classifier)

    data = read_data(step=40)
    X = data[0]
    Y = data[1]

    ensemble = EnsembleVoteClassifier(clfs=[spatial_pipe, gestural_pipe])
    ensemble.fit(X, Y)
