import csv
import sys

from myo.myo import init, Hub, Feed, vector

init()

feed = Feed()
hub = Hub()
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
        vector_str = vector.Vector
        # file name is participant_number_gesture_number_myo_data.csv
        file_name = participant_number + '_' + str(gesture_num) + '_myo_data.csv'

        while True:
            keypress = input()
            with open(file_name, "w+", newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                string = str(quaternion_str.x)+','+str(quaternion_str.y)+','+str(quaternion_str.z)+','+str(quaternion_str.w)
                spamwriter.writerow(string)#, vector_str.x, vector_str.y, vector_str.z
            if keypress == 'q':
                break
        gesture_num += 1
        print('Broke out of inner loop')

except KeyboardInterrupt:
    print("Quitting...")

finally:
    hub.shutdown()
