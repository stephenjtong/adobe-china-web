import http.client



#读取网页。不能处理https
def readURL(url,retry=10,timeout=30):
	if 'http://' in url: url=url[7:]
	baseurl=url[:url.find('/')]
	path=url[url.find('/'):]
	for r in range(retry):
		try:
			conn=http.client.HTTPConnection(baseurl,timeout=timeout)
			conn.request('GET',path)
			res=conn.getresponse()
			if res.status==200:return [200,str(res.read())]
			else: return res.status
		except:
			pass