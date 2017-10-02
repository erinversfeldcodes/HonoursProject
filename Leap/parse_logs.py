# -*- coding: utf-8 -*-
"""
Created on Sun Sep 03 07:36:56 2017

@author: Anna
"""
import glob, os, re, utils, string, sys, numpy
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import pylab


def get_common_features(n, time):
    all_features = []
    for logfile in glob.glob(os.path.join(".", "logs", "*.txt")):
        if os.path.getctime(logfile) < time:
            continue
        feature_blob = ""
        for i, line in enumerate(open(logfile)):
            if "hand_" in line:
                feature_blob += line
        print("")
    #    feature_sets = [[feature.strip("'[]") for feature in feature_set] for feature_set in [x.split() for x in feature_blob.split("features selected: ")]]
        feature_sets = [feature.strip("'[]") for feature_set in [x.split() for x in feature_blob.split("features selected: ")] for feature in feature_set] 
        all_features.extend(feature_sets)
    most_common = Counter(all_features).most_common(n)
    print most_common
    return most_common


def get_average(param, clf, time, num, logfile=""):
    params_lines = []
    accuracies = []
    files = glob.glob(os.path.join(".", "logs", logfile if logfile else "*.txt"))
    for logfile in files:
        if os.path.getctime(logfile) < time:
            continue
        for i, line in enumerate(open(logfile)):
            if ("selected features" in line or "chosen parameters" in line) and "{}" not in line and clf in line:
                params_lines.append(line)
#                print line
#                if param in line:
#                    print logfile
            if "CLASSIFIER: " + clf + " 0" in line:
                accuracies.append(float(line.split()[-1]))
                
    avg = 0
    total = 0
    relevant_accuracies = []
    for i, line in enumerate(params_lines):
        if param in line:
#            print line
#            avg += accuracies[i]
            relevant_accuracies.append(accuracies[i]*100)
#            total += 1
    if len(relevant_accuracies):
        print
        print("average for {}, param {}".format(clf, param))
        print relevant_accuracies
        print len(relevant_accuracies)
#        print avg/total
        mean = numpy.mean(relevant_accuracies)
        std = numpy.std(relevant_accuracies)
        q75, q50, q25 = numpy.percentile(relevant_accuracies, [75, 50, 25])
        minimum = min(relevant_accuracies)
        maximum = max(relevant_accuracies)
        print "mean: " + str(mean)
        print "std: " + str(std)
        print "~~~~~~~~~~~~~~~"
        print "{} {} {} {} {}".format(minimum, q25, q50, q75, maximum)
        print "~~~~~~~~~~~~~~~"
        
        
        plt.boxplot([relevant_accuracies], 0, 'rs', 0,  positions=[num], widths=0.05)



def get_average_time(clf, time, logfile=""):
    times = []
    files = glob.glob(os.path.join(".", "logs", logfile if logfile else "*.txt"))
    for logfile in files:
        if os.path.getctime(logfile) < time:
            continue
        for i, line in enumerate(open(logfile)):
            if "testing classifier" in line and clf + " took" in line:
                times.append(float(line.split()[-2]))

    if len(times):
        print
        print("average time taken to test for {}".format(clf))
        print times
        print len(times)
#        print avg/total
        mean = numpy.mean(times)
        std = numpy.std(times)
        print "mean: " + str(mean)
        print "std: " + str(std)
        print "~~~~~~~~~~~~~~~"

   


def get_confusion_matrices(time, logfile=""):
    matrices = []
    for logfile in glob.glob(os.path.join(".", "logs", logfile if logfile else "*.txt")):
        if os.path.getctime(logfile) < time:
            continue
        with open(logfile, 'r') as lf:
            data = lf.read()
        matrix_matches = re.findall(r'\[\[(.*?)\]\]', data, re.DOTALL)
        matrix_matches = [x for x in matrix_matches if 'hand' not in x]
        clf_matches = re.findall(r'CLASSIFIER: (.*?) 0', data, re.DOTALL)
        if not matrix_matches:
            continue
        for i, x in enumerate(matrix_matches):
            matrix = []
            x = "[" + x + ']]'
            line_matches = re.findall(r'\[(.*?)\]', x, re.DOTALL)
            for line in line_matches:
                line = line.replace('\n', '')
                row = filter(None, line.split(' '))
                row = [int(y) for y in row]
                matrix.append(row)

            matrices.append((clf_matches[i], matrix))
    return matrices
    

def get_total_matrix(clf, matrices):
    totals_matrix = [[0 for x in range(26)] for y in range(26)]
    for name, matrix in matrices:
        if not clf=="all" and name != clf:
            continue
        for j in range(26):
            for k in range(26):
                elem = matrix[j][k]
                totals_matrix[j][k] += elem

    return totals_matrix
                        
def del_quick_tests():
    for logfile in glob.glob(os.path.join(".", "logs", "*.txt")):
        with open(logfile, 'r') as lf:
            data = lf.read()
        if "train_paths: []" in data:
            os.remove(logfile)


def plot_box_whisker():
    fig = pylab.figure()
    ax = pylab.axes()
    pylab.hold(True)
    
    get_average("", 'SVM', 1505544000.0, 1, logfile="experiment_1506586086.44.txt")   
    get_average("", 'kNN', 1505544000.0, 1.1, logfile="experiment_1506586086.44.txt")   
    get_average("", 'MLP', 1505544000.0, 1.2, logfile="experiment_1506586086.44.txt")   
    
    
    plt.ylabel("Classifier")
    plt.xlabel("Percentage")
    
    pylab.xlim(25,70)
    pylab.ylim(0.9, 1.3)
    ax.set_yticks([1, 1.1, 1.2])
    ax.set_yticklabels(['SVM', 'kNN', 'MLP'])
    plt.show()


font = {'size': 22}

matplotlib.rc('font', **font)


#get_average_time('SVM', 1505544000.0, logfile="experiment_1506586086.44.txt")   
#get_average_time('kNN', 1505544000.0, logfile="experiment_1506586086.44.txt")   
#get_average_time('MLP', 1505544000.0, logfile="experiment_1506586086.44.txt")   
#get_average_time('voting', 1505544000.0, logfile="experiment_1506586086.44.txt")   
    
    

#plot_box_whisker()


matrices = get_confusion_matrices(1505000000.0, logfile="experiment_1506586086.44.txt")

clfs = ['all', 'kNN', 'SVM', 'MLP', 'voting']
#clfs = ['all']
for clf in clfs:
    utils.plot_confusion_matrix(get_total_matrix(clf, matrices), list(string.ascii_lowercase), title=clf)
#    
plt.show()

#print(zip(*get_common_features(100, 1505000000.0))[0])

#get_confusion_matrix()



#get_average("poly", 'SVM', 1505000000.0)   
#get_average("alpha': 10.0,", 'MLP', 1505544000.0)   
#get_average("linear", 'SVM', 1505000000.0)   
#get_average("rbf", 'SVM', 1505000000.0)   
#get_average("p': 4", 'kNN', 1504800000.0)   

#for i in range(1,50):
#    get_average("'n_neighbors': " + str(i) + "}", "kNN", 1505000000.0)



#get_average('constant', 'MLP', 1505000000.0)   
#get_average('invscaling', 'MLP', 1505000000.0)
#get_average('adaptive', 'MLP', 1505000000.0)






#average for kNN, param p': 1
#75
#0.485804054261
#average for kNN, param p': 2
#11
#0.483085924601


#average for kNN, param auto
#38
#0.484141794492
#average for kNN, param ball_tree
#48
#0.486497105197


#average for SVM, param poly
#3
#0.572343891121
#average for SVM, param linear
#7
#0.516800595472
#average for SVM, param rbf
#55
#0.507238257213



#average for MLP, param logistic
#14
#0.514682249223
#average for MLP, param tanh
#51
#0.50056171881


#average for MLP, param lbfgs
#44
#0.508343770467
#average for MLP, param sgd
#12
#0.494628086373
#average for MLP, param adam
#9
#0.49239291238



#average for MLP, param constant
#29
#0.50905133516
#average for MLP, param invscaling
#15
#0.500739460313
#average for MLP, param adaptive
#21
#0.498124691623

#
#
#
#ball_av = 0
#print("adam")   
#for logfile in ball_trees:
#    for i, line in enumerate(open(logfile)):
#        if "CLASSIFIER: MLP" in line:
#            ball_av += float(line.split()[-1])         
#
#print(len(ball_trees))
#ball_av = ball_av / len(ball_trees)
#print ball_av


#algorithm ball_tree: 0.365989010989 average
# algorithm auto: 0.389749492642 average
# algorithms inconclusive

#rbf
#22
#0.515135164353
#Poly
#5
#0.510113297555
#Linear
#3
#0.46282051282
# choose rbf

#ovo
#23
#0.520079806292
#ovr
#7
#0.472880871043
# choose ovo

#sgd
#8
#0.487019230769
#adam
#6
#0.475641025641
#inconclusive

#average for MLP, param constant
#10
#0.500952977533
#average for MLP, param invscaling
#8
#0.497424608317
#average for MLP, param adaptive
#8
#0.474038461538
#inconclusive

#average for MLP, param tanh
#9
#0.480189395427
#average for MLP, param logistic
#7
#0.554108649222
#average for MLP, param relu
#5
#0.466923076923
#average for MLP, param identity
#5
#0.449230769231
#suspect

# the only kNN uniform weights which was trainined on more than one participant gave terrible performance .\logs\experiment_1503775988.14.txt
