import csv
import sys

import myo as libmyo

libmyo.init()

feed = libmyo.device_listener.Feed()
hub = libmyo.Hub()
hub.run(1000, feed)
try:
    myo = feed.wait_for_single_device(timeout=10.0)  # seconds
    if not myo:
        print("No Myo connected after 10 seconds.")
        sys.exit()

    while hub.running and myo.connected:
        quat = myo.orientation
        with open('myo_data.csv', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(quat.x, quat.y, quat.z, quat.w)
except KeyboardInterrupt:
    print("Quitting...")
finally:
    hub.shutdown()