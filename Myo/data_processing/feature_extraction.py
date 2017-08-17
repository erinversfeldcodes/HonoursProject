import logging
import os
import time

filename = "feature_extraction.log"
path_to_logs = os.path.abspath("log/")
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
logging.info(str(time.time()) + ": Loaded pre_processing.py")


def mean_absolute_value(window_length, data_in_window):
    total = 0

    for w in range(1, window_length):
        total += abs(data_in_window)

    mav = total/window_length

    return mav


def moving_variance(window_length, data_in_window, mean_data_in_window):
    total = 0

    for w in range(1, window_length):
        data_less_mean = data_in_window - mean_data_in_window
        total += data_less_mean ** 2

    mv = total / window_length

    return mv