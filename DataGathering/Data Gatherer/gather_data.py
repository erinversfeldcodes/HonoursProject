import logging
import os
import subprocess
import sys
import tkinter
from tkinter import *
import time

time_stamp = time.time()
logging.basicConfig(filename="./log/" + (str(time_stamp) + ".log"), level=logging.DEBUG)
logging.info("Loaded gather_data.py")


class DataGatheringApplication(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("SASL gesture recording")

        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.gestures = []
        self.frames = {}

        frame = ParticipantInfoFrame(parent=self.container, controller=self)
        self.frames[ParticipantInfoFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ParticipantInfoFrame)

    def show_frame(self, F):
        if F == DataRecordingFrame:
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[F]
        frame.tkraise()

    def set_gestures(self, gestures):
        self.gestures = gestures
        logging.debug("Set gestures to: "+ str(self.gestures))

    def get_gestures(self):
        logging.debug("Returning gestures to: " + str(self.gestures))
        return self.gestures


class ParticipantInfoFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2)
        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1)

        participant_label = Label(self, text="Please enter your participant number: ")
        participant_label.grid(row=0, column=0)
        self.participant_entry = Entry(self, bd=5)
        self.participant_entry.grid(row=0, column=1)

        round_label = Label(self, text="Please enter the round number: ")
        round_label.grid(row=1, column=0)
        self.round_entry = Entry(self, bd=5)
        self.round_entry.grid(row=1, column=1)

        self.done_button = Button(self, text="Submit", command=self.load_data)
        self.done_button.grid(row=2, column=1)

    def load_data(self):
        participant_number = self.participant_entry.get()
        logging.debug("Partiticpant number set to: " + str(participant_number))
        round_number = self.round_entry.get()
        logging.debug("Round number set to: " + str(round_number))

        try:
            logging.debug("Trying to open file containing order of gestures to be performed.")
            with open('./orders/' + str(participant_number) + '-' + str(round_number) + '.txt') as order_of_gestures:
                logging.debug("Able to open file containing the gestures to be performed.")
                self.done_button.destroy()

                confirm_label = Label(self, text="Thank you! Please click 'Next' to proceed.")
                confirm_label.grid(row=2, column=0)

                next_button = Button(self, text="Next", command=lambda: self.controller.show_frame(DataRecordingFrame))
                next_button.grid(row=2, column=1)

                gestures = list(order_of_gestures.read().replace(',', ''))
                self.controller.set_gestures(gestures)

        except FileNotFoundError:
            logging.debug("Unable to open file containing order of gestures to be performed.")
            error_msg = Label(self, text="Please enter the correct participant and round number.")
            error_msg.grid(row=2, column=0)


class DataRecordingFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.gestures = self.controller.get_gestures()
        self.gesture_images = self.get_gesture_image_paths()
        self.image_iterator = iter(self.gesture_images)
        self.current_gesture = None

        msg_label = Label(self, text="Please perform the gesture shown in the image. Click 'Start recording' to begin "
                                     "recording the gesture: ")
        msg_label.pack(side=TOP, anchor=W, fill=X, expand=YES)

        self.image_label = Label(self)
        self.image_label.pack()

        Label(self).pack(side=LEFT)

        start_recording = Button(self, text="Start recording", command=self.start_recording)
        start_recording.pack()

        self.next_gesture()

    def get_gesture_image_paths(self):
        paths = []

        for gesture in self.gestures:
            image_name = ".\\images\\" + gesture + ".gif"
            image_path = os.path.abspath(image_name)
            paths.append(image_path)

        logging.info("Paths to images of gestures: " + str(paths))
        return paths

    def next_gesture(self):
        try:
            path_to_image = next(self.image_iterator)
            self.current_gesture = path_to_image[-5]
            logging.debug("Current gesture set to: " + str(path_to_image))
            gesture_image = PhotoImage(file=path_to_image)
            self.image_label.img = gesture_image
            self.image_label.config(image=self.image_label.img)

        except StopIteration:
            logging.info("Readhed the end of the list of gestures to be performed. Exiting.")
            sys.exit()

    def start_recording(self):
        os.system("START ..\\Myo\\MyoDataCapture")
        print("Myo data gatherer is running")

        os.system("START ..\\Kinect\\kinectv2_viewer(updatedv3) " + self.current_gesture)
        logging.info("Kinect data gatherer is running with gesture: " +str(self.current_gesture))
        print("Kinect data gatherer is running")

        os.system("START /IM py -2 ..\\Leap\\Sample.py " + self.current_gesture)
        print("Leap data gatherer is running")

        time.sleep(3)

        os.system("TASKKILL /IM MyoDataCapture.exe")
        os.system("TASKKILL /IM kinectv2_viewer(updatedv3).exe ")
        logging.info("Kinect data gatherer has been killed.")
        os.system("TASKKILL /IM py.exe")
        time.sleep(1)

        self.next_gesture()


if __name__ == "__main__":
    app = DataGatheringApplication()
    logging.debug("Created instance of DataGatheringApplication(): "+str(app))
    app.mainloop()
