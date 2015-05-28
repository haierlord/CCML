#__author__ = 'Zhihua Zhang'
# -*- coding: utf-8 -*-
import sklearn
from sklearn import svm
from sklearn import metrics
import random, logging
import numpy as np

logging.basicConfig(format = "%(asctime)s %(message)s", datefmt = "%H-%M-%S    ", level = logging.INFO)


def eval_classifier(train_X, train_Y, test_X, test_Y, clf):
	clf.fit(train_X, train_Y)
	predict_Y = clf.predict(test_X)
	f1 = metrics.f1_score(predict_Y, test_Y, labels = [1, 0, 2], average = None)
	return (predict_Y, f1[0])

def classifier(features, labels):
	classifiers = []
	features = np.asarray(features)
	labels = np.asarray(labels)
	kernel = ["rbf", "linear"]
	kernel = "linear"
	if kernel == "rbf":
		for c in [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10]:
			clf = svm.SVC(kernel = kernel, C = c)
			classifiers.append((clf, kernel, c))
	else:
		for c in [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10]:
			clf = svm.SVC(kernel = kernel, C = c)
			classifiers.append((clf, kernel, c))
	label_1 = []; label_0 = []
	for index, t in enumerate(labels):
		if t == 1: label_1.append(index)
		else: label_0.append(index)
	cvs = [[], [], [], [], []]
	length_0 = len(label_0) / 5; length_1 = len(label_1) / 5
	for i in range(4):
		temp_0 = random.sample(label_0, length_0)
		temp_1 = random.sample(label_1, length_1)
		cvs[i] = temp_0 + temp_1
		t_0 = set(label_0); t_1 = set(label_1)
		for t in temp_0:
			t_0.remove(t)
		for t in temp_1:
			t_1.remove(t)
		label_0 = list(t_0); label_1 = list(t_1)
	cvs[4] = label_0 + label_1
	ans = []
	for clf, kernel, c in classifiers:
		f1s = []
		for cv in range(5):
			index_train = []
			for i in range(5):
				if i != cv: index_train += cvs[i]
			X_train = features[index_train]; Y_train = labels[index_train]
			X_test = features[cvs[cv]]; Y_test = labels[cvs[cv]]
			Y_pred, f1 = eval_classifier(X_train, Y_train, X_test, Y_test, clf)
			f1s.append(f1)
		f1score = sum(f1s) / 5.0
		ans.append(f1score)
	# 	logging.info("Kernel: %s\t C: %f\t%.3f"%(kernel, c, f1score))
	# 	print "Kernel: %s\t C: %f\t%.3f"%(kernel, c, f1score)
	# print "-"*30, "max = %.3f"%max(ans)