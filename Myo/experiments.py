import random

from data_processing import read_data

def extra_trees_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def randomforests_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def voting_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def hmm_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def ann_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def knn_experiments(data):
    try:
        return 0
    except Exception:
        return 1


def run_experiments():
    test_participants = [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                         34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48]
    participant = test_participants[random.randint(0, len(test_participants) - 1)]
    data = read_data.get_data(hmm=False, test_participant=participant)
    knn_experiments(data)
    ann_experiments(data)
    voting_experiments(data)
    randomforests_experiments(data)
    extra_trees_experiments(data)
    return 0
