import sklearn.neural_network as neural_network

def train(target_data_training, training_data, target_data_test, test_data):

    multilayer_perceptron = neural_network.MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)
    multilayer_perceptron.fit(training_data, target_data_training)
    multilayer_perceptron.predict(test_data)
    return multilayer_perceptron.score(test_data, target_data_test)
