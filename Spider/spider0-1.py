# _*_ coding:utf-8 _*_
import urllib
import urllib2
import re
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

page = 1
url = 'http://www.qiushibaike.com/hot/page/'+str(page)
#+'?s=4830655'
user_agent = 'Mozilla/5.0 (Windos NT 10.0)'
headers = {'User-Agent':user_agent}
print url
try:
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	#print response.read()
	content = response.read().decode('utf-8')
	# print content
	# qb = open('qiubai.html','w')
	# qb.write(content)
	#print content
	#pattern = re.compile(r'<div.*?author">.*?<a.*?<img.*>>(.*>)</a>.*?
	# <div.*?'+'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*>class="number">(.*?)</i>',re.S)
	# print pattern
	#pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
    #                     'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
	#22pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?href>*?title="(.*?)">/a>.*?<div.*?class="content">(.*?)<!--.*?</div>.*?<div.*?class="stats.*?<i.*?class="number">(.*?)</i>',re.S)
	# pattern = re.compile(r'<div.*?class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?</div>.*?' +\
	# '<div.*?class="content">(.*?)<!--(.*?)-->.*?</div>.*?' +\
	# '<div.*?class="stats">.*?' +\
	#'<i.*?class="number">(.*?)</i>.*?',re.S)
	####pattern = re.compile('<div.*?content">(.*?)><!--(.*?)--></div>')
	pattern = re.compile('<div.*?class="content">(.*?)</div>',re.S)
	#<a.*?<img.*?>>(.*?)</a>'+\
						# '.*?<div.*?class="content">(.*?)<!--.*?</div>'+\
						# '.*?<div.*?class="stats.*?<i.*?class="number">(.*?)</i>',re.S)
	#print pattern
	
	items = re.findall(pattern,content)
	# print items
	type(items)
	for item in items:
		haveImg = re.search("img",item[3])
		if not haveImg:
			print item#here should apply items[*], or just item
			# ,item[1],item[2],item[3],item[4]
	print 'Get ready'
	
except urllib2.URLError, e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason\




	
print 'done'
