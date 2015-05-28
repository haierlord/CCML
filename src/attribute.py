# -*- coding: gbk -*-
import re
from profession_similarity import *
import utils, re, json, pickle
from bagofwords import *


FPROFESSION = []
FDETAIL = []
def load_detail():
	global FPROFESSION
	global FDETAIL
	ff = open("detail_profession.token")
	count = 0
	for line in ff:
		line = line.strip().split("\t")
		# if len(line) > 2:
		# 	print "WRONG!!!", line[0]; break
		temp = re.sub("\s+", "", line[0].strip())
		FPROFESSION.append(temp)
		FDETAIL.append("\t".join(line[1:]).strip())

# load_detail()
# stopwords = utils.GetStopwords(FDETAIL)

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
	# profession = {}
	# for i in range(len(FPROFESSION)):
	# 	profession[FPROFESSION[i].strip()] = CalcuP(FDETAIL[i].strip(), {})
	# wordlist = utils.GetWords(FDETAIL)
	# dic_IDF = CalcuIDF(FDETAIL, wordlist)
	# for i in range(len(FPROFESSION)):
	# 	print i,
	# 	temp = CalcuTI(profession[FPROFESSION[i].strip()], dic_IDF)
	# 	profession[FPROFESSION[i].strip()] = temp
	# pickle.dump(profession, open("T1.pickle", "wb"))
	# fout1 = open("ttt1", "w")
	profession = pickle.load(open("T1.pickle", "rb"))
	for i in range(len(FPROFESSION)):
		print FPROFESSION[i].strip(), ":",
		similaritys = {}
		for j in range(len(FPROFESSION)):
	 		if i == j: continue
			# print len(profession[FPROFESSION[i].strip()])
			# unigram = Combine1(profession[FPROFESSION[i].strip()], profession[FPROFESSION[j].strip()]).keys()
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

# similarity_cosine()

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
		pro = re.sub(",|，", " ", pro)
		self.profession = re.sub("\s+", " ", pro).strip().split()

	def setBirthPlace(self, birthPlace):
		self.birthPlace = birthPlace

	def setWeight(self, weight):
		weight = re.search("(\d+|\d+\.\d*)\D*", weight).group()
		self.weight = int(weight.split(".")[0])

	def setGender(self, gender):
		if gender == "男" or gender == "0":
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


def is_same_Country(place1, place2): # 是否是同一个国家
	return 1

def is_same_Province(place1, place2): # 是否是同一个省
	return 1

def is_same_Firstname(attr1, attr2): # 返回名字是否一致
	return 1

def is_same_nation(attr1, attr2): # 返回是否一个民族
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

def similarity_Profession(attr1, attr2): # 返回两人职业的最高相似度和最低相似度
	cosine = []
	pair_profession = [(x, y) for x in attr1.profession for y in attr2.profession]
	for pro1, pro2 in pair_profession:
		unigram = list(set(TFIDF_PROFESSION[pro1].keys()).union(set(TFIDF_PROFESSION[pro2].keys())))
		feature1 = [0] * len(unigram); feature2 = [0] * len(unigram)
		for index, word in enumerate(unigram):
			if word in TFIDF_PROFESSION[pro1]:
				feature1[index] = TFIDF_PROFESSION[pro1][word]
			if word in TFIDF_PROFESSION[pro2]
				feature2[index] = TFIDF_PROFESSION[pro2][word]
		cosine.append(cosine_similarity(feature1, feature2))
		print cosine[-1]
	return (max(cosine), min(cosine))

per1 = attribute()
per1.setProfession("博士生导师等")
print len(TFIDF_PROFESSION["家务"])
# for t in TFIDF_PROFESSION["家务"]:
# 	print t, TFIDF_PROFESSION["家务"][t]
per2 = attribute()
per2.setProfession("博士生导师")
t = similarity_Profession(per2, per1)
print t

class feature:
	def __init__(self):
		self.feature = []

	def gender(self, attr1, attr2): #性别
		self.feature.append(attr1.gender)
		self.feature.append(attr2.gender)

	def gender_consistent(self, attr1, attr2): # 性别是否一致
		if attr1.gender == attr2.gender:
			self.feature.append(1)
		else:
			self.feature.append(0)

	def weight_diff(self, attr1, attr2): #体重差
		self.feature.append(attr1.weight - attr2.weight)

	def age_diff(self, attr1, attr2): #年龄差
		self.feature.append(attr1.birthDate[0] - attr1.birthDate[0])

	def age(self, attr1, attr2): # 年龄分布
		self.feature += [2015 - attr1.birthDate[0], 2015 -
							attr2.birthDate[0]]

	def height_diff(self, attr1, attr2): # 身高差
		self.feature.append(attr1.height - attr2.height)

	def name_consistent(self, attr1, attr2): # 姓名是否一致
		return 1

	def birthplace(self, attr1, attr2): # 出生地是否一致
		self.feature.append(is_same_Country(attr1.birthPlace, attr2.birthPlace))
		self.feature.append(is_same_Province(attr1.birthPlace, attr2.birthPlace))

	def nativeplace(self, attr1, attr2): # 籍贯是否一致
		self.feature.append(is_same_Country(attr1.nativePlace, attr2.nativePlace))
		self.feature.append(is_same_Province(attr1.nativePlace, attr2.nativePlace))

	def firstname(self, attr1, attr2): # 姓是否一致
		self.feature.append(is_same_Firstname(attr1, attr2))

	def nation(self, attr1, attr2):
		self.feature.append(is_same_nation(attr1, attr2))

	def profession_similarity(self, attr1, attr2):
		self.feature.append(similarity_Profession(attr1, attr2))