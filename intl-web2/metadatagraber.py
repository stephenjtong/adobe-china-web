import http.client
import re


def getMetas(url):
	conn = http.client.HTTPSConnection('www.adobe.com', timeout=30)
	conn.request("GET",url)
	res = conn.getresponse()
	content=str(res.read())
	p=re.compile('<(title)>(.*)</title>')
	results=p.findall(content)
	p=re.compile('<meta.*?name="(.*?)".*?content="(.*?)"',re.S)
	results=results+p.findall(content)
	p=re.compile('<InstanceParam.*?name="(.*?)".*?value="(.*?)"',re.S)
	results=results+p.findall(content)
	d=dict(results)
	return d


f=open('list.txt','r')
meta=open('metas.txt','w')
e=open('error.txt','w')
pagess=f.readlines()
for page in pagess:
	print(page)
	try:
		rs=getMetas(page[20:])
		meta.write(page)
		for r in rs:
			meta.write(r+'\t'+rs[r]+'\n')
		meta.write('\n')
	except:e.write(page)

		
