#!/usr/bin/python  
#-*- coding: utf-8 -*-
#
# Create by Meibenjin. 
#
# Last updated: 2013-04-02
#
# google search results crawler 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import re, random, types

from bs4 import BeautifulSoup 

base_url = 'https://www.google.com.hk/'

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
		(KHTML, like Gecko) Element Browser 5.0', \
		'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
		'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
		'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
		'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
		Version/6.0 Mobile/10A5355d Safari/8536.25', \
		'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
		Chrome/28.0.1468.0 Safari/537.36', \
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

# results from the search engine
# basically include url, title,content
class SearchResult:
	def __init__(self):
		self.title = '' 
		self.content = ''
		self.info = ''

	def getInfo(self):
		return self.info

	def getTitle(self):
		return self.title

	def setTitle(self, title):
		self.title = title

	def getContent(self):
		return self.content

	def setInfo(self, info):
		self.info = info

	def setContent(self, content):
		self.content = content

	def printIt(self, prefix = ''):
		print 'title\t->', self.title
		print 'content\t->', self.content
		print 

	def writeFile(self, filename):
		file = open(filename, 'a')
		try:
			file.write('url:' + self.url+ '\n')
			file.write('title:' + self.title + '\n')
			file.write('content:' + self.content + '\n\n')

		except IOError, e:
			print 'file error:', e
		finally:
			file.close()


class BaiduAPI:
	def __init__(self):
		timeout = 40
		socket.setdefaulttimeout(timeout)

	def randomSleep(self):
		sleeptime =  random.randint(60, 120)
		time.sleep(sleeptime)

	#extract the domain of a url
	def extractDomain(self, url):
		domain = ''
		pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
		url_match = pattern.search(url)
		if(url_match and url_match.lastindex > 0):
			domain = url_match.group(1)

		return domain

	# extract serach results list from downloaded html file
	def extractSearchResults_snip(self, html):
		result = SearchResult()
		results = list()
		soup = BeautifulSoup(html)
		div = soup.find('div', {"class": "text", "id": "sec-content0"})
		if (type(div) != types.NoneType):
			lis = div.findAll('div', {'class': 'biItemInner'})
			if(len(lis) > 0):
				attr = ""
				for li in lis:
					biTitle = li.find("span", {"class": "biTitle"})
					if (type(biTitle) != biTitle.NoneType):
						attr += biTitle.text + "\t"
					biContent = li.find("div", {"class": "biContent"})
					if (type(biContent) != biContent.NoneType):
						attr += biContent.text + "\t"
				result.setInfo(attr)
			lis = div.findAll('div', {'class': 'para'})
			if(len(lis) > 0):
				paras = ""
				for li in lis:
					para = re.sub("<a .+a>|<sup>.+<sup>|\[\d*-?\d*\]", " ", li.text)
					paras += para + "\t"
				result.setContent(paras.strip())
		else:
			div = soup.find('div', {"class": "body-wrapper feature feature_small starSmall"})
			lis = div.findAll('div', {'class': 'para'})
			if(len(lis) > 0):
				paras = ""
				for li in lis:
					para = re.sub("<a .+a>|<sup>.+<sup>|\[\d*-?\d*\]", " ", li.text)
					paras += para + "\t"
				result.setContent(paras)
			lisdt = div.findAll('dt', {'class': 'basicInfo-item name'})
			lisdd = div.findAll('dd', {'class': 'basicInfo-item value'})
			if(len(lisdt) > 0):
				attr = ""
				for index, dt in enumerate(lisdt):
					attr += re.sub("\s+", " ", dt.text).strip() + "\t"
					attr += re.sub("\s+", " ", lisdd[index].text).strip() + "\t"
				result.setInfo(attr.strip())

		return [result.info, result.content]

	def extractSearchResults_baike(self, html):
		results = list()
		soup = BeautifulSoup(html)
		div = soup.find("div", id = "content_left")
		if (type(div) != types.NoneType):
			lis = div.findAll("div", {"mu": re.compile("http://baike.baidu.com/.*")})
			if (len(lis)) > 0:
				for li in lis:
					url_baike = li.attrs["mu"]
					Ps = li.findAll("p")
					for P in Ps:
						Dc = P.findAll("a")
						Pc = P.findAll("a", {"href": re.compile("http://.+")})
						if len(Dc) == len(Pc):
							return url_baike
		return ""

	def search_baike(self, query):
		query  = urllib2.quote(query)
		search_results = ""
		url = "http://www.baidu.com.cn/s?wd=" + query + "&cl=3&rn=30"
		retry = 3
		while(retry > 0):
			try:
				request = urllib2.Request(url)
				length = len(user_agents)
				index = random.randint(0, length-1)
				user_agent = user_agents[index]
				request.add_header('User-agent', user_agent)
				request.add_header('connection','keep-alive')
				response = urllib2.urlopen(request)
				html = response.read()
				results = self.extractSearchResults_baike(html)
				return results
			except urllib2.URLError,e:
				print 'url error:', e
				self.randomSleep()
				retry = retry - 1
				continue
			except Exception, e:
				print 'error:', e
				retry = retry - 1
				self.randomSleep()
				continue
		return search_results

	def search_snip(self, query):
		# query = urllib2.quote(query)
		search_results = ["", ""]#list()
		url = query
		#url = '%s/search?hl=%s&num=%d&q=%s' % (base_url, lang, num, query)
		str = ''
		retry = 3
		while(retry > 0):
			try:
				request = urllib2.Request(url)
				length = len(user_agents)
				index = random.randint(0, length-1)
				user_agent = user_agents[index] 
				request.add_header('User-agent', user_agent)
				request.add_header('connection','keep-alive')
				response = urllib2.urlopen(request)
				html = response.read() 
				results = self.extractSearchResults_snip(html)
				return results
			except urllib2.URLError,e:
				print 'url error:', e
				self.randomSleep()
				retry = retry - 1
				continue
			
			except Exception, e:
				print 'error:', e
				retry = retry - 1
				self.randomSleep()
				continue
		return search_results
	
def test():
	url = "http://baike.baidu.com/view/3643732.htm"
	api = BaiduAPI()
	result = api.search_snip(url)
	info = "" ; content = ""
	result[1] = re.sub("\s+", " ", result[1])
	for t in result[0]:
		try:
			info += t.encode("gbk")
		except:
			continue
	print info
	for t in result[1]:
		try:
			content += t.encode("gbk")
		except:
			continue
	print content
	return 1

# test()
def	catchBaike():
	fin = open("../data/attribute/attribute_url.all")
	dic_ = {}
	dic_info = {}
	dic_content = {}
	for line in fin:
		line = line.strip().split("\t")
		dic_[line[0]] = line[-1]
		dic_info[line[0]] = ""
		dic_content[line[0]] = ""
	fout1 = open("../data/attribute/attribute.info", "a")
	fout2 = open("../data/attribute/attribute.content", "a")
	iter = 0
	while (iter < 25):
		iter += 1
		for name, url in dic_.iteritems():
			if len(dic_info[name]) >= 4: continue
			print iter, name,
			api = BaiduAPI()
			result = api.search_snip(url)
			info = ""; content = ""
			result[1] = re.sub("\s+", " ", result[1])
			for t in result[0]:
				try:
					info += t.encode("gbk")
				except:
					continue
			try:
				print info[:20]
			except:
				print info
			for t in result[1]:
				try:
					content += t.encode("gbk")
				except:
					continue
			dic_info[name] = info; dic_content[name] = content
			if len(info) >= 4:
				fout1.write(name + "\t" + info + '\n')
				fout2.write(name + "\t" + content + '\n')
	with open("../data/attribute/final.info", "w") as f:
		for name, info in dic_info.iteritems():
			f.write(name + "\t" + info + "\n")
		f.close()
	with open("../data/attribute/final.content", "w") as f:
		for name, content in dic_content.iteritems():
			f.write(name + "\t" + content + "\n")


catchBaike()

def main0():
	professions = "lose3"
	fout = open("lose3_professions", "w")
	for line in open(professions):
		print line.strip()
		fout.write(line.strip() + "\t")
		api = BaiduAPI()
		results = api.search(line.strip())
		for i in range(min(15, len(results))):
			title = '';
			for t in results[i].getTitle():
				try:
					title += t.encode("gbk")
				except:
					continue
			content = '';
			for t in results[i].getContent():
				try:
					content += t.encode("gbk")
				except:
					continue
			fout.write(title + ' ' + content + '\t')
		fout.write("\n")

def main1():
	fout = open("../data/attribute/attribute_url.exist", "w")
	count = 0
	dic_lose = {}
	for line in open("../data/attribute/attribute.clean"):
		line = line.strip().split("\t")
		if len(line) != 4:
			dic_lose[line[3]] = ""
		# else:
		# 	dic_lose[line[0]] = line[-1]#"http://baike.baidu.com/view/" + line[1] + ".htm"
	iter = 0
	print sum([1 for t in dic_lose if dic_lose[t] == ""])
	while (iter < 10):
		for name in dic_lose:
			if len(dic_lose[name]) > 3: continue
			print iter, name,
			api = BaiduAPI()
			result = api.search_baike(name)
			temp = ""
			for t in result:
				try:
					temp1 = t.encode("gbk")
					temp += temp1
				except:
					continue
			print temp
			dic_lose[name] = temp.strip()
		iter += 1
	for t in dic_lose:
		fout.write(t + '\t' + dic_lose[t] + '\n')

