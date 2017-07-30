import numpy
from hmmlearn import hmm

def train(target_values_training, training_data, target_values_test, test_data):

    numpy.random.seed(42)

    number_of_states = None


    gaussian = hmm.GaussianHMM(n_components=number_of_states).fit()
    gmm = hmm.GMMHMM()
    multinomial = hmm.MultinomialHMM()