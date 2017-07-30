from sklearn.neighbours import KNeighboursClassifier

def train(target_values_training, training_data, target_values_test, test_data):
    # maybe use some smexy EC to optimise the number of neighbours?
    number_of_neighbours = 3
    knn = KNeighboursClassifier(n_neighbours=number_of_neighbours)
    knn.fit(training_data, target_values_training)
    knn.predict(test_data)
    return knn.score(test_data, target_values_test)
