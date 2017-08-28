import logging
import glob
import os

from pandas import Series
from statsmodels.tsa.ar_model import AR
import time

# filename = "feature_extraction.log"
# path_to_logs = os.path.abspath("log/")
# path_to_log_file = os.path.join(path_to_logs, filename)
#
# logging.basicConfig(filename=path_to_log_file, level=logging.DEBUG)
# logging.info(str(time.time()) + ": Loaded pre_processing.py")


def calculate_ar_coefficients(data):
    # try:
    model = AR(data)
    fitted_model = model.fit()
    coefficients = fitted_model.params

    third, fourth, fifth, sixth = coefficients[2], coefficients[3], coefficients[4], coefficients[5]

    return [third, fourth, fifth, sixth]
    # except ValueError:
    #     return False


def emg_features(data):
    ar_coefficients = calculate_ar_coefficients(data)

    return ar_coefficients

# emg_files = glob.glob(os.path.join("../data/myo_data", "*-emg-*.csv"))
# for file in emg_files:
#     emg_features(file)
