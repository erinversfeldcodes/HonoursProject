import csv
import sys

import myo.myo as libmyo

libmyo.init()

feed = libmyo.device_listener.Feed()
hub = libmyo.Hub()
hub.run(1000, feed)
try:
    myo = feed.wait_for_single_device(timeout=10.0)  # seconds
    if not myo:
        print("No Myo connected after 10 seconds.")
        sys.exit()

    gesture_num = 0
    participant_number = input("Participant_number: ")

    while hub.running and myo.connected:
        quaternion_str = myo.orientation
        # file name is participant_number_gesture_number_myo_data.csv
        file_name = participant_number + '_' + gesture_num + '_myo_data.csv'

        while input() != '\n':
            with open(file_name, newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(quaternion_str.x, quaternion_str.y, quaternion_str.z, quaternion_str.w)

except KeyboardInterrupt:
    print("Quitting...")
finally:
    hub.shutdown()
