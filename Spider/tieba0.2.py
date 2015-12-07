#_*_ coding:utf-8 _*_
#bdte now adding get the content
import urllib
import urllib2
import re

#tool to remove tags form BDTB
class Tool:
	#remove img tag, 7 bit blank
	removeImg = re.compile('<img.*?>| {7}|')
	#remove super link tag 
	removeAddr = re.compile('<a.*?>|</a>')
	#replace tag \n to string '\n'
	replaceLine = re.compile('<tr>|<div>|</div>\</p>')
	#replace tag \t to '\n'
	replaceTD = re.compile('<td>')
	#replace para or item's beginning to \n and two blanks
	replacePara = re.compile('<p.*?>')
	#replace \n or double \n to '\n'
	replaceBR = re.compile('<br><br>|<br>')
	#remove the rest of tags
	removeExtraTag = re.compile('<.*?>')
	def replace(self,x):
		x = re.sub(self.removeImg,"",x)
		x = re.sub(self.removeAddr,"",x)
		x = re.sub(self.replaceLine,"\n",x)
		x = re.sub(self.replaceTD,"\t",x)
		x = re.sub(self.replacePara,"\n  ",x)
		x = re.sub(self.replaceBR,"\n",x)
		x = re.sub(self.removeExtraTag,"",x)
		#strip() will del all extra content
		return x.strip()

#BDTB project
class BDTB:
	#init baseURL and seeLZ only
	def __init__(self,baseURL,seeLZ,floorTag):
		self.baseURL = baseURL
		self.seeLZ = seeLZ
		# '?see_lz=' + str(seeLZ)
		#call other project Tool
		self.tool = Tool()
		#floor now
		self.floor = 1
		#global file for open and wirte
		self.file = None
		#default title
		self.defaultTitle = '百度贴吧'
		# whether write char of separate each floor
		self.floorTag = floorTag
		
	#get the code of the pagenum
	def getPage(self,pageNum):
		try:
			if self.seeLZ == '0':
				self.seeLZ = None
				url = self.baseURL + '?&pg=' + str(pageNum)
			else:
				url = self.baseURL + '?see_lz=' + str(self.seeLZ) + str(pageNum)
				# url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
			print url
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			# print response.read()
			# print type(response)
			Page = response.read().decode('utf-8')
			# print type(Page)
			return Page
		except urllib2.URLError, e:
			if hasattr(e,'reason'):
				print '连接贴吧失败',e.reason
				return None
	# get the title
	def getTitle(self,Page):
		# page = self.getPage(1)
		# print page
		pattern = re.compile('<h3\sclass="core_title.*?title=".*?>(.*?)</h3>',re.S)
		#result take ablity from re.search object, just get one result enught
		result = re.search(pattern,Page)
		# print result.group(),type(result)
		if result:
			# print result.group(1)
			# print type(result.group()),type(result.group().strip())
			#here should return a  value not list of result
			return result.group(1).strip()
		else:
			return None
	# get the pageNuber
	def getPageNum(self,Page):
		# page = self.getPage(1)
		pattern = re.compile('<li class="l_reply.*?<span class="red">(\d+)</span>',re.S)
		pagenub = re.search(pattern,Page)
		print pagenub.group(1)
		if pagenub:
			return pagenub.group(1).strip()
		else:
			return None
	#get the content
	# def getContent1111111111(self,pageNum):
		# page = self.getPage(pageNum)
		# pattern = re.compile('<div id="post_content.+?>(.+?)</div>',re.S)
		# get all the result
		# items = re.findall(pattern,page)
		# for item in items:
			# print item
		# print self.tool.replace(items[1])
		# floor = 1
		# for item in items:
			# print floor,'楼---------------------------------------------------------------------'
			# print self.tool.replace(item)
			# floor +=1
	def getContent(self,Page):
		pattern = re.compile('<div id="post_content.+?>(.+?)</div>',re.S)
		items = re.findall(pattern,Page)
		contents = []
		for item in items:
			#remove the tag, and add \n at the beginning and the endswith
			content = "\n" + self.tool.replace(item)+ "\n"
			contents.append(content.encode('utf-8'))
		return contents
	
	def setFileTitle(self,title):
		if title is not None:
			self.file = open(title + ".txt",'w+')
		else:
			self.file = open(self.defaultTitle + ".txt",'w+')
			
	def writeData(self,contents):
		for item in contents:
			if self.floorTag == '1':
				floorLine = "\n" + str(self.floor) + u"------------------------------------------------\n"
				self.file.write(floorLine)
			self.file.write(item)
			self.floor +=1
			
	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print u'URL 已失效'
			return
		try:
			print '该帖子共有'+ str(pageNum) + '页'
			for i in range(1,int(pageNum)+1):
				print "正在写入" + str(i) + "页数据"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError,e:
			print u'写入异常，原因'+e.message
		finally:
			print u'写入任务完成'

print u'请写入帖子待会'
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
# print baseURL,type(baseURL)
seeLZ = raw_input("是否只获取楼主发言，1-yes,0-no")
# print seeLZ,type(seeLZ)
#此处一直出错时由于将单引号和双引号配对了
#floorTag = raw_input('")
floorTag = raw_input("是否写入楼层信息，1-yes,0-nno")
# print floorTag, type(floorTag)
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()		

	
	
# baseURL = 'http://tieba.baidu.com/p/3138733512'
# bdtb = BDTB(baseURL,1)
# bdtb.getPage(1)
# bdtb.getTitle()
# bdtb.getPageNum()
# bdtb.getContent(1)