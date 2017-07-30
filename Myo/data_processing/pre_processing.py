import os

def generate_order_of_gestures():
    #construct ordered list of ge`stures
    gestures = []
    for participant_number in range(0, 50):
        for round_number in range(0, 26):
            filename = participant_number+"-"+round_number+".txt"
            with open("./data/"+filename) as data_file:
                while True:
                    current_char = file.read(1)
                    if current_char == ",":
                        pass
                    else:
                        gestures.append(current_char)
    return gestures

def rename_accelerometer_data_files(gesture):
    regex = ''
    for accelerometer_data_file in data:
        os.rename(accelerometer_data_file, str(gesture)+"-"+str(accelerometer_data_file))

def rename_orientation_data_files(gesture):
    regex = ''
    for orientation_data_file in data:
        os.rename(orientation_data_file, str(gesture)+"-"+str(orientation_data_file))

def rename_orientation_euler_data_files(gesture):
    regex = ''
    for orientation_euler_data_file in data:
        os.rename(orientation_euler_data_file, str(gesture)+"-"+str(orientation_euler_data_file))

def rename_emg_data_files(gesture):
    regex = ''
    for emg_data_file in data:
        os.rename(emg_data_file, str(gesture)+"-"+str(emg_data_file))

def rename_gyro_data_files(gesture):
    regex = ''
    for gyro_data_file in data:
        os.rename(gyro_data_file, str(gesture)+"-"+str(gyro_data_file))

def rename_data_files(order_of_gestures):
    for gesture in order_of_gestures:
        rename_accelerometer_data_files(gesture)
        rename_orientation_data_files(gesture)
        rename_orientation_euler_data_files(gesture)
        rename_emg_data_files(gesture)
        rename_gyro_data_files(gesture)

def condense_accelerometer_data():

def condense_orientation_data():

def condense_orientation_euler_data():

def condense_emg_data():

def condense_gyro_data():

def generate_gesture_data():