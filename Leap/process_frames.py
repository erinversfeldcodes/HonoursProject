# -*- coding: utf-8 -*-
import utils, pickle, glob, os
from operator import itemgetter

def process_frame(frame, feature_set_type='all', labels=False):
    if len(frame.hands) != 1:
        return []
    if feature_set_type == 'all':
        return utils.get_features(frame.hands[0], labels=labels)    
    if feature_set_type == 'fingers_only':
        return utils.get_finger_features(frame.hands[0], labels=labels)
    if feature_set_type == 'hands_only':
        return utils.get_hand_features(frame.hands[0], labels=labels)


def rewrite(path, feature_set_type):
    feature_names = []
    get_labels = True
    for gesture_count, foldername in enumerate(sorted(glob.glob(os.path.join(path, "Leap_*")))):
        print(foldername)
        frames = []
        for count, filename in enumerate(glob.glob(os.path.join(foldername, "*.data"))):
            if count%5 != 0:
                continue

            frame_features = process_frame(utils.read_frame(filename), feature_set_type, labels=get_labels)
            if frame_features:
                if get_labels:
                    print("getting feature names")
                    frame_features = zip(*frame_features)
                    feature_names = frame_features[1]
                    frame_features = frame_features[0]
                    with open(os.path.join(path, feature_set_type + ".feature_names"), 'wb') as fp:
                        print(os.path.join(path, feature_set_type + ".feature_names"))
                        pickle.dump([x for x in feature_names], fp)
                        print("written")
                        get_labels = False
                        
                frames.append(frame_features)
#                with open(filename[:-5] + '_' + feature_set_type + ".features", 'wb') as fp:
#                    pickle.dump([x for x in frame_features], fp)
                    
        confidence_index = feature_names.index("hand_confidence")            
        frames = sorted(frames, key=itemgetter(confidence_index), reverse=True)
        with open(os.path.join(foldername, feature_set_type + ".ordered_frames"), 'wb') as fp:
            pickle.dump(frames, fp)        
                    
            
def rewrite_all():
    paths = [os.path.join("Leap_Data", "Legit_Data", "Participant " + str(x), "Leap") for x in range(12, 50)]
    paths = [os.path.join("Leap_Data", "Legit_Data", "Participant 0", "Leap")]

#    feature_set_types = ['fingers_only', 'hands_only', 'all']
    feature_set_types = ['all']
    for path in paths:
        for feature_set_type in feature_set_types:
            print("rewriting in " + path + " for feature_set_type " + feature_set_type )
            rewrite(path, feature_set_type)


if __name__=="__main__":
    rewrite_all()

