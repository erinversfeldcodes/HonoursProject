import logging
import numpy as np
import os
import pandas as pd
import re
import sys
import time

filename = "processing_" + str(time.time())
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info("Loaded processing.py")


def read_emg_data(path_to_emg_files_list=None, step=180):

    X = []
    Y = []
    processed_data_path = os.path.abspath("data/processed_data")

    for path_to_file in path_to_emg_files_list:
        emg_filename = os.path.basename(path_to_file)
        try:
            for i in range(0, 1000, step):
                gesture = pd.read_csv(path_to_file, skiprows=[i], nrows=step, header=None).as_matrix(
                [1, 2, 3, 4, 5, 6, 7, 8])  # returns a numpy array, which I can use in train_split

                gesture = gesture.flatten()

                if len(gesture) == step * 8:
                    gesture = gesture[8:]
                    X.append(gesture)
                    gesture_name = emg_filename[0]
                    Y.append(gesture_name)

        except Exception:
            logging.error(str(time.time()) + " No data in: " + str(path_to_file))

    X_path = os.path.join(processed_data_path, "X.npy")
    Y_path = os.path.join(processed_data_path, "Y.npy")
    np.save(X_path, X)
    np.save(Y_path, Y)

    return X, Y

    np.save()
