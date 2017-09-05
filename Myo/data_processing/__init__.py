# import os
#
# def get_participant_order():
#     dirs = os.listdir("H:\\data\\Participant 21\\Kinect")
#     gesture_time = []
#
#     for dir_name in dirs:
#         gesture_time_pair = (dir_name[0], dir_name[-6:])
#         gesture_time.append(gesture_time_pair)
#
#     gesture_time = sorted(gesture_time, key=lambda x: x[1])
#
#     participant_order = []
#
#     for gesture_time_pair in gesture_time:
#         participant_order.append(gesture_time_pair[0])
#
#     return participant_order
#
# if __name__ == "__main__":
#     order = get_participant_order()
#
#     time_stamps = []
#     files = os.listdir("H:\\data\\Participant 21\\Myo")
#
#     for file in files:
#         time_stamps.append(file[-14:-4])
#
#     time_stamps = sorted(list(set(time_stamps)))
#     gesture_time_stamp_pairs = list(zip(order, time_stamps))
#
#     for pair in gesture_time_stamp_pairs:
#         gesture = pair[0]
#         time_stamp = pair[1]
#
#         for file in files:
#             if time_stamp in file:
#                 path = "H:\\data\\Participant 21\\Myo"
#                 file_name = os.path.basename(file)#[5:]
#                 new_file_name = str(gesture) + "-" + str(file_name)
#                 os.rename(os.path.join(path, file), os.path.join(path, new_file_name))
#
#     renamed_files = os.listdir("H:\\data\\Participant 21\\Myo")

