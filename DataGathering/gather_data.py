import os
import sys
import time

participant_number = sys.argv[1]
round_number = sys.argv[2]

with open('./orders/' + str(participant_number) + "-" + str(round_number) + ".txt") as order_of_gestures:
    gestures = list(order_of_gestures.read().replace(',', ''))
    print gestures
    for gesture in gestures:
        os.system("START .\\Myo\\MyoDataCapture")
        print "Myo data gatherer is running"
        os.system("START .\\Kinect\\kinectv2_viewer(updatedv2) " + gesture)
        print "Kinect data gatherer is running"
        os.system("START .\\Leap\\Sample.py Leap_" + gesture)
        print "Leap data gatherer is running"

        time.sleep(3)

        os.system("TASKKILL /IM MyoDataCapture.exe")
        os.system("TASKKILL /IM kinectv2_viewer(updatedv2).exe ")
        os.system("TASKKILL /IM Sample.exe")
        time.sleep(1)
