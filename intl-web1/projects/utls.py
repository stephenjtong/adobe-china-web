import re
import http.client
import codecs

eeurope=['ee','hu','lt','lv','sk','ro','si','rs','hr','tr']


#相对URL不能处理
#https偶尔会出现异常：socket.error: [Errno 10035] A non-blocking socket operation could not be completed immediately，暂时按404处理
def checkLinks(filename, baseurl='www.stage.adobe.com', timeout=30):
	file=codecs.open(filename,'r','utf-8')
	filename=formatFilename(filename)
	print('Processing file:"'+filename+'", checking links ...')
	url404=set()
	url200=set()
	url301=set()
	p=re.compile('<a.*?href="([^#]*?)"',re.S)
	urls=p.findall(str(file.read()))
	urls=list(set(urls)) #过滤重复URL
	for url in urls:
		#print('-----\n'+url)
		status=getLinkStatus(url,baseurl,timeout)		
		if status==200: url200.add(url)
		elif status==301: url301.add(url)
			#if url.find('/go/')!=-1:url301.add(url) #301重定向只针对go URL，其余URL按404处理
			#else: url404.add(url)
		else: url404.add(url)
		
	#print('==================================================')
	#print('OK urls:'+str(url200))
	#print('redirect urls:'+str(url301))
	#print('error urls:'+str(url404))
	return {'200':url200,'301':url301,'404':url404}

#给某一个file中的所有链接加上GEO code及星号
#1.其中的*号会被double 2.如果GEO code以g开头会有问题
def asteriskFile(filename,baseurl='www.stage.adobe.com'):
	geoCode=getGeoCode(filename)
	file=codecs.open(filename,'r','utf-8')
	f=formatFilename(filename)
	print('Processing file:"'+f+'", adding GEO code and asterisk to links ...')
	content=str(file.read())
	#content=re.sub(r'\*','%%',content) #首先把所有的星号（注释）double
	#content=re.sub(r'/go/buy.*?"',r'/'+geoCode+r'/purchase/"',content) #仅针对没有local store的geo. buy link用local puchase代替
	
	content=re.sub(r'(/products.*?\.ssi)',r'/'+geoCode+r'\1',content) #将所有的ssi文件链接改为本地
	#content=re.sub(r'/..(/ubi/.*?\.ssi)',r'\1',content) #去掉ubi文件上的geo code
	
	content=re.sub(r'(<a.*?href="/)([^#g].*?")',r'\1'+geoCode+r'/\2',content) #全部以"/"开头的非go URL加GEO code
	content=re.sub(r'(<a.*?href="/)"',r'\1'+geoCode+r'/"',content) #修改Homepage
	content=re.sub(r'href="/\w\w/cfusion/',r'href="/cfusion/',content) #不处理/cfusion/链接
	content=re.sub(r'href="(/[^g]./.*?)"(.*?)</a>', asteriskLink,content,flags=re.S) #检查以GEO code开头的链接，如果有坏链则去掉GEO code
	content=re.sub(r'<area.*?href="(/[^g]./.*?)"', asteriskLink,content,flags=re.S) #检查<area .... />中的链接
	content=re.sub(r'([^ ]) *?(</a>)',r'\1\2',content,flags=re.S)#去掉</a>前多余的空格	
	
	'''
	content=re.sub(r'(<a[^<>]*>.*?)(</a>)',r'\1*\2',content,flags=re.S) #全部URL加星号
	content=re.sub(r'(/[^g]./[^<>]*>[^<>]*)\*(</a>)',r'\1\2',content,flags=re.S) #有GEO的链接星号去掉
	content=re.sub(r'(<a.*?>.*?<img.*?)\*(</a>)',r'\1\2',content,flags=re.S) #图片上链接的星号去掉
	content=re.sub(r'(<a[^<>]*button[^<>]*>[^<>]*)\*(</a>)',r'\1\2',content,flags=re.S) #button的星号去掉
	content=re.sub(r'(<a[^<>]*href="#[^<>]*>[^<>]*)\*(</a>)',r'\1\2',content,flags=re.S) #带锚点的链接的星号去掉
	'''
	
	content=re.sub(r'(href="/go/[^"/]+)',r'\1_'+geoCode,content) #将所有的gourl加上_[geoCode]，忽略带promoid的
	content=re.sub(r'href="(/go/.*?)(".*?)</a>',checkgo,content) #检查go url
	
	if 'news.ssi' in f: content=re.sub(r'p>',r'li>',content) #将首页新闻的<p>替换成<li>
	
	#filename=re.sub(r'summary.html','index.html',filename)
	file=codecs.open(filename,'w','utf-8')
	file.write(content)

def checkgo(matchobj):
	ostr=matchobj.group(0)
	link=matchobj.group(1)
	conn = http.client.HTTPConnection('www.stage.adobe.com',timeout=30)
	retry=0
	while retry<30:
		try:
			conn.request("HEAD",link)
			res = conn.getresponse()
		except Exception as e:
			retry=retry+1
			print('Error: '+link+' '+str(e))
	if res.status==301: #go url存在
		return ostr
		#location=dict(res.getheaders())['Location'] #取得跳转页面地址
	else:
		return re.sub(r'_.."',r'"',ostr) 
	
	
def asteriskLink(matchobj):
	ostr=matchobj.group(0)
	link=matchobj.group(1)
	geocode=re.search('/(..)/',ostr).group(1)
	if getLinkStatus(link)==404:
		if geocode in eeurope:
			link=re.sub(r'/\w\w/',r'/eeurope/',link)
			if getLinkStatus(link)==200:
				return re.sub(r'"/\w\w/',r'"/eeurope/',ostr)
			else:
				return re.sub(r'"/\w\w/',r'"/',ostr)
		else:
			return re.sub(r'"/\w\w/',r'"/',ostr)
	else:
		return ostr
	
	
	
def getGeoCode(filename):
	filename=filename.replace('\\','/')
	return re.search('/(..)/',filename).group(1)
	

def formatFilename(filename):
	filename=filename.replace('\\','/')
	filename=re.search('/(../.*)',filename).group(1)
	return filename
	
	
#根据所给的link返回链接的status（200，404等）
def getLinkStatus(url,baseurl='www.stage.adobe.com', timeout=30):
	retry=0
	while retry<30:
		try:
			if url.find('https://')==0:	
				tempurl=url.split('/')
				tempbase=tempurl[2]
				try:
					tempurl='/'+tempurl[3].split('?')[0]
				except:
					tempurl='/'
				conn = http.client.HTTPSConnection(tempbase, timeout=timeout)
				conn.request("HEAD",tempurl)
			##################处理http###############
			elif url.find('http://')==0:
				tempurl=url.split('/')
				tempbase=tempurl[2]
				try:
					tempurl='/'+tempurl[3].split('?')[0]
				except:
					tempurl='/'
				conn = http.client.HTTPConnection(tempbase, timeout=timeout)
				conn.request("HEAD",tempurl)
			##################处理根相对路径################
			elif url.find('/')==0:
				conn = http.client.HTTPConnection(baseurl, timeout=timeout)
				conn.request("HEAD",url)
			else: #链接为相对路径
				tempurl='error' 
				try:tempurl=r2a(filename,url)
				except:pass #如果是ssi文件，raise一个exception
				conn = http.client.HTTPConnection(baseurl, timeout=timeout)
				conn.request("HEAD",tempurl)
			res = conn.getresponse()
			return res.status
		except Exception as e:
			retry=retry+1
			print('Error: '+str(e))
	return 404
	

	
		
		

def genPushList(filename): 
	f=codecs.open(filename,"r","utf-8")
	content=str(f.read())
	content=content.replace('\\','/')
	#print(content)
	p=re.compile('mm_filename=".*/(../.*?)"')
	pushlist=list(set(p.findall(content)))
	temp=pushlist[:]
	for file in temp:
		if '_bak' or 'copy' in file.lower(): pushlist.remove(file)
	print(str(pushlist))
	pushlist.sort()
	return pushlist
	
	

#change reletive path to root reletive path
#ssi中的相对路径无法处理
def r2a(filepath, url):
	filepath=filepath.split('/')
	url=url.split('/')
	if filepath[0]=='': filepath.pop(0)
	if filepath.pop().find('.ssi')!=-1: raise NameError('Cannot handel relitave path in ssi files')
	while url[0]=='..':
		url.pop(0)
		filepath.pop()
	result=str()
	for f in filepath:
		result=result+'/'+f
	for u in url:
		result=result+'/'+u
	result+='/'
	return result

#打印result
def formatResult(list):
	l=str()
	for urls in list:
		l=l+urls+'\n'
		for url in list[urls]:
			l=l+'	'+url+'\n'
	return l


#给定url 返回status和内容
def readURL(url,retry=20,timeout=30):
	if 'http://' in url: url=url[7:]
	baseurl=url.split('/')[0]
	if url.find('/')!=-1:path=url[url.find('/'):]
	else:path='/'
	if path=='': path='/'
	for r in range(retry):
		try:
			#print(baseurl+' '+path)
			conn=http.client.HTTPConnection(baseurl,timeout=timeout)
			conn.request('GET',path)
			res=conn.getresponse()
			if res.status==200:return [200,str(res.read().decode('utf-8'))]
			else: return [res.status,res.read().decode('utf-8')]
		except:
			pass
	print('timeout: '+ url)
	e.write('timeout: '+url+'\n')
	return [000,'000']















	
	