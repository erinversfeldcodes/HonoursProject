import os
import subprocess
import sys
import time

try:
    participant_number = sys.argv[1]
    round_number = sys.argv[2]
except Exception:
    user_input = input("Please supply your participant number as well as the round number, space separated:\n")
    user_input_list = user_input.split(" ")
    participant_number = int(user_input_list[0])
    round_number = int(user_input_list[1])


with open('./orders/' + str(participant_number) + "-" + str(round_number) + ".txt") as order_of_gestures:
    gestures = list(order_of_gestures.read().replace(',', ''))
    print(gestures)
    for gesture in gestures:

        os.system("START .\\Myo\\MyoDataCapture")
        print("Myo data gatherer is running")

        os.system("START .\\Kinect\\kinectv2_viewer(updatedv2) " + gesture)
        print("Kinect data gatherer is running")

        path_to_data_gatherer_script = os.path.abspath("Leap\\Sample.py")
        os.system("leap_script.batch "+gesture)
        print("Leap data gatherer is running")

        time.sleep(3)

        os.system("TASKKILL /IM MyoDataCapture.exe")
        os.system("TASKKILL /IM kinectv2_viewer(updatedv2).exe ")
        time.sleep(1)
