
import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/5.0 (Windows NT 10.0)'
headers = {'User-agent':user_agent}

try:
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	# print response.read()
except urllib2.URLError, e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason

content = response.read().decode('utf-8')

# the 3 patterns below,works well each of them
# but when group them together, it will output octonary number八进制， 其实输出的是16进制 u开头 
def getTitle():
	pattern = re.compile(r'<div.*?author.*?title="(.*?)"',re.S)
	items = re.findall(pattern,content)
	# print items[i]
	return items
def getContent():
	pattern = re.compile(r'<div.*?class="content">(.*?)</div>',re.S)
	items = re.findall(pattern,content)
	# print items[i],'\n'
	return items
pat = re.compile('<div.*?author.*?title="(.*?)"',re.S)
# pattern = re.compile('<div.*?class="content">(.*?)</div>',re.S)
# pattern = re.compile('<i.*?class="number">(.*?)</i>',re.S)

#正则式单独匹配没问题，合起来却出现问题
# pattern = re.compile('<div.*?author.*?title="(.*?)".*?<div.*?class=".*?<div.*?class="content">(.*?)</div>.*?<i.*?class="number">(.*?)</i>',re.S)
# pattern = re.compile('<div.*?author.*?title="(.*?)".*?<div.*?class="content">(.+?)</div>.+?<i.*?class="number">(.*?)</i>',re.S)

# pattern = re.compile('<div\sclass\="author.+?title="(.+?)">.+?<div\sclass\="content">(.+?)</div>.+?class\="number">(\d+)</i>',re.S)
# pattern = re.compile('<div\sid="content".+">(.+?)<!--Main\scontent\send\s-->',re.S)
items = re.findall(pat,content)
# print items
Title = getTitle()
Content = getContent()
for i in range(len(items)):
	print Title[i]
	print Content[i]
	# print items[i],i