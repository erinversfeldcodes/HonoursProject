import logging
from operator import itemgetter

from mlxtend.classifier import EnsembleVoteClassifier
from mlxtend.feature_selection import ColumnSelector
from multiprocessing import Manager, Process
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
import time


def compare_voting_ensemble_classifiers(classifier_1, classifier_2, classifier_3, x_train, x_test, y_train, y_test,
                                        feat_extr=False, return_values=[None, None, None]):

    class1_class2 = voting_ensemble_classifier(classifier_1, classifier_2, None, x_train, x_test, y_train, y_test,
                                               feat_extr)
    class1_class3 = voting_ensemble_classifier(classifier_1, classifier_3, None, x_train, x_test, y_train, y_test,
                                               feat_extr)
    class2_class3 = voting_ensemble_classifier(classifier_2, classifier_3, None, x_train, x_test, y_train, y_test,
                                               feat_extr)
    class1_class2_class3 = voting_ensemble_classifier(classifier_1, classifier_2, classifier_3, x_train, x_test,
                                                      y_train, y_test, feat_extr)

    max_accuracy = class1_class2.get('Accuracy')
    best = class1_class2

    if class1_class3.get('Accuracy') > max_accuracy:
        max_accuracy = class1_class3.get('Accuracy')
        best = class1_class3
    if class2_class3.get('Accuracy') > max_accuracy:
        max_accuracy = class2_class3.get('Accuracy')
        best = class1_class3
    if class1_class2_class3.get('Accuracy') > max_accuracy:
        msg = '{0}: The best voting ensembler produced an accuracy score of: {1}' \
              ''.format(str(time.time()), str(class1_class2_class3.get('Accuracy')))
        print(msg)
        logging.info(msg)
        return_values[0] = class1_class2_class3
        return class1_class2_class3

    msg = '{0}: The best voting ensembler produced an accuracy score of: {1}' \
          ''.format(str(time.time()), str(max_accuracy))
    print(msg)
    logging.info(msg)
    return_values[0] = best


def voting_ensemble_classifier(classifier_1, classifier_2, classifier_3, x_train, x_test, y_train, y_test,
                               feat_extr=False):

    msg = str(time.time()) + ": Experimenting with voting ensemble classifiers"
    print(msg)
    logging.info(msg)

    if feat_extr:
        classifier_1 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4)), classifier_1)
        classifier_2 = make_pipeline(ColumnSelector(cols=(5, 6, 7, 8)), classifier_2)

        if classifier_3 is not None:
            classifier_3 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)), classifier_3)
    else:
        classifier_1 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)), classifier_1)
        classifier_2 = make_pipeline(ColumnSelector(cols=(9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)),
                                      classifier_2)
        if classifier_3 is not None:
            classifier_3 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                                              18, 19, 20, 21)), classifier_3)

    if classifier_3 is not None:
        ensemble = EnsembleVoteClassifier(clfs=[classifier_1, classifier_2, classifier_3], voting='soft')
    else:
        ensemble = EnsembleVoteClassifier(clfs=[classifier_1, classifier_2], voting='soft')
    ensemble.fit(x_train, y_train)
    y_score = ensemble.predict(x_test)
    accuracy = float(ensemble.score(x_test, y_test))

    return {'Accuracy': accuracy, 'y_score': y_score, 'y_train': y_train, 'Classifier type': 'Voting Ensemble'}


def random_forest_ensemble(x_train, x_test, y_train, y_test, return_values):
    msg = str(time.time()) + ": Experimenting with random forest ensemble classifiers"
    print(msg)
    logging.info(msg)

    parameter_options = {
        'n_estimators': [26, 52],
        'criterion': ['gini', 'entropy'],
    }
    fitted_rf = get_parameters(RandomForestClassifier(), parameter_options, x_train, y_train)
    best_params = fitted_rf.best_params_
    max_accuracy = fitted_rf.score(x_test, y_test)
    y_score = fitted_rf.predict(x_test)

    msg = '{0}: The best random forest classifier was trained with the parameters{1}which produced an accuracy score ' \
          'of: {2}'.format(str(time.time()), str(best_params), str(max_accuracy))
    print(msg)
    logging.info(msg)
    result = {'Accuracy': max_accuracy, 'y_score': y_score, 'y_train': y_train,
              'Classifier type': 'Random forest', 'Classifier obj': fitted_rf, 'Params': best_params}
    return_values[1] = result


def extra_trees_ensemble(x_train, x_test, y_train, y_test, return_values):
    msg = str(time.time()) + ": Experimenting with extra trees ensemble classifiers"
    print(msg)
    logging.info(msg)

    parameter_options = {
        'n_estimators': [200, 400],
        'criterion': ['gini', 'entropy']
    }
    fitted_et = get_parameters(ExtraTreesClassifier(), parameter_options, x_train, y_train)
    best_params = fitted_et.best_params_
    max_accuracy = fitted_et.score(x_test, y_test)
    y_score = fitted_et.predict(x_test)

    msg = '{0}: The best extra trees classifier was trained with the parameters{1}which produced an accuracy score ' \
          'of: {2}'.format(str(time.time()), str(best_params), str(max_accuracy))
    print(msg)
    logging.info(msg)
    result = {'Accuracy': max_accuracy, 'y_score': y_score, 'y_train': y_train,
              'Classifier type': 'Extra Trees', 'Classifier obj': fitted_et, 'Params': best_params}
    return_values[2] = result


def best_ensemble_classifier(classifier_1, classifier_2, classifier_3, x_train, x_test, y_train, y_test,
                             feat_extr=False):

    msg = str(time.time()) + ": Experimenting with ensemble classifiers"
    print(msg)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logging.info(msg)

    manager = Manager()
    return_values = manager.list([None, None, None])
    voting_thread = Process(target=compare_voting_ensemble_classifiers, args=(classifier_1, classifier_2, classifier_3,
                                                                              x_train, x_test, y_train, y_test,
                                                                              feat_extr, return_values,))
    voting_thread.start()
    rf_thread = Process(target=random_forest_ensemble, args=(x_train, x_test, y_train, y_test, return_values,))
    rf_thread.start()
    et_thread = Process(target=extra_trees_ensemble, args=(x_train, x_test, y_train, y_test, return_values,))
    et_thread.start()

    voting_thread.join()
    rf_thread.join()
    et_thread.join()

    sorted_list = list(sorted(return_values, key=itemgetter('Accuracy')))  # returns all three values in order of worst
    # to best
    voting_thread.terminate()
    rf_thread.terminate()
    et_thread.terminate()

    return sorted_list


def get_parameters(classifier, parameters, x_train, y_train):
    try:
        randomised = RandomizedSearchCV(classifier, parameters, n_iter=40, n_jobs=-1)
        return randomised.fit(x_train, y_train)
    except ValueError:
        grid = GridSearchCV(classifier, parameters)
    return grid.fit(x_train, y_train)