import sys, os
from config import leap_lib, more_leap
sys.path.insert(0, leap_lib)
sys.path.insert(0, more_leap)
import Leap, ctypes, itertools
import matplotlib.pyplot as plt
import numpy as np


def read_frame(filename):

    Leap.Controller()
    new_frame = Leap.Frame()
    with open(os.path.realpath(filename), 'rb') as data_file:
        data = data_file.read()

    leap_byte_array = Leap.byte_array(len(data))
    address = leap_byte_array.cast().__long__()
    ctypes.memmove(address, data, len(data))
    new_frame.deserialize((leap_byte_array, len(data)))
    return new_frame


valid_features = ('center', 'next_joint', 'prev_joint', 'hands', 'fingers', 'arm', 'basis', 'x_basis', 'y_basis', 'origin', 'z_basis', 'x', 'y', 'z', 'pitch', 'roll', 'yaw', 'confidence', 'direction', 'grab_strength', 'palm_normal', 'palm_position', 'palm_velocity', 'pinch_strength', 'sphere_center', 'sphere_radius', 'stabilized_palm_position', 'stabilized_tip_position', 'tip_position', 'tip_velocity', 'wrist_position')


def flatten_old(obj):
    l = [val for val in dir(obj) if val in valid_features]
    for el in l:
        for sub in flatten(getattr(obj, el)):
            yield sub
    if isinstance(obj, float):
        yield obj

def flatten(tup):
    obj = tup[0]
    name = tup[1]
    l = [val for val in dir(obj) if val in valid_features]
    for el in l:
        for sub in flatten((getattr(obj, el), name+"_"+el)):
            yield sub
    if isinstance(obj, float):
        yield tup

def get_features(hand, labels=False):
    hand_tup = (hand, 'hand')
    features = itertools.chain(flatten(hand_tup), get_normalised_fingers_features(hand))
    return features if labels else zip(*features)[0]

    
def get_hand_features(hand, labels=False):
    hand = (hand, 'hand')
    features = flatten(hand)
    return features if labels else zip(*features)[0]


def get_finger_features(hand, labels=False):
    features = get_normalised_fingers_features(hand)
    return features if labels else zip(*features)[0]

def get_normalised_fingers_features(hand):
    hand_x_basis = hand.basis.x_basis
    hand_y_basis = hand.basis.y_basis
    hand_z_basis = hand.basis.z_basis
    hand_origin = hand.palm_position
    hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
    hand_transform = hand_transform.rigid_inverse()

    trans_wrist = (hand_transform.transform_point(hand.wrist_position), 'hand_wrist_position_transformed')
    trans_sphere = (hand_transform.transform_point(hand.sphere_center), 'hand_sphere_center_transformed') 
    

    features = itertools.chain(flatten(trans_wrist), flatten(trans_sphere))
    # force some sort of order for ML
    for finger in hand.fingers:
        if finger.type == 0:
            thumb = process_finger(finger, hand_transform)
        elif finger.type == 1:
            index = process_finger(finger, hand_transform)
        elif finger.type == 2:
            middle = process_finger(finger, hand_transform)
        elif finger.type == 3:
            ring = process_finger(finger, hand_transform)
        elif finger.type == 4:
            pinky = process_finger(finger, hand_transform)

    features = itertools.chain(features, thumb, index, middle, ring, pinky)

    return features


def process_finger(finger, hand_transform):
        # flatten finger with pointable features
        name = 'hand_finger_' + str(finger.type)
        features = flatten((finger, name))
        for i in range(4):
            features = itertools.chain(features, process_bone(finger.bone(i), hand_transform, name))

        transformed_position = (hand_transform.transform_point(finger.tip_position), name + '_tip_position_transformed')
        trans_stab_tip = (hand_transform.transform_point(finger.stabilized_tip_position), name + '_stabilized_tip_position_transformed')
        features = itertools.chain(features, flatten(transformed_position), flatten(trans_stab_tip))
        
        return features

def process_bone(bone, hand_transform, finger_name):
    name = finger_name + '_bone_' + str(bone.type)
    features = flatten((bone, name))
    transformed_prev = (hand_transform.transform_point(bone.prev_joint), name + '_prev_joint_transformed')
    transformed_next = (hand_transform.transform_point(bone.next_joint), name + '_next_joint_transformed')
    features = itertools.chain(features, flatten(transformed_prev), flatten(transformed_next))
    return features

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

