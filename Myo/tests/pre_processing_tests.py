import pre_processing as pre_processing

import os
import string
import unittest


class GenerateOrderOfGestures(unittest.TestCase):
    """
    Run a series of tests to evaluate the logic of generate_order_of_gestures()
    """
    def setUp(self):
        """
        Define a series of variables common to the tests for generate_order_of_gestures()
        :return: The absolute path to the data used in these tests
        """
        self.path_to_test_data = os.path.abspath("test_data/gesture_orders/")

    def test_produces_a_flat_list(self):
        """
        Evaluate whether generate_order_of_gestures() produces a 1D array
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        order_of_gestures = ['o', 'j', 'p', 'r', 'b', 'c', 'q', 'd', 'v', 'r', 'd', 'v', 'm', 'f', 'y', 'h', 'i', 'j',
                             'a', 'a', 'a', 'r', 'y', 'i', 'n', 'z', 'e', 'y', 'q', 'c', 'e', 'j', 'a', 'b', 'h', 'l',
                             'u', 'h', 'h', 'f', 't', 'm', 'f', 'f', 'o', 'r', 'g', 'd', 'i', 'p', 't', 'z', 'i', 'v',
                             'p', 'h', 'z', 'p', 'i', 'h', 'r', 'q', 'z', 'u', 'l', 'm', 'n', 'g', 'i', 'm', 'f', 'r',
                             'e', 'c', 'y', 'l', 'o', 'w', 'y', 'r', 'r', 'd', 'x', 'z', 'g', 'g', 'm', 'c', 'i', 's',
                             'x', 'z', 'b', 'w', 'z', 'k', 'j', 'h', 'j', 'x', 'g', 'c', 'c', 'd', 'v', 'e', 'h', 'b',
                             'n', 'm', 'b', 'u', 'a', 'w', 'n', 'k', 'x', 'w', 'w', 'o', 'n', 'm', 'i', 'j', 'l', 'e',
                             'k', 'q', 'c', 'e', 'c', 'u', 'b', 'g', 'x', 'p', 'p', 'x', 'o', 't', 's', 'k', 'v', 'n',
                             'u', 's', 'o', 'z', 'u', 't', 'l', 't', 'j', 'd', 'k', 'f', 'q', 'g', 'i', 'p', 'b', 'v',
                             'n', 'j', 'j', 'r', 't', 'l', 'x', 'g', 'k', 'h', 'f', 'y', 'v', 'n', 'e', 'j', 's', 'p',
                             'e', 't', 'a', 'w', 'k', 'v', 'u', 't', 'p', 'd', 'q', 'i', 'h', 'g', 'v', 'd', 'f', 'd',
                             'q', 'q', 'd', 'k', 'q', 'a', 'o', 'x', 'c', 't', 'z', 'w', 'e', 's', 'y', 'l', 'm', 's',
                             'z', 'e', 'y', 'k', 's', 's', 't', 'm', 'l', 'l', 'g', 'u', 'o', 'f', 'r', 's', 'l', 'a',
                             'u', 'w', 'n', 'k', 'p', 'w', 'a', 'w', 'b', 'x', 'f', 's', 'a', 'o', 'y', 'm', 'b', 'o',
                             'u', 'b', 'q', 'c', 'v', 'x', 'y', 'n']
        self.assertEqual(pre_processing.generate_order_of_gestures(path_to_files=self.path_to_test_data,
                                                                   total_participants=1,
                                                                   total_rounds=26),
                         order_of_gestures)

    def test_ten_of_each_letter_performed(self):
        """
        Evaluate whether the result of generate_order_of_gestures() contains ten instances of each letter. This verifies
        that the correct number of gestures were performed
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        alphabet = list(string.ascii_lowercase)
        gestures = pre_processing.generate_order_of_gestures(path_to_files=self.path_to_test_data,
                                                             total_participants=1,
                                                             total_rounds=26)

        for letter in alphabet:
            occurrence_of_letter = gestures.count(letter)
            self.assertEqual(occurrence_of_letter, 10)


class RenameDataFile(unittest.TestCase):
    """
    Run a series of tests to evaluate the logic of rename_data_file()
    """
    def setUp(self):
        """
        Define a series of variables common to the tests for rename_data_file()
        :return: The time stamps, number of time stamps, gestures, number of gestures and absolute path to the data
        used in these tests
        """
        self.time_stamps = ['1501622034', '1501622042', '1501622055', '1501622064', '1501622072',
                            '1501622079', '1501622086', '1501622095', '1501622101', '1501622109']
        self.gestures = ['o', 'j', 'p', 'r', 'b', 'c', 'q', 'd', 'v', 'r']
        self.number_of_gestures = len(self.gestures)
        self.number_of_time_stamps = len(self.time_stamps)
        self.path_to_test_data = os.path.abspath("test_data/myo_data/")

    def tearDown(self):
        """
        Restore the test environment to it's original state
        :return: The original names of the data files used in these tests
        """
        for file in os.listdir(self.path_to_test_data):
            directory_levels = file.split("/")
            directory_levels[-1] = directory_levels[-1][2:]
            old_filename = "/".join(directory_levels)
            os.rename(file, old_filename)

    def test_renames_accelerometer_data_files_correctly(self):
        """
        Evaluate whether rename_data_file() renames the accelerometer data files correctly.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        correct_names = ['o-accelerometer-1501622034.csv',
                         'j-accelerometer-1501622042.csv',
                         'p-accelerometer-1501622055.csv',
                         'r-accelerometer-1501622064.csv',
                         'b-accelerometer-1501622072.csv',
                         'c-accelerometer-1501622079.csv',
                         'q-accelerometer-1501622086.csv',
                         'd-accelerometer-1501622095.csv',
                         'v-accelerometer-1501622101.csv',
                         'r-accelerometer-1501622109.csv']

        self.assertEqual(self.number_of_gestures, self.number_of_time_stamps)

        for i in range(self.number_of_gestures):
            time_stamp = self.time_stamps[i]
            gesture = self.gestures[i]
            correct_name = correct_names[i]
            new_filename = pre_processing.rename_data_file(time_stamp, gesture, "accelerometer", path_to_file=self.path_to_test_data)

            self.assertEqual(new_filename, correct_name)

    def test_renames_emg_data_files_correctly(self):
        """
        Evaluate whether rename_data_file() renames the emg data files correctly.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        correct_names = ['o-emg-1501622034.csv',
                         'j-emg-1501622042.csv',
                         'p-emg-1501622055.csv',
                         'r-emg-1501622064.csv',
                         'b-emg-1501622072.csv',
                         'c-emg-1501622079.csv',
                         'q-emg-1501622086.csv',
                         'd-emg-1501622095.csv',
                         'v-emg-1501622101.csv',
                         'r-emg-1501622109.csv']

        self.assertEqual(self.number_of_gestures, self.number_of_time_stamps)

        for i in range(self.number_of_gestures):
            time_stamp = self.time_stamps[i]
            gesture = self.gestures[i]
            correct_name = correct_names[i]
            new_filename = pre_processing.rename_data_file(time_stamp, gesture, "emg", path_to_file=self.path_to_test_data)

            self.assertEqual(new_filename, correct_name)

    def test_renames_gyro_data_files_correctly(self):
        """
        Evaluate whether rename_data_file() renames the gyro data files correctly.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        correct_names = ['o-gyro-1501622034.csv',
                         'j-gyro-1501622042.csv',
                         'p-gyro-1501622055.csv',
                         'r-gyro-1501622064.csv',
                         'b-gyro-1501622072.csv',
                         'c-gyro-1501622079.csv',
                         'q-gyro-1501622086.csv',
                         'd-gyro-1501622095.csv',
                         'v-gyro-1501622101.csv',
                         'r-gyro-1501622109.csv']

        self.assertEqual(self.number_of_gestures, self.number_of_time_stamps)

        for i in range(self.number_of_gestures):
            time_stamp = self.time_stamps[i]
            gesture = self.gestures[i]
            correct_name = correct_names[i]
            new_filename = pre_processing.rename_data_file(time_stamp, gesture, "gyro", path_to_file=self.path_to_test_data)

            self.assertEqual(new_filename, correct_name)

    def test_renames_orientation_data_files_correctly(self):
        """
        Evaluate whether rename_data_file() renames the orientation data files correctly.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        correct_names = ['o-orientation-1501622034.csv',
                         'j-orientation-1501622042.csv',
                         'p-orientation-1501622055.csv',
                         'r-orientation-1501622064.csv',
                         'b-orientation-1501622072.csv',
                         'c-orientation-1501622079.csv',
                         'q-orientation-1501622086.csv',
                         'd-orientation-1501622095.csv',
                         'v-orientation-1501622101.csv',
                         'r-orientation-1501622109.csv']

        self.assertEqual(self.number_of_gestures, self.number_of_time_stamps)

        for i in range(self.number_of_gestures):
            time_stamp = self.time_stamps[i]
            gesture = self.gestures[i]
            correct_name = correct_names[i]
            new_filename = pre_processing.rename_data_file(time_stamp, gesture, "orientation", path_to_file=self.path_to_test_data)

            self.assertEqual(new_filename, correct_name)

    def test_renames_orientationEuler_data_files_correctly(self):
        """
        Evaluate whether rename_data_file() renames the orientation euler data files correctly.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        correct_names = ['o-orientationEuler-1501622034.csv',
                         'j-orientationEuler-1501622042.csv',
                         'p-orientationEuler-1501622055.csv',
                         'r-orientationEuler-1501622064.csv',
                         'b-orientationEuler-1501622072.csv',
                         'c-orientationEuler-1501622079.csv',
                         'q-orientationEuler-1501622086.csv',
                         'd-orientationEuler-1501622095.csv',
                         'v-orientationEuler-1501622101.csv',
                         'r-orientationEuler-1501622109.csv']

        self.assertEqual(self.number_of_gestures, self.number_of_time_stamps)

        for i in range(self.number_of_gestures):
            time_stamp = self.time_stamps[i]
            gesture = self.gestures[i]
            correct_name = correct_names[i]
            new_filename = pre_processing.rename_data_file(time_stamp, gesture, "orientationEuler", path_to_file=self.path_to_test_data)

            self.assertEqual(new_filename, correct_name)


class RenameDataFiles(unittest.TestCase):
    """
    Run a series of tests to evaluate the logic of rename_data_files()
    """
    def setUp(self):
        """
        Define a series of variables common to the tests for generate_order_of_gestures()
        :return: The correct file names which the function should return, the time stamps used in this test, the
        gestures used in these tests and the absolute path to the data used in these tests
        """
        self. correct_filenames = ['o-accelerometer-1501622034.csv',
                                   'j-accelerometer-1501622042.csv',
                                   'p-accelerometer-1501622055.csv',
                                   'r-accelerometer-1501622064.csv',
                                   'b-accelerometer-1501622072.csv',
                                   'c-accelerometer-1501622079.csv',
                                   'q-accelerometer-1501622086.csv',
                                   'd-accelerometer-1501622095.csv',
                                   'v-accelerometer-1501622101.csv',
                                   'r-accelerometer-1501622109.csv',
                                   'o-emg-1501622034.csv',
                                   'j-emg-1501622042.csv',
                                   'p-emg-1501622055.csv',
                                   'r-emg-1501622064.csv',
                                   'b-emg-1501622072.csv',
                                   'c-emg-1501622079.csv',
                                   'q-emg-1501622086.csv',
                                   'd-emg-1501622095.csv',
                                   'v-emg-1501622101.csv',
                                   'r-emg-1501622109.csv',
                                   'o-gyro-1501622034.csv',
                                   'j-gyro-1501622042.csv',
                                   'p-gyro-1501622055.csv',
                                   'r-gyro-1501622064.csv',
                                   'b-gyro-1501622072.csv',
                                   'c-gyro-1501622079.csv',
                                   'q-gyro-1501622086.csv',
                                   'd-gyro-1501622095.csv',
                                   'v-gyro-1501622101.csv',
                                   'r-gyro-1501622109.csv',
                                   'o-orientation-1501622034.csv',
                                   'j-orientation-1501622042.csv',
                                   'p-orientation-1501622055.csv',
                                   'r-orientation-1501622064.csv',
                                   'b-orientation-1501622072.csv',
                                   'c-orientation-1501622079.csv',
                                   'q-orientation-1501622086.csv',
                                   'd-orientation-1501622095.csv',
                                   'v-orientation-1501622101.csv',
                                   'r-orientation-1501622109.csv',
                                   'o-orientationEuler-1501622034.csv',
                                   'j-orientationEuler-1501622042.csv',
                                   'p-orientationEuler-1501622055.csv',
                                   'r-orientationEuler-1501622064.csv',
                                   'b-orientationEuler-1501622072.csv',
                                   'c-orientationEuler-1501622079.csv',
                                   'q-orientationEuler-1501622086.csv',
                                   'd-orientationEuler-1501622095.csv',
                                   'v-orientationEuler-1501622101.csv',
                                   'r-orientationEuler-1501622109.csv']

        self.time_stamps = ['1501622034', '1501622042', '1501622055', '1501622064', '1501622072',
                            '1501622079', '1501622086', '1501622095', '1501622101', '1501622109']
        self.gestures = ['o', 'j', 'p', 'r', 'b', 'c', 'q', 'd', 'v', 'r']
        self.path_to_test_data = os.path.abspath("test_data/myo_data/")

    def tearDown(self):
        """
        Restore the test environment to it's original state
        :return: The original names of the data files used in the test
        """
        for file in os.listdir(self.path_to_test_data):
            directory_levels = file.split("/")
            directory_levels[-1] = directory_levels[-1][2:]
            old_filename = "/".join(directory_levels)
            os.rename(file, old_filename)

    def test_renames_all_relevant_files(self):
        """
        Evaluate whether rename_data_files() produces the correct file names
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        self.assertEqual(self.correct_filenames, pre_processing.rename_data_files(time_stamps=self.time_stamps,
                                                                                  order_of_gestures=self.gestures,
                                                                                  path_to_file=self.path_to_test_data))


# class CondenseData(unittest.TestCase):


class GetPerformanceTimeStamps(unittest.TestCase):
    """
    Run a series of tests to evaluate the logic of get_performance_time_stamps()
    """
    def setUp(self):
        """
        Define a series of variables common to the tests for get_performance_time_stamps()
        :return: The absolute path to the data used in these tests
        """
        self.path_to_test_data = os.path.abspath("test_data/gesture_orders")

    def test_return_all_time_stamps(self):
        """
        Evaluate whether get_performance_time_stamps() returns all the time stamps for the gestures performed.
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        all_time_stamps = ['1501622034', '1501622042', '1501622055', '1501622064', '1501622072', '1501622079',
                           '1501622086', '1501622095', '1501622101', '1501622109']

        self.assertEqual(pre_processing.get_performance_time_stamps(self.path_to_test_data), all_time_stamps)

    def test_appropriate_number_of_time_stamps(self):
        """
        Evaluate whether get_performance_time_stamps() returns time stamps for all the gestures performed
        :return: A boolean expressing whether or not the test has passed. True indicates the test has passed,
        False that it has failed.
        """
        appropriate_number_of_time_stamps = len(os.listdir(self.path_to_test_data))/5

        self.assertEqual(len(pre_processing.get_performance_time_stamps(self.path_to_test_data)),
                         appropriate_number_of_time_stamps)


# class GenerateGestureData(unittest.TestCase):


if __name__ == "__main__":
    unittest.main()
