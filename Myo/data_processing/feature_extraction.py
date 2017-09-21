from biosppy.signals.tools import zero_cross as zero_crossings
import numpy as np
import os
import statistics
from statsmodels.tsa.ar_model import AR

conll_folder = os.path.abspath('data\\conll')


def mean_absolute_value(data):
    mav = []
    no_columns = len(data[0])
    no_rows = len(data)

    for column in range(no_columns):
        column_sum = 0
        for row in data:
            column_entry = row[column]
            column_sum += abs(column_entry)
        mean_abs = column_sum/no_rows
        mav.append(mean_abs)

    return mav


def standard_deviation(data):
    sd = []
    no_columns = len(data[0])

    for col in range(no_columns):
        column = []
        for row in data:
            column_entry = row[col]
            column.append(column_entry)
        col_sd = statistics.stdev(column)
        sd.append(col_sd)

    return sd


def zero_crossing_coefficients(data):
    zero_x_list = list(zero_crossings(data)[0])
    selected_zeros = [zero_x_list[0], zero_x_list[1], zero_x_list[2], zero_x_list[8]]
    return selected_zeros


def ar_coefficients(data):
    # try:
    one_D = np.array(np.array(data).flat)
    model = AR(one_D, missing='drop')
    nobs = one_D.shape[0]
    maxlag = nobs - 1
    fitted_model = model.fit(maxlag=maxlag)
    coefficients = fitted_model.params

    try:
        third, fourth, fifth, sixth = coefficients[2], coefficients[3], coefficients[4], coefficients[5]
        return [third, fourth, fifth, sixth]
    except IndexError:
        coeffs = []

        for i in range(3, 6):
            try:
                coeffs.append(coefficients[i])
            except IndexError:
                coeffs.append(0.0)

        return coeffs


def moving_average(data, window_len=10, window='hanning'):
    if np.array(data).ndim != 1:
        data = data.flatten()
        # raise ValueError("Moving average cannot be calculated for multidimensional data")

    s = np.r_[data[window_len-1:0:-1], data, data[-2:-window_len-1:-1]]
    w = eval('np.' + window + '(window_len)')
    y = np.convolve(w/w.sum(), s, mode='valid')

    return y
