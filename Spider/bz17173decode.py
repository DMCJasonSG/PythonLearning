# author:DMCJ
# _*_ coding:utf-8 _*_
import urllib
import urllib2
import re
import os

#17173 backgroup image: bizhi
class BZ17173(object):
	#init
	def __init__(self,FirstURL,TotalPageNu):
		# fist formal URL
		self.FirstURL = FirstURL
		# Total page number
		self.TotalPageNu = TotalPageNu
		#headers
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0)'
		self.headers = {'User-Agent':self.user_agent}
	#get page
	def getPage(self,FirstURL,PageNu):
		if PageNu == 0:
			baseURL = FirstURL + 'index.shtml'
			# print baseURL
		else:
			baseURL = FirstURL + 'index_' + str(PageNu) + '.shtml'
		try:
			#request
			re = urllib2.Request(baseURL,headers = self.headers)
			#responce
			r = urllib2.urlopen(re)
			page = r.read() .decode('utf-8','ignore')
			# print page
			return page
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print '连接失败',e.reason
				return None
	#get the list of detail img URL and title
	def getDListUT(self,page):
		# print page
		# the content include url we need
		contentpt = re.compile('<!--content.+?<ul>(.+?)</ul>',re.S)
		contents = re.findall(contentpt,page)
		content = contents[0]
		# print content
		urlpattern = re.compile('<a href="(.+?)".+?</span>',re.S)
		urllist = re.findall(urlpattern,content)
		# for i in range(len(urllist)):
			# print i,urllist[i]
		# print 'urllist done'
		titlepattern = re.compile('<span.+?>(.+?)</a>',re.S)
		titlelist = re.findall(titlepattern,content)
		# for i in range(len(titlelist)):
			# print i,titlelist[i]
		# print 'titlelist done'
		# print titlelist[0],type(titlelist)
		return urllist,titlelist
	# write and save img
	def saveImg(self,imageurl,Title,number):
		i = urllib2.urlopen(imageurl)
		data = i.read()
		fname = Title + '/' + Title + number +'.jpg'
		f = open(fname,'wb')
		f.write(data)
		print 'save img as',Title
		f.close()
	# judge and creat path
	def mkdir(self,path):
		path = path.strip()
		#check if the path exist
		isExists = os.path.exists(path)
		if not isExists:
			print ' creat a new folder as',path
			os.makedirs(path)
			return True
		else:
			print path,' had been created'
			return False
	# edit the url to more detail
	def editURL(self,suburl):
		eurl = ''
		for i in range(len(suburl)):
			#save edit url
			eurl =eurl + suburl[i]
			if suburl[i] == '_':
				# print eurl,type(eurl)
				return str(eurl)
	#get sub page
	def getSubpage(self,suburl):
		#request
		# print suburl
		r = urllib2.Request(suburl,headers = self.headers)
		#responce
		re = urllib2.urlopen(r)
		subpage = re.read().decode('utf-8','ignore')
		# print subpage
		return subpage
	#get sub page number
	def getSubpagenu(self,suburl):
		subpage = self.getSubpage(suburl)
		# print subpage
		#total number of img page pattern
		tnup = re.compile('<a.+?final-page-last.+?="(\d+).+?</a>',re.S)
		#total number fo sub page
		tnu = re.findall(tnup,subpage)
		# print tnu[0],type(tnu[0])
		return int(tnu[0])
	#save sub page's img
	def Savesubimg(self,suburl,title,nu):
		# print '00',suburl
		subpage = self.getSubpage(suburl)
		# print suburl,subpage
		#middle data content to make pattern smaller
		contentpt = re.compile('<div.+?</p>(.+?)<!--.+?-->',re.S)
		contents = re.findall(contentpt,subpage)
		# print contents
		# img pattern
		imgpt = re.compile('url=(.+?)".+?</a>',re.S)
		#img url list
		imgurll = re.findall(imgpt,contents[0])
		# print '00',imgurll[0],imgurll[1]
		for i in range(len(imgurll)):
			self.saveImg(imgurll[i],title,nu +'.'+str(i))
	#get sub page img's url
	def getSubpageUrl(self,suburl,tnu):
		#total number of page
		# print tnu,type(tnu)
		# the before part of the sub url
		basesuburl = self.editURL(suburl)
		#complete sub page url
		comurl = []
		for i in range(1,tnu):
			#middle url to save data
			midurl = basesuburl + str(i) + '.shtml'
			comurl.append(midurl)
			# print comurl[i]
		# print comurl
		return comurl	
	#save each sub page's img
	def SESpage(self,suburl,title,tnu):
		#complete url list
		# print suburl
		completeurlL = self.getSubpageUrl(suburl,tnu)
		for i in range(len(completeurlL)):
			# print completeurlL[i]
			self.Savesubimg(completeurlL[i],title,str(i))
	#start
	def start(self,FirstURL,TN):
		tmpn = TN
		# print tmpn
		for i in range(tmpn+1):
			tump = tmpn -1
			#main page
			page = self.getPage(FirstURL,tmpn)
			# print i
			# print FirstURL,page
			#subpage's urllist and the titlelist
			surllist,titlelist = self.getDListUT(page)
			for j in range(len(surllist)):
				self.mkdir(titlelist[j])
				# print surllist[i],titlelist[i]
				tnu = self.getSubpagenu(surllist[j])
				# print tnu
				self.SESpage(surllist[j],titlelist[j],tnu)
			
				
firsturl = 'http://news.17173.com/gameview/wallpaper/'
#total main page number
T = raw_input('input tatal nuber')
tmpn = int(T)
# print tmpn
bz = BZ17173(firsturl,tmpn)
bz.start(firsturl,tmpn)
		