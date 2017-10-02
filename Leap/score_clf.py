from sklearn import svm, neighbors, tree, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.feature_selection import SelectKBest, VarianceThreshold, RFE, SelectFromModel, mutual_info_classif
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import VotingClassifier, ExtraTreesClassifier, RandomForestClassifier
import os, string, time, logging, pickle
from read_data import read_data, get_feature_names, load_selected_features
import numpy as np


log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
filename = "experiment_" + str(time.time()) + ".txt"
path_to_logs = os.path.abspath("logs/")
path_to_log_file = os.path.join(path_to_logs, filename)
fh = logging.FileHandler(path_to_log_file)
fh.setLevel(logging.DEBUG)
log.addHandler(fh)


def select_features(training_data, training_target, test_data, feature_labels, fresh=False):
    """Perform preprocessing and feature selection

    Parameters
    ----------
    training_data : list
        The training data to be transformed
    training_target : list
        The labels for the training data to be transformed
    test_data : list
        The test data to be transformed
    feature_labels : list
        The names of the features defining a data point
    fresh : boolean
        Recalculate feature selection or not, optional
    """

    training_data, test_data, feature_labels = remove_0_var(training_data, training_target, test_data, feature_labels)
    training_data, test_data = scale(training_data, test_data)
    
    if fresh:
        selector = SelectKBest(k=500)
        training_data = selector.fit_transform(training_data, training_target)
        test_data = selector.transform(test_data)
        feature_labels = selector.transform(feature_labels)
        log.info(selector)

        selector = RFE(ExtraTreesClassifier(), n_features_to_select=50)
        training_data = selector.fit_transform(training_data, training_target)
        test_data = selector.transform(test_data)
        feature_labels = selector.transform(feature_labels)
        log.info(selector)

    else:
        loaded_labels = list(load_selected_features())
        feature_indeces = [x for x, feature in enumerate(feature_labels[0]) if feature in loaded_labels]
        feature_labels = [[each_list[i] for i in feature_indeces] for each_list in feature_labels]
        training_data = [[each_list[i] for i in feature_indeces] for each_list in training_data]
        test_data = [[each_list[i] for i in feature_indeces] for each_list in test_data]

        selector = SelectKBest(k=50, score_func=mutual_info_classif)
        training_data = selector.fit_transform(training_data, training_target)
        test_data = selector.transform(test_data)
        feature_labels = selector.transform(feature_labels)
        log.info("last run features")
        log.info(selector)

    log.info("number of features: {}".format(len(training_data[0])))
    print("number of features: {}".format(len(training_data[0])))
    log.info("features selected: {}".format(feature_labels[0]))

    
    return training_data, test_data, feature_labels

    

def optimize_params(clf, params, training_data, training_target):
    """Run grid search on given classifier 

    Parameters
    ----------
    clf : sklearn classifier
        The classifier to tune
    params : dict
        The possible parameters and their values
    training_data : list
        The training data for the classifier
    training_target : list
        The labels of the training data
    """
    
    try:
        rand_scv = RandomizedSearchCV(clf, params, n_iter=40, n_jobs=-1)
        return rand_scv.fit(training_data, training_target)
    except ValueError:
        rand_scv = GridSearchCV(clf, params)
        return rand_scv.fit(training_data, training_target)
        

def test_clf(name, clf, test_data, test_target, results):
    """Test and record classifier performance 

    Parameters
    ----------
    name : string
        The name of the classifier
    clf : sklearn classifier
        The trained classifier to test
    test_data : list
        The data used to test the classifier
    test_target : list
        The correct labels of the training data
    results : dict
        The results of the curernt execution
    """
    
    gesture_pred = clf.predict(test_data)
    target_names = list(string.ascii_lowercase)
    accuracy = accuracy_score(test_target, gesture_pred)
    precision = precision_score(test_target, gesture_pred, average='weighted')
    recall = recall_score(test_target, gesture_pred, average='weighted')
    results[name] = {}
    results[name]['accuracy'] = accuracy
    results[name]['precision'] = precision
    results[name]['recall'] = recall
    
    print "CLASSIFIER: {} {}".format(name, accuracy)
    log.info("CLASSIFIER: {} {}".format(name, accuracy))

    report = classification_report(test_target, gesture_pred, target_names=target_names)
    cm = confusion_matrix(test_target, gesture_pred, target_names)
    log.info(report)
    log.info(cm)

def remove_0_var(training_data, training_target, test_data, feature_labels):
    """Remove features that do not vary across data points

    Parameters
    ----------
    training_data : list
        The training data to be transformed
    training_target : list
        The labels of the training data
    test_data : list
        The test data to be transformed
    feature_labels : list
        The names of the features defining a data point
    """
    selector = VarianceThreshold()
    training_data = selector.fit_transform(training_data, training_target)
    test_data = selector.transform(test_data)
    feature_labels = selector.transform(feature_labels)
    return training_data, test_data, feature_labels

def scale(training_data, test_data):
    """Scale data

    Parameters
    ----------
    training_data : list
        The training data to be transformed
    test_data : list
        The test data to be transformed
    """
    log.info("scaling")
    training_data = preprocessing.scale(training_data)
    test_data = preprocessing.scale(test_data)
    return training_data, test_data


def remove_low_confidence(confidence, data, target, feature_labels):
    """Remove data points with low confidence

    Parameters
    ----------
    confidence : float 
        Minimum confidence value
    data : list
        The data to be transformed
    target : list
        The labels for the data to be transformed
    feature_labels : list
        The names of the features defining a data point
    """
    confidence_index = feature_labels.index("hand_confidence")
    for i, gesture in enumerate(data):
        if gesture[confidence_index] <= confidence:
            del data[i]
            del target[i]
    


def load_paths(paths, fresh, frames_per_gesture, separate_frames, feature_set_type):
    """Load data from given paths

    Parameters
    ----------
    paths : list
        The paths to the data: every path leads to the Leap subfolder of a participant folder
    fresh : boolean
        Recalculate aggregate of frames
    frames_per_gesture : int
        The number of frames considered to define a gesture
    separate_frames : boolean
        Treat every frame as a separate data point [not recommended]
    feature_set_type : string
        'hands_only', 'fingers_only', 'all'
    """
    all_data = []
    all_target = []
    for path in paths:
        if fresh:
            data, target = read_data(path, frames_per_gesture, separate_frames, feature_set_type)
            try:
                with open(path[:-4] + "Participant_fpg_{}.data".format(frames_per_gesture), 'wb') as fp:
                    pickle.dump((data, target), fp)
            except IOError:
                continue
        else:
            try:
                with open(path[:-4] + "Participant_fpg_{}.data".format(frames_per_gesture), 'rb') as fp:
                    data, target = pickle.load(fp)
            except IOError:
                continue
        all_data.extend(data)
        all_target.extend(target)
    return all_data, all_target

def get_train_test_split(frames_per_gesture, separate_frames, fresh=False, feature_set_type="all", train_paths=[], test_paths=[], use_auto_split=False, average=False):
    """Split given paths into sklearn appropriate train and test lists

    Parameters
    ----------
    frames_per_gesture : int
        The number of frames considered to define a gesture
    separate_frames : boolean
        Treat every frame as a separate data point [not recommended]
    fresh : boolean
        Recalculate aggregate of frames
    feature_set_type : string
        `hands_only`, `fingers_only`, `all`
   train_paths : list
        The paths to the training data, optional
   test_paths : list
        The paths to the testing data, optional
    use_auto_split : boolean
        Split data randomly, optional
    average : boolean
        Take average of all frames in a gesture, optional
    """
    
    log.info('Data variables: \n'
            '\t train_paths: {}, \n'
            '\t test_paths: {}, \n'
            '\t use_auto_split: {}, \n'
            '\t frames_per_gesture: {}, \n'
            '\t separate_frames: {}, \n'
            '\t feature_set_type: {} \n'
            '\t average: {}'
            .format(train_paths, 
                    test_paths, 
                    use_auto_split, 
                    frames_per_gesture, 
                    separate_frames, 
                    feature_set_type,
                    average))

    training_data, training_target = load_paths(train_paths, fresh, frames_per_gesture, separate_frames, feature_set_type)
    test_data, test_target = load_paths(test_paths, fresh, frames_per_gesture, separate_frames, feature_set_type)

    if use_auto_split:
        data = test_data + training_data
        target = test_target + training_target
        training_data, test_data, training_target, test_target = train_test_split(data, target, test_size=0.25, random_state=0)

    return training_data, test_data, training_target, test_target

    
def run_experiment(test_participant, valid_participants, fpg=1, quick_test=False, fresh_paths=True, fresh_labels=True):
    """Run the experiment for one participan

    Parameters
    ----------
    test_participant : int
        The participant number selected as the test set
    valid_participants : list
        All valid participant numbers
    fpg : int
        The number of frames considered to define a gesture
    quick_test : boolean
        Use only test_participant's data
    fresh_paths : boolean
        Recalculate aggregate of frames
    fresh_labels : boolean
        Recalculate features to be selected
    """

    results = {}    
    
    train_paths = [os.path.join("Leap_Data", "Legit_Data", "Participant " + str(x), "Leap") for x in valid_participants]
    test_paths = [os.path.join("Leap_Data", "Legit_Data", "Participant " + str(test_participant), "Leap")]
    train_paths.remove(test_paths[0])

    start = time.clock()
    training_data, test_data, training_target, test_target = get_train_test_split(
            train_paths= [] if quick_test else train_paths, 
            test_paths=test_paths, 
            use_auto_split=quick_test, 
            frames_per_gesture=fpg, 
            separate_frames=False, 
            feature_set_type='all',
            average=False,
            fresh=fresh_paths,
        )
    end = time.clock()
    log.info("loading data took {} seconds".format(end - start))
    log.info("loaded top {} confidence frames...".format(fpg))

    
    all_feature_labels = get_feature_names(test_paths[0], 'all') * fpg

    print len(training_data[0])
    print len(all_feature_labels)
    start = time.clock()
    training_data, test_data, feature_labels = select_features(training_data, training_target, test_data, [all_feature_labels], fresh=fresh_labels)
    end = time.clock()
    log.info("feature selection took {} seconds".format(end - start))



    lower_c = [2**(x) for x in range(-5, 7)]
    gamma_range = [2**(x) for x in range(-15, 3)] + ['auto']
    
    svm_params = {  'gamma': gamma_range, 
                    'C': lower_c,}
                  
    neighbor_range = range(1,50) 
    p_range = range(1,3)
    knn_params = {'n_neighbors': neighbor_range, 
                    'p': p_range,}
                    
                
    
    if 26 > len(training_data[0]):
        nodes_per_layer_range = range(len(training_data[0]), 27, 1)
    else:
        nodes_per_layer_range = range(26, len(training_data[0])+1, 1)
        
        
    nodes_per_layer_range = range(30, 200, 5)
    alpha_range = np.logspace(-5, 3, 5)
    learning_rate_init_range = [10**x for x in range(-6,1)] 
    mlp_params = {
                    'hidden_layer_sizes': [(x,) for x in nodes_per_layer_range],
                    'activation': ('identity', 'logistic', 'tanh', 'relu'),
                    'learning_rate_init': learning_rate_init_range,
                    'alpha': alpha_range,
                    'solver': ['lbfgs', 'sgd', 'adam'],
                    'learning_rate': ['constant', 'invscaling', 'adaptive'],
                }
             
                
    classifiers = {        
            'SVM': (svm.SVC(probability=True, decision_function_shape='ovo'), svm_params),
            'SVM pretuned': (svm.SVC(probability=True, kernel='rbf', decision_function_shape='ovo'), {}),
            'SVM default': (svm.SVC(probability=True), {}),

            'kNN': (neighbors.KNeighborsClassifier(weights='distance', algorithm="ball_tree"), knn_params),
            'kNN pretuned': (neighbors.KNeighborsClassifier(weights='distance', algorithm="ball_tree"), {}),
            'kNN default': (neighbors.KNeighborsClassifier(), {}),

            'MLP': (MLPClassifier(), mlp_params),
            'MLP default': (MLPClassifier(), {}),

        }
    
    
    trained_clfs = []
    
    for name, clf_data in classifiers.iteritems():
        clf = clf_data[0]
        params = clf_data[1]
              
        start = time.clock()
        fitted_clf = optimize_params(clf, params, training_data, training_target)
        end = time.clock()
        log.info("parameter tuning {} took {} seconds".format(name, end - start))

        log.info("{} chosen parameters: {}".format(name, fitted_clf.best_params_))
    
        trained_clfs.append((name, fitted_clf.best_estimator_))
        
        start = time.clock()
        test_clf(name, fitted_clf, test_data, test_target, results)
        end = time.clock()
        log.info("testing classifier {} took {} seconds".format(name, end - start))
    
    
    voting_clf = VotingClassifier(estimators=trained_clfs, voting='soft')
    voting_clf.fit(training_data, training_target)

    
    start = time.clock()
    test_clf("voting", voting_clf, test_data, test_target, results)
    end = time.clock()
    log.info("testing classifier {} took {} seconds".format("voting", end - start))

    return results

if __name__=="__main__":
    valid_participants = range(3) + [x for x in range(12, 49) if x not in [13, 20, 24, 25, 34]]
    averages = {}
    for x, participant in enumerate(valid_participants):
        print("\nTest participant {}".format(participant))
        # do not run quick_test for final experimentation 
        result = run_experiment(participant, valid_participants, fresh_paths=False, quick_test=True)
        for name, clf_result in result.iteritems():
            try:
                a = averages[name]
            except KeyError:
                averages[name] = {}
            for attribute, value in clf_result.iteritems():
                try:
                    averages[name][attribute] += value/len(valid_participants)
                except KeyError:
                    averages[name][attribute] = value/len(valid_participants)


    log.info("Averages: \n{}".format(averages))
    print(averages)

    