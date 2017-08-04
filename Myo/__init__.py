import data_processing
import k_nearest_neighbour
import artificial_neural_networks
import hidden_markov_models

from sklearn.model_selection import train_test_split


gesture_order = data_processing.pre_processing.generate_order_of_gestures()
data_processing.pre_processing.rename_data_files(gesture_order)
training_data, target_data_training, test_data, target_data_test = train_test_split(data, gesture_order, random_state=0)

knn_accuracy = k_nearest_neighbour.k_nearest_neighbour.train(target_data_training, training_data, target_data_test, test_data)
hmm_accuracy = hidden_markov_models.hidden_markov_model.train(target_data_training, training_data, target_data_test, test_data)
ann_accuracy = artificial_neural_networks.artificial_neural_network(target_data_training, training_data, target_data_test, test_data)