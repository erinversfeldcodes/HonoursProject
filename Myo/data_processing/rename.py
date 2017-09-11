import os

participant_folder = "C:\\Users\\Erin\\Code\\HonoursProject\\Myo\\data\\Participant *\\"

def get_participant_order(main_folder):
    kinect_folder = os.path.join(main_folder, "Kinect")
    dirs = os.listdir(kinect_folder)
    gesture_time = []

    for dir_name in dirs:
        gesture_time_pair = (dir_name[0], dir_name[-6:])
        gesture_time.append(gesture_time_pair)

    gesture_time = sorted(gesture_time, key=lambda x: x[1])

    participant_order = []

    for gesture_time_pair in gesture_time:
        participant_order.append(gesture_time_pair[0])

    return participant_order


def rename_files(folder):
    order = get_participant_order(folder)

    time_stamps = []
    myo_folder = os.path.join(folder, "Myo")
    files = os.listdir(myo_folder)

    for file in files:
        time_stamps.append(file[-14:-4])

    time_stamps = sorted(list(set(time_stamps)))
    gesture_time_stamp_pairs = list(zip(order, time_stamps))

    for pair in gesture_time_stamp_pairs:
        gesture = pair[0]
        time_stamp = pair[1]

        for file in files:
            if time_stamp in file:
                file_name = os.path.basename(file)
                new_file_name = str(gesture) + "-" + str(file_name)
                os.rename(os.path.join(myo_folder, file), os.path.join(myo_folder, new_file_name))

    renamed_files = os.listdir(myo_folder)


def generate_db_stats():
    pass


if __name__ == "__main__":
    participant_numbers = []

    for p_num in participant_numbers:
        folder = participant_folder.replace("*", str(p_num))
        rename_files(folder)

    generate_db_stats()

#
