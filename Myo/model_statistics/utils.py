import itertools
from itertools import cycle
import logging
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve
from sklearn.preprocessing import label_binarize
import string
import time
import winsound


def calc_model_accuracy(true_positive, false_positive, true_negative, false_negative):
    numerator = true_positive + true_negative
    denominator = true_positive + false_positive + true_negative + false_negative
    try:
        accuracy = numerator/denominator
    except ZeroDivisionError:
        accuracy = 'is not calculatable as TP is ' + str(true_positive) + ', FP is ' + str(false_positive) + ', TN is' \
                                                                                                             '' \
                   + str(true_negative) + 'and FN is ' + str(false_negative)
    return accuracy


def calc_misclassification_rate(true_positive, false_positive, true_negative, false_negative):
    numerator = false_positive + false_negative
    denominator = true_positive + false_positive + true_negative + false_negative
    try:
        accuracy = numerator/denominator
    except ZeroDivisionError:
        accuracy = 'is not calculatable as TP is ' + str(true_positive) + ', FP is ' + str(false_positive) + ', TN is ' \
                   + str(true_negative) + 'and FN is ' + str(false_negative)
    return accuracy


def calc_sensitivity(true_positive, false_negative):
    numerator = true_positive
    denominator = true_positive + false_negative
    try:
        accuracy = numerator/denominator
    except ZeroDivisionError:
        accuracy = "is not calculatable as TP is " + str(true_positive) + " and FN is " + str(false_negative)
    return accuracy


def calc_specificity(false_positive, true_negative):
    numerator = true_negative
    denominator = false_positive + true_negative
    accuracy = numerator/denominator
    return accuracy


def generate_roc_curve(classifier_type, data_type, y_true, y_score, target_names):
    binarised_target = label_binarize(y_true, classes=target_names)
    binarised_score = label_binarize(y_score, classes=target_names)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(len(target_names)):
        cls = target_names[i]
        fpr[cls], tpr[cls], _ = roc_curve(binarised_target[:, i], binarised_score[:, i])
        roc_auc[cls] = auc(fpr[cls], tpr[cls])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(binarised_target.ravel(), binarised_target.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    all_fpr = np.unique(np.concatenate([fpr[cls] for cls in target_names]))
    mean_tpr = np.zeros_like(all_fpr)
    for cls in target_names:
        mean_tpr += np.interp(all_fpr, fpr[cls], tpr[cls])

    # Finally average it and compute AUC
    mean_tpr /= 26

    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    # Plot all ROC curves
    plt.figure()
    plt.plot(fpr["micro"], tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]),
             color='deeppink', linestyle=':', linewidth=4)

    plt.plot(fpr["macro"], tpr["macro"],
             label='macro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["macro"]),
             color='grey', linestyle=':', linewidth=4)

    colors = cycle(['palevioletred', 'crimson', 'darkmagenta', 'dodgerblue', 'navy', 'darkturquoise', 'seagreen',
                    'limegreen', 'indianred', 'sienna', 'firebrick', 'blueviolet', 'cyan', 'darkorchid',
                    'lightseagreen', 'darkorange', 'gold', 'orangered', 'black', 'darkgoldenrod', 'yellow',
                    'hotpink', 'slateblue', 'teal', 'olive', 'darkkhaki'])
    lw = 2
    for cls, color in zip(target_names, colors):
        plt.plot(fpr[cls], tpr[cls], color=color, lw=lw,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(cls, roc_auc[cls]))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    title = 'Receiver operating curve for a ' + classifier_type + ' trained on ' + data_type
    plt.title(title)
    plt.legend(loc="lower right")
    # save_title = title + str(time.time()) + ".pdf"
    # plt.savefig(save_title)
    winsound.Beep(2000, 500)
    plt.show()

    return fpr, tpr


def generate_report(classifier_type, y_true, y_score, target_names):
    report = classification_report(y_true, y_score, target_names=target_names)
    print(report)
    logging.info(str(time.time()) + ": " + classifier_type)
    logging.info(str(time.time()) + ": " + report)


def generate_confusion_matrix(classifier_type, data_type, y_true, y_score, target_names):
    cm = confusion_matrix(y_true, y_score, target_names)
    plot_confusion_matrix(classifier_type, data_type, cm, target_names, normalize=True)
    plot_confusion_matrix(classifier_type, data_type, cm, target_names)


def plot_confusion_matrix(classifier_type, data_type, cm, classes, normalize=False, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    if normalize is True:
        title = "Normalised confusion matrix for " + classifier_type + " trained on " + data_type
    else:
        title = "Confusion matrix for " + classifier_type + " trained on " + data_type
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    winsound.Beep(2000, 500)
    plt.show()
    # save_title = title + str(time.time()) + ".pdf"
    # plt.savefig(save_title)


# def generate_statistics(best_emg, best_imu, best_emg_and_imu):  #, best_ensemble):
def generate_statistics(best_emg,):# best_imu, best_emg_and_imu):
    classifiers = [best_emg]#, best_imu, best_emg_and_imu]  #, best_ensemble]
    count = 0
    for classifier in classifiers:
        if count == 0:
            data_type = 'emg data'
        elif count == 1:
            data_type = 'imu data'
        else:
            data_type = 'both emg and imu data'
        classifier_type = classifier.get('Classifier type')
        y_true = classifier.get('y_train')
        y_score = classifier.get('y_score')
        target_names = list(string.ascii_lowercase)

        fpr, tpr = generate_roc_curve(classifier_type, data_type, y_true, y_score, target_names)
        generate_report(classifier_type, y_true, y_score, target_names)
        generate_confusion_matrix(classifier_type, data_type, y_true, y_score, target_names)

        for letter in target_names:
            tp = tpr[letter]
            fp = fpr[letter]
            tn = 1 - fp
            fn = 1 - tp
            model_accuracy = calc_model_accuracy(tp, fp, tn, fn)
            misclassification_rate = calc_misclassification_rate(tp, fp, tn, fn)
            sensitivity = calc_sensitivity(tp, fn)
            specificity = calc_specificity(fp, tn)
            messages = ["Model accuracy for " + str(letter) + ": " + str(model_accuracy),
                        "Misclassification rate for " + str(letter) + ": " + str(misclassification_rate),
                        "Sensitivity for " + str(letter) + ": " + str(sensitivity),
                        "Specificity for " + str(letter) + ": " + str(specificity)]
            for msg in messages:
                print(msg)
                logging.info(str(time.time()) + ": " + msg)

        count += 1
