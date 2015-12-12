# _*_ coding:utf-8 _*_
import urllib
import urllib2
import re
import os

# import requests

#处理页面标签类
class Tool:
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

class MX(object):
	#init
	def __init__(self):
		self.baseURL = 'http://mingxing.com/tuku/mote'
		self.tool = Tool()
		self.user_agent = 'Mozilla 5.0'
		self.headers = {'User-Agent':self.user_agent}
	#get page
	def getPage(self):
		try:	
			# print self.baseURL
			#request
			request = urllib2.Request(self.baseURL,headers = self.headers)
			#response
			response = urllib2.urlopen(request)
			# response = requests.get(self.baseURL)
			page = response.read().decode('utf-8')
			# print page
			return page
		except urllib2.URLError, e:
			if hasattr(e,'reason'):
				print '连接失败',e.reason
				return None
	#get information
	def getInfo(self):
		page = self.getPage()
		#imgurl pattern
		iconURLP = re.compile('li.+?<img src="(.+?)".+?</i>',re.S)
		iconURL = re.findall(iconURLP,page)
		# print imgURL
		#name pattern
		nameP = re.compile('<h5>(.+?)</h5>',re.S)
		name = re.findall(nameP,page)
		# print name
		return iconURL,name
	#the detail of the icon img
	def getDetail(self):
		page = self.getPage()
		detailImgPT = re.compile('<li>.+?href="(.+?)" target.+?</li>',re.S)
		detailImg = re.findall(detailImgPT,page)
		# print detailImg,type(detailImg)
		# print len(detailImg)
		return detailImg
	#get detail page img number
	def DetailPageImgNu(self,detailurl):
		# print detailurl
		request = urllib2.Request(detailurl)
		r = urllib2.urlopen(request)
		DP = r.read().decode('utf-8')
		# print DP
		pt = re.compile('totalpage.+?= (.+?);',re.S)
		nu = re.findall(pt,DP)
		# print 'nu is ',nu[0],type(nu)
		return nu[0]
	#get detail page img
	def getDPImg(self,dpurl):
		print dpurl
		req = urllib2.Request(dpurl,headers = self.headers)
		r = urllib2.urlopen(req)
		DP = r.read().decode('utf-8')
		# print DP
		dpimgurlpt = re.compile('<img onload.+?src="(.+?)".+?</a>',re.S)
		dpimgurl = re.findall(dpimgurlpt,DP)
		# print dpimgurl[0]
		return dpimgurl[0]
	# write name and save img
	def saveImg(self,imageURL,name,nu = 0):
		u = urllib2.urlopen(imageURL)
		fileName = name + '/' + name + str(nu) +'.jpg'
		data = u.read()
		f = open(fileName,'wb')
		f.write(data)
		print u'保存图片为：',fileName
		f.close()
	# write content
	# def saveContent(self,content,name):
		# fileName = name +"/" +name+'.txt'
		# f = open(fileName,'w+')
		# print '正在保存信息..',fileName
		# f.write(content.encode('utf-8'))
	#creat new path
	def mkdir(self,path):
		path = path.strip()
		# judge the existence of the path
		#if exist, True if not, False
		isExists=os.path.exists(path)
		# judgment
		if not isExists:
			#if not exists,creat the path
			os.makedirs(path)
			return True
		else:
			return False
	#start 
	def start(self):
		imgURL, name = self.getInfo()
		detailimg = self.getDetail()
		# print len(name),len(detailimg)
		for i in range(len(name)):
		# for i in range(12,13):
			print 'the',i,'lady',name[i]
			self.mkdir(name[i])
			self.saveImg(imgURL[i],name[i])
			dpnu = int(self.DetailPageImgNu(detailimg[i]))
			# print detailimg[i],self.DetailPageImgNu(detailimg[i])
			# print dpnu
			# print dpnu,type(dpnu)
			for j in range(1,dpnu+1):
				if j == 1:
					# the first page url
					dpurl = detailimg[i] +'index.html'
				else:
					# the other pages url
					dpurl = detailimg[i] +str(j)+'.html'
				# print 'j is ',j
				dpimgurl = self.getDPImg(dpurl)
				# print dpimgurl
				self.saveImg(dpimgurl,name[i],j)
			print '------------------------'+ str(i) +'-----------------------'
			
				
		# self.getDPImg(detailimg[0])			
			
mingxing = MX()
mingxing.start()			