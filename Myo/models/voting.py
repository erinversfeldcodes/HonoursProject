import seqlearn
# from sklearn.ensemble import VotingClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.neural_network import MLPClassifier
#
#
# def compare_voting_ensemble_classifiers(x_train, x_test, y_train, y_test):
#
#     ann = MLPClassifier()
#     knn = KNeighborsClassifier()
#     hmm = seqlearn.hmm.MultinomialHMM()
#
#     ann_knn = VotingClassifier(estimators=[('ann', ann), ('knn', knn)], voting='soft')
#     ann_knn.fit(x_train, y_train)
#
#     best_voting = ann_knn
#     model_type = 'ANN_KNN voting'
#     max_accuracy = ann_knn.score(x_test, y_test)
#     best_params = ann
#
#     knn_hmm = VotingClassifier(estimators=[('knn', knn), ('hmm', hmm)], voting='soft')
#     knn_hmm.fit(x_train, y_train)
#     hmm_ann = VotingClassifier(estimators=[('ann', ann), ('hmm', hmm)], voting='soft')
#     hmm_ann.fit(x_train, y_train)
#     ann_knn_hmm = VotingClassifier(estimators=[('ann', ann), ('knn', knn), ('hmm', hmm)], voting='soft')
#     ann_knn_hmm.fit(x_train, y_train)
#
#     return {'model': best_knn,
#             'model_type': 'KNN',
#             'max_accuracy': max_accuracy,
#             'best_params': best_params,
#             'method': method_params_found,
#             'y_score': y_score,
#             'y_test': y_test
#             }
#     max_accuracy = class1_class2.get('Accuracy')
#     best = class1_class2
#
#     if class1_class3.get('Accuracy') > max_accuracy:
#         max_accuracy = class1_class3.get('Accuracy')
#         best = class1_class3
#     if class2_class3.get('Accuracy') > max_accuracy:
#         max_accuracy = class2_class3.get('Accuracy')
#         best = class1_class3
#     if class1_class2_class3.get('Accuracy') > max_accuracy:
#         msg = '{0}: The best voting ensembler produced an accuracy score of: {1}' \
#               ''.format(str(time.time()), str(class1_class2_class3.get('Accuracy')))
#         print(msg)
#         logging.info(msg)
#         return_values[0] = class1_class2_class3
#         return class1_class2_class3
#
#     msg = '{0}: The best voting ensembler produced an accuracy score of: {1}' \
#           ''.format(str(time.time()), str(max_accuracy))
#     print(msg)
#     logging.info(msg)
#     return_values[0] = best
#
#
# def voting_ensemble_classifier(classifier_1, classifier_2, classifier_3, x_train, x_test, y_train, y_test,
#                                fp_flag=False):
#
#     msg = str(time.time()) + ": Experimenting with voting ensemble classifiers"
#     print(msg)
#     logging.info(msg)
#
#     if fp_flag == 'p':
#         classifier_1 = make_pipeline(cols=set(range(1, 9)))
#         classifier_2 = make_pipeline(cols=set(range(1, 9)))
#     elif fp_flag == 'f':
#         classifier_1 = make_pipeline(cols=set(range(1, 9)))
#         classifier_2 = make_pipeline(cols=set(range(1, 9)))
#     elif fp_flag == 'fp':
#         classifier_1 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4)), classifier_1)
#         classifier_2 = make_pipeline(ColumnSelector(cols=(5, 6, 7, 8)), classifier_2)
#
#         if classifier_3 is not None:
#             classifier_3 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)), classifier_3)
#     else:
#         classifier_1 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8)), classifier_1)
#         classifier_2 = make_pipeline(ColumnSelector(cols=(9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)),
#                                       classifier_2)
#         if classifier_3 is not None:
#             classifier_3 = make_pipeline(ColumnSelector(cols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
#                                                               18, 19, 20, 21)), classifier_3)
#
#     if classifier_3 is not None:
#         ensemble = EnsembleVoteClassifier(clfs=[classifier_1, classifier_2, classifier_3], voting='soft')
#     else:
#         ensemble = EnsembleVoteClassifier(clfs=[classifier_1, classifier_2], voting='soft')
#     ensemble.fit(x_train, y_train)
#     y_score = ensemble.predict(x_test)
#     accuracy = float(ensemble.score(x_test, y_test))
#
#     return {'Accuracy': accuracy, 'y_score': y_score, 'y_train': y_train, 'Classifier type': 'Voting Ensemble'}
