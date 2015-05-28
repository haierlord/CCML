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

	def getTitle(self):
		return self.title

	def setTitle(self, title):
		self.title = title

	def getContent(self):
		return self.content

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
		results = list()
		soup = BeautifulSoup(html)
		div = soup.find('div', id  = 'content_left')
		if (type(div) != types.NoneType):
			lis = div.findAll('div', {'class': 'result c-container '})
			if(len(lis) > 0):
				for li in lis:
					result = SearchResult()
					h3 = li.find('h3', {'class': 't'})
					if(type(h3) == types.NoneType):
						continue
					# extract domain and title from h3 object
					link = h3.find('a')
					if (type(link) == types.NoneType):
						continue
					title = link.text
					abst = li.find("div", {"class": "c-abstract"})
					if (type(abst) == types.NoneType):
						content = title
					else:
						content = abst.text
					result.setContent(content)
					result.setTitle(title)
					results.append(result)
		return results

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
	# search web
	# @param query -> query key words 
	# @param lang -> language of search results  
	# @param num -> number of search results to return 
	def search_snip(self, query):
		query = urllib2.quote(query)
		search_results = list()
		url = "http://www.baidu.com.cn/s?wd=" + query + "&cl=3&rn=30"
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
				results = self.extractSearchResults(html)
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
	fout = open("lose1_attribute", "w")
	count = 0
	# api = BaiduAPI()
	# results = api.search_baike("沙龙")
	# print results
	for line in open("lose_attribute"):
		count += 1
		line = line.strip().split("\t")
		if len(line) == 4:
			api = BaiduAPI()
			results = api.search_baike(line[-1])
			temp = ""
			for t in results:
				try:
					temp1 = t.encode("gbk")
					temp += temp1
				except:
					continue
			temp = "\t".join(line + [temp])
			fout.write(temp + '\n')
			print count, line[-1], results

main1()