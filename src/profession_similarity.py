#__author__ = 'Zhihua Zhang'
#-*- coding: utf-8 -*-
import nltk, collections, re, math, copy, numpy


def cosine_similarity(feature1, feature2):
	feature1 = numpy.asarray(feature1)
	feature2 = numpy.asarray(feature2)
	# v.dot(v2) / math.sqrt(v1.dot(v1) * v2.dot(v2))
	return feature1.dot(feature2) / math.sqrt(feature1.dot(feature1) * feature2.dot(feature2))

def CalcuTI(sentence, dic_IDF):
	#sentence = CalcuP(sentence, {})
	for word in sentence:
		sentence[word] *= dic_IDF[word]
	return sentence


def CalcuIDF(sentences, dic_words):
	dic_IDF = collections.defaultdict(float)
	for sentence in sentences:
		sentence = nltk.FreqDist(re.sub("\s+", " ", sentence).split())
		for word in sentence:
			dic_IDF[word] += 1.0
	length = len(sentences)
	for word in dic_IDF:
		dic_IDF[word] = math.log(length / dic_IDF[word], 2)
	return dic_IDF
def Combine1(dic1, dic2):
	# dic3 = collections.defaultdict(float)
	# for t in dic1:
	# 	dic3[t] = dic1[t]
	dic3 = copy.deepcopy(dic1)
	print len(dic1)
	for t in dic2:
		dic3[t] += dic2[t]
	for t in dic3:
		dic3[t] /= 2
	return dic3


def CalcuP(sentence, stopwords):
	dic_freq = collections.defaultdict(float)
	tokens = sentence.split()
	length = 0
	for word in tokens:
		if word in stopwords:
			continue
		dic_freq[word] += 1.0
	dic_freq_copy = copy.copy(dic_freq)
	for word in dic_freq_copy:
		if dic_freq[word] > 0:
			length += dic_freq[word]
		else: dic_freq.pop(word)
	for word in dic_freq:
		dic_freq[word] /= length
	return dic_freq


def CalKL(p, q):
	KL = 0.0
	infinity = 1.0
	accretion = infinity
	for word in p:
		if word in q:
			accretion = p[word] * math.log10(p[word] / q[word])
		KL += accretion
		accretion = infinity
	return KL