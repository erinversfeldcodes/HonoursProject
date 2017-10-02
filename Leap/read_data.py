import glob, pickle, os
from itertools import chain


def read_data(path, frames_per_gesture=1, separate_frames=False, feature_set_type="all", average=False):
    gesture_names = []
    gesture_data = []
    if average:
        separate_frames = False

    for foldername in sorted(glob.glob(os.path.join(path, "Leap_*"))):
        
        
        gesture = process_gesture_folder(foldername, frames_per_gesture, separate_frames, feature_set_type, average)

        # only consider a gesture if correct number of frames/features            
        if gesture:
            letter = foldername[len(path)+6]
            
            # gesture_data is a list of lists
            # gesture_names is a list of letters
            if separate_frames:
                # gesture is a list of lists
                gesture_data.extend(gesture)
                gesture_names.extend([letter] * len(gesture))
            else:
                # gesture is a list of floats
                gesture_data.append(gesture)
                gesture_names.append(letter)
                
    return gesture_data, gesture_names


def process_gesture_folder(foldername, frames_per_gesture, separate_frames, feature_set_type, average):
        gesture = []
        
        with open(os.path.join(foldername, feature_set_type + ".ordered_frames"), 'rb') as fp:
            gesture = pickle.load(fp)
        frame_num = float(len(gesture))
        if average:
             return [sum(x)/frame_num for x in zip(*gesture)]
        if frame_num < frames_per_gesture:
            return []
        if separate_frames:
            return gesture[:frames_per_gesture]
        else:
            return list(chain.from_iterable(gesture[:frames_per_gesture]))
        

def get_feature_names(path, feature_set_type):
    with open(os.path.join(path, feature_set_type + ".feature_names"), 'rb') as fp:
        return pickle.load(fp)

def load_selected_features():
    with open(os.path.join("50features.txt"), 'rb') as fp:
        return pickle.load(fp)
    