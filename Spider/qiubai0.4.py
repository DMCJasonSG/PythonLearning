# _*_ conding:utf-8 _*_
import urllib
import urllib2
import re
import thread
import time


class QSBK:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0)'
		self.headers = {'User-Agent':self.user_agent}
		self.stories = []
		self.enable = False
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url,headers = self.headers)
			reponse = urllib2.urlopen(request)
			pageCode = reponse.read().decode('utf-8')
			return pageCode
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print '连接糗百失败',e.reason
				return None
	def getTitle(self):
		pageCode = self.getPage(self.pageIndex)
		if not pageCode:
			print '加载失败'
		pattern = re.compile('<div.*?class="author.*?title="(.+?)".*?</a>',re.S)
		Title = re.findall(pattern,pageCode)
		return Title
	def getContent(self):
		pageCode = self.getPage(self.pageIndex)
		if not pageCode:
			print '加载失败'
		pattern = re.compile('<div\sclass="content">(.+?)</div>',re.S)
		Content = re.findall(pattern,pageCode)
		return Content
	def Stories(self):
		title = self.getTitle()
		content = self.getContent()
		for i in range(len(title)):
			print title[i],content[i]
		# print stories
		# nu = len(title)
		# for j in range(nu):
			# del title[0]
			# del content[0]
		# return stories
	# def loadPage(self):
		# if self.enable == True:
			# if len(self.stories)<2:
				# self.pageIndex +=1
			# stories = self.getaStory()
	# def getaStory(self):
		# story = self.Stories()
		# for i in range(len(story)):
			# input = raw_input()
			# self.loadPage()
			# if input == 'Q':
				# self.enable = False
				# return
		# print story
			# del self.stories[0]
	def	start(self):
		print '正在读取糗事百科，按回车查看段子，按Q推出'
		# self.enable = True
		# self.getaStory()
		# nowPage = 1
		# while self.enable:
			# if len(self.stories)>0:
		self.Stories()
			# else:
				# nowPage +=1
		
	# def getPageItems(self,pageIndex):
		# pageCode = self.getPage(pageIndex)
		# if not pageCode:
			# print '页面加载失败'
			# return None
		# pattern = re.compile('<div.*?author.*?title="(.+?)".*?class="content">(.+?)<!--\d+--></div>',re.S)
		# items = re.findall(pattern,pageCode)
		# pageStories = []
		# for item in items:
			# replaceBR = re.compile('<br/>')
			# text = re.sub(replaceBR,"\n",item[i])
			# pageStories.append(item[0].strip(),text.strip(),item[2].strip(),item[4].strip())
			# return pageStories
		
	# def loadPage(self):
		# if self.enable == True:
			# if len(self.stories)< 2:
				# pageStories = self.getPageItems(self.pageIndex)
				# if pageStories:
					# self.stories.append(pageStories)
					# self.pageIndex +=1
				
	# def getOneStory(self,pageStories,page):
		# for story in pageStories:
			# input = raw_input()
			# self.loadPage()
			# if input =='Q':
				# self.enable = False
				# return
			# print "第%d页\t发布人：%s\t赞：%s\n%s"%(page,story[0],story[2],story[3],story[1])
			
	# def start(self):
		# print "正在读取糗事百科，按回车查看段子，按Q推出"
		# self.enable  == True
		# self.loadPage()
		# nowPage = 0
		# while self.enable:
			# if len(self.stories)>0:
				# pageStories = self.stories[0]
				# nowPage +=1
				# del self.sotries[0]
				# self.getOneStory(pageStories,NowPage)
				
spider = QSBK()
spider.start()