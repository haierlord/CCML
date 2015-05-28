#__author__ = 'Zhihua Zhang'
# -*- coding: utf-8 -*-

import collections, re

def GetStopwords(sentences):
	dic_words = collections.defaultdict(int)
	stopwords = {}
	for line in sentences:
		line = re.sub("\s+", " ", line)
		line = line.strip().split()
		for t in line:
			dic_words[t] += 1
	for t in dic_words:
		if dic_words[t] > 4000: stopwords[t] = dic_words[t]
	return stopwords


def GetWords(sentences):
	dic_words = collections.defaultdict(int)
	for line in sentences:
		line = re.sub("\s+", " ", line)
		line = line.strip().split()
		for t in line:
			dic_words[t] += 1
	return dic_words