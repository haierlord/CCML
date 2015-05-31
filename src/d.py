from urllib2 import Request, urlopen, URLError, HTTPError


old_url = 'http://rrurl.cn/b1UZuP'
req = Request(old_url)
req.add_header('User-agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0")
print dir(req)
print req.get_header("User-agent")
response = urlopen(req)

print 'Old url :' + old_url
print 'Real url :' + response.geturl()

