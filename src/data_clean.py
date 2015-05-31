# -*- coding: utf-8  -*- 
import collections
import codecs, os, re, csv

def tran(str):
	return unicode(str, "utf-8")

def func1():
	dic = {"name":1, "weight":1, "birthDate":1, "height":1, "alias":1, "profession":1, "birthPlace":1, "nation":1, "deathDate":1, "gender":1, "nativePlace":1}
	leng = len(dic)
	f = open("attribute").readlines()
	count = 0
	dic = collections.defaultdict(int)
	for index, line in enumerate(f):
		line1 = line.strip().split("\t")[2:]
		length = len(line1) / 2
		dic[length] += 1
		if length == leng - 9:
			count += 1
	print count
	print dic
	
	
def func2(): # 统计正负样本
	dic = collections.defaultdict(int)
	for line in open("task1.trainSentence.clean"):
		line = line.strip().split("\t")
		if line[0] not in dic:
			dic[line[0]] = collections.defaultdict(int)
		dic[line[0]][line[4]] += 1
	# fout = open("task1.trainSentence.clean", "w")
	for t in "同居 昔日情敌 闺蜜 朋友 分手 老师 老乡 同学 前女友 翻版 妻子 撞衫 同为校花 绯闻女友 偶像 暧昧 传闻不和 经纪人 前妻".split():
	#for t in "妻子 昔日情敌 闺蜜 分手 撞衫 老师 老乡 暧昧 同学 前女友 翻版 经纪人 绯闻女友 同为校花 前妻 偶像 朋友 传闻不和 同居"
		#print unicode(t, "utf-8"), dic[t]["1"] + dic[t]["0"], dic[t]["0"], dic[t]["1"]
		print tran(t), dic[t]
		# fout.write(t)
	# print dic.values()
	# for t in dic:
		# print unicode(t, "utf-8"), '\t', dic[t]["1"] + dic[t]["0"], "\t", dic[t]['0'], dic[t]['1']
	# print len(dic)

def func3():
	t1 = "同居 昔日情敌 闺蜜 朋友 分手 老师 老乡 同学 前女友 翻版 妻子 撞衫 同为校花 绯闻女友 偶像 暧昧 传闻不和 经纪人 前妻".split()
	t2 = "老师 儿子 队友 妻子 哥哥 旧爱 祖父 同学 姐姐 女婿 撞衫 撞脸 前妻 前女友 老乡 传闻不和 经纪人 绯闻女友 闺蜜 偶像".split()
	for t in t2:
		if t not in t1:
			print unicode(t, "utf-8"), 
	print len(t1), len(t2)
	
def func4():
	dic = collections.defaultdict(int)
	count = 0
	for line in open("task2.TrainSPO"):
		count += 1
		dic[line] += 1
	# for t in dic:
		# if dic[t] > 2:
			# print unicode(t, "utf-8")
	print dic.values()
	print len(dic), count
	
def func5():
	dic = collections.defaultdict(int)
	for line in open("task1.trainSentence.clean"):
		line = line.strip().split("\t")
		if line[4] == "0": continue
		dic[line[1]] += 1; dic[line[2]] += 1
	print "train: ", len(dic)
	dic1 = collections.defaultdict(int)
	for line in open("task1.assistSentence"):
		line = line.strip().split("\t")
		dic1[line[1]] += 1; dic[line[0]] += 1
	print "assist: ", len(dic1)
	dic2 = collections.defaultdict(int)
	for t in dic:
		if t in dic1:
			dic2[t] = dic[t]
	print "joint: ", len(dic2)		

	
def func6():
	dic = collections.defaultdict(int)
	for line in open("task2.TrainSPO"):
		line = line.strip().split("\t")
		tup = (line[1], line[2])
		if line[3] == "0":
			continue;
		dic[tup] += 1
	for t in dic:
		if dic[t] > 1:
			print tran(t[0]), '\t', tran(t[1])
			
def func7(): # task2.TrainSOSet 去重			
	fout = open("task2.trainSOSet.clean", "w")
	fin  = open("task2.trainSOSet")
	for line in fin:
		dic = {}
		line = line.strip().split("\t")
		fout.write("\t".join(line[:6]))
		for index, url in enumerate(line[6:]):
			if index % 2 == 0:
				content = url
				continue
			dic[content] = url
		for t in dic:
			fout.write("\t" + t + "\t" + dic[t])
		fout.write("\n")
	fout.close()
	
	
def func8(): # task1。assist 去除新闻名 --> clean
	assistfile = codecs.open("../data/attribute/attribute", encoding = "utf-8")
	fout = codecs.open("../data/attribute/attribute.clean","w")
	dic_ = {}
	for line in assistfile:
		line1 = line.split("\t")
		temp = ""
		if line1[0] in dic_:
			continue
		dic_[line1[0]] = 1
		for t in line:
			try:
				temp1 = t.encode("gbk")
				temp += temp1
			except:
				continue
		#line = " ".join(temp.split("\t")[:3])
		if temp in dic_:
			continue
		fout.write(temp.strip() + "\n")	
		


def func9():
	assistfile = codecs.open("../../data/version.0.0.1/task1.assistSentence.clean")
	fout = open("../../data/version.0.0.1/task1.assistSentence.title", "w")
	for line in assistfile:
		line = line.strip().split("\t")
		if '_' in line[2]:
			t = line[2].split("_")
		else:
			t = line[2].split("-")
		fout.write("\t".join([line[0], line[1], t[0].strip()]) + "\n")
		
def func10(): # user_name_dict
	assistfile1 = codecs.open("../../data/version.0.0.1/task1.assistSentence.clean")
	assistfile2 = codecs.open("../../data/version.0.0.1/task1.trainSentence.clean")
	attribute = open("../../data/version.0.0.1/attribute.clean")
	fout = open("userdic.txt", "w")
	dic = {}
	for line in assistfile2:
		line = line.split("\t")
		dic[line[1]] = 1; dic[line[2]] = 1
	for line in assistfile1:
		line = line.split("\t")
		dic[line[0]] = 1; dic[line[1]] = 1
	for line in attribute:
		line = line.strip().split("\t")
		dic[line[3]] = 1
	for t in dic:
		fout.write(t + "\tnr\n")
		
def func11(): # task1.assistSentence.title.v1 --> remove name in title --> tokenization
	fin = open("../../data/version.0.0.1/task1.assistSentence.clean")
	fout = open("../../data/version.0.0.1/task1.assistSentence.clean.title", "w")
	for line in fin:
		line = line.split("\t")
		line[2] = re.sub(line[1], " Subject ", line[2])
		line[2] = re.sub(line[0], " Object ", line[2]).strip()
		line[2] = re.sub("\s+", " ", line[2])
		fout.write("\t".join(line[0:3]).strip() + "\n")
		
def func12(): #statistic of attribute_clean
	fin = open("../../data/version.0.0.1/attribute.clean")
	dic = collections.defaultdict(set)
	for line in fin:
		line = line.strip().split("\t")[2:]
		for index, t in enumerate(line):
			if index % 2 != 0:
				t = t.replace("、", " ")
				t = re.sub(",", " ", t)
				t = re.sub("\s+", " ", t).strip().split(" ")
				dic[attribute].update(t)
				continue
			attribute = t
	for t in dic["profession"]:
		print t
	print len(dic["profession"])

def func13():
	fin1 = open("../../data/version.0.0.1/attribute.clean")
	fin1 = open("../../data/version.0.0.1/task1.trainSentence.clean")
	fin2 = open("../../data/version.0.0.1/task1.assistSentence.clean")
	dic1 = {}; dic2 = {}
	for line in fin1:
		line = line.strip().split("\t")
		#dic1[line[3]] = 1
		dic1[line[1]] = 1; dic1[line[2]] = 1
	for line in fin2:
		line = line.strip().split("\t")
		dic2[line[1]] = 1; dic2[line[0]] = 1
	count = 0
	for t in dic2:
		if t in dic1:
			count += 1
	print "attribute:", len(dic1)
	print "task1.assist:", len(dic2)
	print "attribute_task1.assist:", count
	
def func14():
	fin = open("../../data/version.0.0.1/task1.assistSentence.clean.title.token")
	for line in fin:
		line1 = line.split("\t")
		if line1[0].count("/") > 1 or line1[1].count("/") > 1:
			print line
		
	
def func15():
	fin2 = open("../data/version.0.0.1/task1.trainSentence.clean.title.token")
	fin1 = open("../data/version.0.0.1/task1.trainSentence.clean")
	fout = open("../data/version.0.0.1/task1.trainSentence.clean.all", "w")
	for line in fin1:
		line = line.split("\t")
		line1 = fin2.readline().strip().split("\t")[-1].strip()
		line[3] = line1
		fout.write("\t".join(line))

def func16():
	fin = []
	fin.append(open("detail_professions"))
	fin.append(open("lose_professions"))
	fin.append(open("lose1_professions"))
	fin.append(open("lose2_professions"))
	fin.append(open("lose3_professions"))
	fout = open("detail_profession", "w")
	for f in fin:
		for line in	f:
			line1 = line.strip().split()
			if len(line1) != 1:
				fout.write(line)

def func17():
	fin = open("../data/version.0.0.1/attribute.clean").readlines()
	writer = csv.writer(open("../data/version.0.0.1/attribute.clean.csv", "w"))
	dic_attr = collections.defaultdict(int)
	for line in fin:
		line = line.strip().split("\t")
		for i in range(2, len(line), 2):
			dic_attr[line[i]] += 1
	attrs = ["id0", "id1"] + dic_attr.keys()
	writer.writerow(attrs)
	for line1 in fin:
		line = line1.strip().split("\t")
		temp = line[:2]
		dic_temp = {}
		for i in range(2, len(line), 2):
			try:
				dic_temp[line[i]] = line[i + 1].strip()
			except:
				dic_temp[line[i]] = "sb"
		for t in attrs[2:]:
			if t in dic_temp:
				temp.append(dic_temp[t])
			else:
				temp.append("")
		writer.writerow(temp)

def func18():
	fin = open("../data/version.0.0.1/attribute.clean").readlines()
	fout = open("../data/version.0.0.1/lose_attribute", "w")
	for line in fin:
		line = line.strip().split("\t")
		if len(line) == 4:
			fout.write(line[0] + "\t" +  line[-1] + "\n")

def func19():
	fin = csv.reader(open("../data/version.0.0.1/attribute.clean.csv"))
	count = 0
	attribute = fin.next()
	dic_attribute = {}
	for index, t in enumerate(attribute):
		dic_attribute[t] = index
	list_attribute = [collections.defaultdict(int) for t in attribute]
	for line in fin:
		for index, t in enumerate(line):
			list_attribute[index][t] += 1
	for t in list_attribute[-1]:
		print t, list_attribute[-1][t]
	print len(list_attribute[-1])
	print attribute
func8()
	

	