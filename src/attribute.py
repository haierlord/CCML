# -*- coding: gbk -*-
import re, codecs
from profession_similarity import *
import utils, re, json, pickle
from bagofwords import *


FPROFESSION = []
FDETAIL = []
dic_profession = {}
def load_detail():
	global FPROFESSION
	global FDETAIL
	global dic_profession
	ff = codecs.open("detail_profession.token", encoding = "gbk")
	count = 0
	for line in ff:
		line = line.strip().split("\t")
		# if len(line) > 2:
		# 	print "WRONG!!!", line[0]; break
		temp = re.sub("\s+", "", line[0].strip())
		FPROFESSION.append(temp)
		dic_profession[temp] = line[0]
		FDETAIL.append("\t".join(line[1:]).strip())

load_detail()
stopwords = utils.GetStopwords(FDETAIL)

def similarity_KL():
	profession = {}
	for i in range(len(FPROFESSION)):
		# profession[FPROFESSION[i].strip()] = re.sub("\s+", " ", FDETAIL[i]).strip()
		profession[FPROFESSION[i].strip()] = CalcuP(FDETAIL[i].strip(), stopwords)
	for i in range(len(FPROFESSION)):
		print FPROFESSION[i].strip(), ":"
		similaritys = {}
		for j in range(len(FPROFESSION)):
			if i == j: continue
			dic_c = Combine(profession[FPROFESSION[i].strip()], profession[FPROFESSION[j].strip()])
			similaritys[FPROFESSION[j].strip()] = CalKL(profession[FPROFESSION[i].strip()], dic_c)
		sort = sorted(similaritys.iteritems(), key = lambda d:d[1], reverse = True)
		for p, K in sort[: 10]:
			print p, K, "--",
		print
# similarity_KL()
def similarity_cosine():
	profession = pickle.load(open("T1.pickle", "rb"))
	for i in range(len(FPROFESSION)):
		print FPROFESSION[i].strip(), ":",
		similaritys = {}
		for j in range(len(FPROFESSION)):
			if i == j: continue
			unigram = list(set(profession[FPROFESSION[i].strip()].keys()).union(set(profession[FPROFESSION[j].strip()].keys())))
			feature1 = [0] * len(unigram); feature2 = [0] * len(unigram)
			for index, word in enumerate(unigram):
				if word in profession[FPROFESSION[i].strip()]:
					feature1[index] = profession[FPROFESSION[i].strip()][word]
				if word in profession[FPROFESSION[j].strip()]:
					feature2[index] = profession[FPROFESSION[j].strip()][word]
			similaritys[FPROFESSION[j].strip()] = cosine_similarity(feature2, feature1)
		sort = sorted(similaritys.iteritems(), key = lambda d:d[1], reverse = True)
		for p, K in sort[: 10]:
			print p, K, "--",
		print

print dic_profession.keys()[0]
def similarity_w2v_cosine():
#	dic_word = load_vector("../../dataset/LDC2009T14_T_C/data/xin_all.vector", dic_profession)
	dic_word = pickle.load(open("profession_w2v.pickle", "rb"))
	for word in dic_word:
		similarity = {}
		for word1 in dic_word:
			if word == word1:
				continue
			similarity[word1] = cosine(dic_word[word], dic_word[word1])
		sort = sorted(similarity.iteritems(), key = lambda d:d[1], reverse = True)
		print word,
		for p, K in sort[: 10]:
			print p, K, "--",
		print

similarity_w2v_cosine()

class attribute:
	def __init__ (self):
		self.name = ""
		self.profession = []
		self.birthPlace = ""
		self.deathDate = [0, 0, 0]
		self.weight = 0
		self.gender = 0
		self.nativePlace = ""
		self.height = 0
		self.nation = ""
		self.birthDate = [0, 0, 0]

	def setName(self, name):
		self.name = name

	def setProfession(self, pro):
		pro = re.sub(",|��", " ", pro)
		self.profession = re.sub("\s+", " ", pro).strip().split()

	def setBirthPlace(self, birthPlace):
		self.birthPlace = birthPlace

	def setWeight(self, weight):
		weight = re.search("(\d+|\d+\.\d*)\D*", weight).group()
		self.weight = int(weight.split(".")[0])

	def setGender(self, gender):
		if gender == "��" or gender == "0":
			self.gender = 0
		else:
			self.gender = 1

	def setNativePlace(self, nativePlace):
		self.nativePlace = nativePlace

	def setHeight(self, height):
		height = int(re.search("(\d+)", height))

	def setNation(self, nation):
		self.nation = nation

	def setBirthDate(self, birthDate):
		birthDate = re.findall("(\d+)", birthDate)
		for i in range(3):
			try:
				birthDate[i] = int(birthDate[0])
			except:
				birthDate.append(1)
		self.birthDate = birthDate

	def setDeathDate(self, deathDate):
		deathDate = re.findall("(\d+)", deathDate)
		for i in range(3):
			try:
				deathDate[i] = int(deathDate[0])
			except:
				deathDate.append(1)
		self.deathDate = deathDate


def is_same_Country(place1, place2): # �Ƿ���ͬһ������
	return 1

def is_same_Province(place1, place2): # �Ƿ���ͬһ��ʡ
	return 1

def is_same_Firstname(attr1, attr2): # ���������Ƿ�һ��
	return 1

def is_same_nation(attr1, attr2): # �����Ƿ�һ������
	return 1

TFIDF_PROFESSION = {}
def load_tfidf_profession():
	global TFIDF_PROFESSION
	ftfidf = open("TFIDF_profession")
	for line in ftfidf:
		line = line.strip().split("\t")
		TFIDF_PROFESSION[line[0]] = collections.defaultdict(float)
		for index, t in enumerate(line[1:]):
			t = t.split("-")
			TFIDF_PROFESSION[line[0]]["-".join(t[:-1])] = float(t[-1])

TFIDF_PROFESSION = pickle.load(open("T1.pickle", "rb"))
print type(TFIDF_PROFESSION.keys()[0])
print len(TFIDF_PROFESSION)

def similarity_Profession(attr1, attr2): # ��������ְҵ��������ƶȺ�������ƶ�
	cosine = []
	pair_profession = [(x, y) for x in attr1.profession for y in attr2.profession]
	for pro1, pro2 in pair_profession:
		unigram = list(set(TFIDF_PROFESSION[pro1].keys()).union(set(TFIDF_PROFESSION[pro2].keys())))
		feature1 = [0] * len(unigram); feature2 = [0] * len(unigram)
		for index, word in enumerate(unigram):
			if word in TFIDF_PROFESSION[pro1]:
				feature1[index] = TFIDF_PROFESSION[pro1][word]
			if word in TFIDF_PROFESSION[pro2]:
				feature2[index] = TFIDF_PROFESSION[pro2][word]
		cosine.append(cosine_similarity(feature1, feature2))
		print cosine[-1]
	return (max(cosine), min(cosine))

per1 = attribute()
per1.setProfession("��ʿ����ʦ��")
print len(TFIDF_PROFESSION["����"])
# for t in TFIDF_PROFESSION["����"]:
# 	print t, TFIDF_PROFESSION["����"][t]
per2 = attribute()
per2.setProfession("��ʿ����ʦ")
t = similarity_Profession(per2, per1)
print t

class feature:
	def __init__(self):
		self.feature = []

	def gender(self, attr1, attr2): #�Ա�
		self.feature.append(attr1.gender)
		self.feature.append(attr2.gender)

	def gender_consistent(self, attr1, attr2): # �Ա��Ƿ�һ��
		if attr1.gender == attr2.gender:
			self.feature.append(1)
		else:
			self.feature.append(0)

	def weight_diff(self, attr1, attr2): #���ز�
		self.feature.append(attr1.weight - attr2.weight)

	def age_diff(self, attr1, attr2): #�����
		self.feature.append(attr1.birthDate[0] - attr1.birthDate[0])

	def age(self, attr1, attr2): # ����ֲ�
		self.feature += [2015 - attr1.birthDate[0], 2015 -
							attr2.birthDate[0]]

	def height_diff(self, attr1, attr2): # ��߲�
		self.feature.append(attr1.height - attr2.height)

	def name_consistent(self, attr1, attr2): # �����Ƿ�һ��
		return 1

	def birthplace(self, attr1, attr2): # �������Ƿ�һ��
		self.feature.append(is_same_Country(attr1.birthPlace, attr2.birthPlace))
		self.feature.append(is_same_Province(attr1.birthPlace, attr2.birthPlace))

	def nativeplace(self, attr1, attr2): # �����Ƿ�һ��
		self.feature.append(is_same_Country(attr1.nativePlace, attr2.nativePlace))
		self.feature.append(is_same_Province(attr1.nativePlace, attr2.nativePlace))

	def firstname(self, attr1, attr2): # ���Ƿ�һ��
		self.feature.append(is_same_Firstname(attr1, attr2))

	def nation(self, attr1, attr2):
		self.feature.append(is_same_nation(attr1, attr2))

	def profession_similarity(self, attr1, attr2):
		self.feature.append(similarity_Profession(attr1, attr2))
