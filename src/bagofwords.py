#__author__ = 'Zhihua Zhang'
# -*- coding: utf-8 -*-
import collections
import re, nltk
def getGrams(titlelist, threshold, N):
	dic_gram = collections.defaultdict(int)
	for line in titlelist:
		line = re.sub("\s+", " ", line).strip().split()
		grams = nltk.ngrams(line, N)
		for t in grams:
			dic_gram[t] += 1
	return [t for t in dic_gram if dic_gram[t] >= threshold]

def build_BOW(titlelist, wordlist, N):
	features = []
	dic_word = {}
	for index, word in enumerate(wordlist):
		#print word
		dic_word[word] = index
	for line in titlelist:
		line = re.sub("\s+", " ", line).strip().split()
		grams = nltk.ngrams(line, N)
		feature = [0] * len(wordlist)
		for t in grams:
			if t not in dic_word:
				continue
			feature[dic_word[t]] += 1
		features.append(feature)
	return features


def main():
	filename = "../data/version.0.0.1/task1.trainSentence.clean.title.token"
	titlelist = []
	for line in open(filename):
		line = line.split("\t")
		titlelist.append(line[-1])
	threshold = 1
	wordlist = getGrams(titlelist, 3, 1)
	print len(wordlist)
	features = build_BOW(titlelist, wordlist, 1)
	print features[0]
	print features[0].count(1)
	print len(titlelist[0])
	print titlelist[0]
