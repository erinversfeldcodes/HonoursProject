import datetime
import logging
import unittest

import os
import glob

import numpy as np

import data_processing.processing as processing

filename = "processing_tests_" + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")) + ".log"
path_to_logs = os.path.abspath('../log')
path_to_log_file = os.path.join(path_to_logs, filename)

logging.basicConfig(filename=path_to_log_file, format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)
logging.info('Loaded data_processing tests')


class ProcessingTests(unittest.TestCase):
    def setUp(self):
        self.sensor_data_options = {'emg', 'imu', 'both'}
        self.participant_options = {None, 1, 2, 3, 4, 5}
        self.fp_flag_options = {False, 'f', 'p', 'fp'}
        self.labels = ['a', 'a', 'a', 'b', 'z', 'c']
        self.emg_regex = "*-emg-*.csv"
        self.acc_regex = "*-acc-*.csv"
        self.gyro_regex = "*-gyro-*.csv"
        self.o_regex = "*-orientation-*.csv"
        self.oe_regex = "*-orientationEuler-*.csv"

        self.paths = {'vanilla_data': os.path.abspath('../data'),
                      'conll_folder': os.path.abspath('../data/conll'),
                      'fp_folder': os.path.abspath('../data/feat_extr_preproc'),
                      'f_folder': os.path.abspath('../data/feature_extracted'),
                      'p_folder': os.path.abspath('../data/preprocessed')
                      }

    def tearDown(self):
        pass


class GetDataConllTests(ProcessingTests):
   pass


class GetDataTests(ProcessingTests):
    pass


class ReadEMGAndIMUDataConllTests(ProcessingTests):
    pass


class ReadEMGAndIMUDataTests(ProcessingTests):
    pass


class ReadIMUDataConllTests(ProcessingTests):
    pass


class ReadIMUDataTests(ProcessingTests):
    pass


class ReadEMGDataConllTests(ProcessingTests):
    pass


class ReadEMGDataTests(ProcessingTests):
    pass


class GetEMGIMUXYTests(ProcessingTests):
    pass


class GetIMUXYTests(ProcessingTests):
    def setUp(self):
        super(GetIMUXYTests, self).setUp()

    def test_default_success(self):
        """
        CASE: Vanilla files given, fp_flag False
        :return: a list of values whose contents correspond to the contents of the files, and a second list of labels
        corresponding to the letter associated with the data
        """
        for participant in self.participant_options:
            if participant is None:
                pass
            else:
                folder = 'Participant ' + str(participant)
                path = os.path.join(self.paths.get('vanilla_data'), folder)
                path_regex = '/'.join([path, self.emg_regex])
                files = glob.glob(path_regex)

                returned_x, returned_y = processing.get_emg_x_y(files)
                # note: for final submission, the dummy values which were used to test this have been removed


    def test_empty_data_handled(self):
        """
        CASE: A file is empty it gets passed over
        :return: Two empty lists
        """
        folder = 'Participant 1'
        filename = 'a-accelerometer-1504250623.csv'
        file_path = os.path.join(folder, filename)
        empty_file_path = os.path.join(self.paths.get('vanilla_data'), file_path)
        returned_x, returned_y = processing.get_emg_x_y([empty_file_path])

        self.assertEqual(list(returned_x), [])
        self.assertEqual(list(returned_y), [])


class GetEMGXYTests(ProcessingTests):
    def setUp(self):
        super(GetEMGXYTests, self).setUp()


    def test_default_success(self):
        """
        CASE: Vanilla files given, fp_flag False
        :return: a list of values whose contents correspond to the contents of the files, and a second list of labels
        corresponding to the letter associated with the data
        """
        for participant in self.participant_options:
            if participant is None:
                pass
            else:
                folder = 'Participant ' + str(participant)
                path = os.path.join(self.paths.get('vanilla_data'), folder)
                path_regex = '/'.join([path, self.emg_regex])
                files = glob.glob(path_regex)

                returned_x, returned_y = processing.get_emg_x_y(files)
                # note: for final submission, the dummy values which were used to test functionality as it was
                # developed have been removed, as they obviously fail against real data


    def test_empty_data_handled(self):
        """
        CASE: A file is empty it gets passed over
        :return: Two empty lists
        """
        folder = 'Participant 1'
        filename = 'a-accelerometer-1504250623.csv'
        file_path = os.path.join(folder, filename)
        empty_file_path = os.path.join(self.paths.get('vanilla_data'), file_path)
        returned_x, returned_y = processing.get_emg_x_y([empty_file_path])

        self.assertEqual(list(returned_x), [])
        self.assertEqual(list(returned_y), [])
