#_*_ condig:utf-8 _*_
#juse get the page and only LZ楼主 from baidutieba
#  ?&pn='pagenumber' 可以切换到任意pagenumber
import urllib
import urllib2
import re

class BDTB():
	#init, sending base url and if just check LZ楼主
	def __init__(self,baseURL,seeLZ):
		self.baseURL = baseURL
		self.seeLZ = '?see_lz='+str(seeLZ)
		
	#sending pagenumber, get the code of the pagenumber
	def getPage(self,pageNum):
		try:
			url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			print response.read()
			return response
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print '连接贴吧失败',e.reason
				return None
baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.getPage(1)