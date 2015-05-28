# -*- coding: utf-8 -*-
import re
from attribute import *

def name(filename):
	dic_attr = {}
	for line in filename:
		line = line.strip("\t").split()
		Per = attribute()
		Per.setName(line[1].split(": ")[-1])
		Per.setBirthDate(line[2].split(": ")[-1])
		Per.setBirthPlace(line[3].split(": ")[-1])
		Per.setDeathDate(line[4].split(": ")[-1])
		Per.setGender(line[5].split(":")[-1])
		Per.setHeight(line[6].split(": ")[-1])
		Per.setNation(line[7].split()[-1])
		Per.setNativePlace(line[8].split()[-1])
		Per.setProfession(line[9].split()[-1])
		Per.setWeight(line[10].split()[-1])
		dic_attr[Per.name] = Per
	return dic_attr

def tongju(namePairlist, dic_attr): # 同居
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		features.append(id_feature.feature)
	return features

def xiriqingdi(namePairlist, dic_attr): # 昔日情敌
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		features.append(id_feature.feature)
	return features


def guimi(namePairlist, dic_attr): # 闺蜜
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.height_diff(attr1, attr2)
		id_feature.weight_diff(attr1, attr2)
		features.append(id_feature.feature)
	return features


def pengyou(namePairlist, dic_attr): # 朋友
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		id_feature.birthplace(attr1, attr2)
		features.append(id_feature.feature)
	return features


def fenshou(namePairlist, dic_attr): # 分手
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		features.append(id_feature.feature)
	return features


def laoshi(namePairlist, dic_attr): # 老师 ? 这部分应该加上 是否是老师这个特征
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		# id_feature.gender(attr1, attr2)
		# id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def laoxiang(namePairlist, dic_attr): # 老乡
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		# id_feature.gender(attr1, attr2)
		# id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def tongxue(namePairlist, dic_attr): # 同学
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		# id_feature.gender(attr1, attr2)
		# id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def qiannvyou(namePairlist, dic_attr): # 前女友
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		features.append(id_feature.feature)
	return features


def fanban(namePairlist, dic_attr): # 翻版
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		# id_feature.nativeplace(attr1, attr2)
		# id_feature.nation(attr1, attr2)
		id_feature.height_diff(attr1, attr2)
		id_feature.weight_diff(attr1, attr2)
		features.append(id_feature.feature)
	return features


def qizi(namePairlist, dic_attr): # 妻子
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def zhuangshan(namePairlist, dic_attr): # 撞衫
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		# id_feature.nativeplace(attr1, attr2)
		# id_feature.nation(attr1, attr2)
		features.append = id_feature.feature
	return features


def tongweixiaohua(namePairlist, dic_attr): # 同为校花 身高体重未分块
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		id_feature.height_diff(attr1, attr2)
		id_feature.weight_diff(attr1, attr2)
		features.append(id_feature.feature)
	return features



def feiwennvyou(namePairlist, dic_attr): # 绯闻女友
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		# id_feature.nativeplace(attr1, attr2)
		# id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def ouxiang(namePairlist, dic_attr): # 偶像
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		# id_feature.nativeplace(attr1, attr2)
		# id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def aimei(namePairlist, dic_attr): # 暧昧
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def chuanwenbuhe(namePairlist, dic_attr): # 传闻不和
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		id_feature.gender(attr1, attr2)
		id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		# id_feature.nativeplace(attr1, attr2)
		# id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features


def laoxiang(namePairlist, dic_attr): # 老乡
	features = []
	for id, name1, name2 in namePairlist:
		attr1 = dic_attr[name1]; attr2 = dic_attr[name2]
		id_feature = feature()
		# id_feature.gender(attr1, attr2)
		# id_feature.gender_consistend(attr1, attr2)
		id_feature.age(attr1, attr2)
		id_feature.age_diff(attr1, attr2)
		id_feature.profession_similarity(attr1, attr2)
		id_feature.nativeplace(attr1, attr2)
		id_feature.nation(attr1, attr2)
		features.append(id_feature.feature)
	return features
