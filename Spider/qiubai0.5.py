#_*_ coding:utf-8 _*_
#对匿名用户无效
import urllib
import urllib2
import re

class QSBK():
	#init the data
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0)'
		self.headers = {'User-Agent':self.user_agent}
		#to simulate the browser
		# self.Title = []
		# self.Content = []
		self.nextpage = False
	#get the page's coding in utf-8
	def getPage(self,pageIndex):
		try:
			pageIndex = self.pageIndex
			url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex)
			#creat a request
			request = urllib2.Request(url,headers = self.headers)
			#get a response via urlopen
			response = urllib2.urlopen(request)
			#decode the response to UTF-8
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print '连接失败'
				return None
	#input the pageCode and return title and content
	def getItems(self,pageIndex):
		self.nextpage = False
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print '页面加载失败'
			return None
		titlepattern = re.compile('<div\sclass="author.+?title="(.*?)".+?</a>',re.S)
		title = re.findall(titlepattern,pageCode)
		#  此处多了数值判断会没有结果 <div.*?class="content">(.*?)<!--.*?--></div>
		contentpattern = re.compile('<div.*?class="content">(.*?)</div>',re.S)
		content = re.findall(contentpattern,pageCode)
		# print len(content),len(title)
		# print content[19],title[19]
		#return two value and prepare two varables to accept it's value
		return title,content
	#get one story each time
	def getOnestory(self,pageIndex):
		title,content = self.getItems(pageIndex)
		pagenow = self.pageIndex
		# nu = len(title)
		nu = len(content)
		# print content
		# type(nu)
		for i in range(nu):
		#wait users to comfirm
			comfirm = raw_input()
			if comfirm == 'Q':
				print '程序结束'
				return None
			else:
				if self.nextpage == False:
					print i,title[i],i,content[i]
					if i == nu-2:
						self.nextpage = True
						pagenow +=1
						#call getOnestory()again to get to next page
						self.getOnestory(pagenow)
	#start
	def startsp(self):
		print '正在读取...'
		self.getOnestory(self.pageIndex)
		
spider = QSBK()
spider.startsp()

				
					
		
		
