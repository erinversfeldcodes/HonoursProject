import numpy as np
from sklearn import neighbours

import string
import sys

class KNN_Classifier(object):
    """
    A classifier of Myo gestures using the K-nearest neighbour (KNN) algorithm
    """

    def __init__(self):
        for participant_number in range(sys.argv[1]):
            for letter in list(string.ascii_lowercase):
                for performance_number in range(1, 6):
                    filename = str(participant_number)+"_"+str(letter)+"_"+str(performance_number)+".csv"
                    with open(filename) as file:
                        pass
        self.read_data()

    def read_data(self):
        X = []
        Y = []

        for participant_number in range(sys.argv[1]):
            for letter in list(string.ascii_lowercase):
                for performance_number in range(1, 6):
                    filename = str(participant_number)+"_"+str(letter)+"_"+str(performance_number)+".csv"
                    X.append(np.fromfile(filename, dtype=np.unit16).reshape((-1, 8)))
                    Y.append(np.zeros(X[-1].shape[0]))

        self.X = np.vstack(X)
        self.Y = np.vstack(Y)

        self.train()

    def train(self):
        self.nn = neighbours.KNeighboursClassifier(n_neighbours=5, algorithm='kd_tree').fit(self.X[::-3], self.Y[::-3])


if __name__ == '__main__':

    classifier = KNN_Classifier()
