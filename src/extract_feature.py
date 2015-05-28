#__author__ = 'Zhihua Zhang'
# -*- coding: utf-8 -*-

from attribute import attribute
from relations import *
from bagofwords import *
import collections
from classifier import *
import logging
logging.basicConfig(format = "%(asctime)s %(message)s", datefmt = "%H-%M-%S    ", level = logging.INFO)

def tran_file(filename):
	# dic_attr = name(filename1)
	fin = open(filename) # task1.trainSentence.clean
	dic_train = collections.defaultdict(dict)
	titlelist = []
	for line in fin:
		line = line.strip().split("\t")
		dic_train[line[0]][len(dic_train[line[0]])] = {"label": int(line[4]), "title": line[3], "pair": (line[1], line[2])}
		titlelist.append(line[3])
	dic_features = collections.defaultdict(dict)
	unigram = getGrams(titlelist, 3, 1)
	bigram = getGrams(titlelist, 3, 1)
	dic_func = {"同居": tongju, "昔日情敌": xiriqingdi, "闺蜜": guimi, "朋友": pengyou, "分手": fenshou, "老师": laoshi, "同学": tongxue, "前女友": qiannvyou, "翻版": fanban, "妻子": qizi, "撞衫": zhuangshan, "同为校花": tongweixiaohua, "绯闻女友": feiwennvyou, "偶像": ouxiang, "暧昧": aimei, "传闻不和": chuanwenbuhe, "老乡":laoxiang}
	for relation in dic_train:
		namelist = []; labels = []; titlelist = []
		for id in dic_train[relation]:
			dic_ = dic_train[relation][id]
			namelist.append((len(namelist), dic_["pair"][0], dic_["pair"][1]))
			labels.append(dic_["label"])
			titlelist.append(dic_["title"])
		logging.info("%s:\t%d"%(relation, len(titlelist)))
		# features = dic_func[relation](namelist, dic_attr)
		uni_features = build_BOW(titlelist, unigram, 1)
		bi_features = build_BOW(titlelist, bigram, 1)
		features = uni_features
		features = bi_features
		# for index, feature in enumerate(features):
		# 	# features[index] += uni_features[index]
		# 	features[index] += bi_features[index]
		dic_features[relation]["features"] = features
		dic_features[relation]["label"] = labels
		dic_features[relation]["namelist"] = namelist
		classifier(features, labels)

trainfile = "../data/version.0.0.1/task1.trainSentence.clean.all"
tran_file(trainfile)