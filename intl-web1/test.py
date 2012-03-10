from html.parser import HTMLParser
import http.client

#不能处理https
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
	

class Spider(HTMLParser):
	def __init__(self, url):
			HTMLParser.__init__(self)
			#req = urlopen(url)
			c=readURL('http://www.adobe.com/devnet/flashplayer/articles/secure_swf_apps.html')
			try:self.feed(c)
			except:pass

	def handle_starttag(self, tag, attrs):
			if tag == 'meta' and attrs:
				  print ("Found link => %s" % attrs)
Spider('http://www.hellboundhackers.org')