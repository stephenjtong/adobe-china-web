#用于抓取所给网页中的meta data

import http.client
import re

def getMetas(url):
	conn = http.client.HTTPSConnection('www.adobe.com', timeout=30)
	conn.request("GET",url)
	res = conn.getresponse()
	content=str(res.read())
	p=re.compile('<(title)>(.*)</title>')
	results=p.findall(content)
	p=re.compile('<meta.*?name="(.*?)".*?content="(.*?)"')
	results=results+p.findall(content)
	p=re.compile('InstanceParam.*?name="(.*?)".*?value="(.*?)"')
	results=results+p.findall(content)
	url=url.strip()
	#print(results)
	results=results+[('url','www.adobe.com'+url)]
	#print(results)
	d=dict(results)
	return d


f=open('list.txt','r')
meta=open('metas.txt','w')
e=open('error.txt','w')
pages=f.readlines()
total=len(pages)
count=0
d=dict()
for page in pages:
	count=count+1
	succ=0
	retry=0
	print('('+str(count)+'/'+str(total)+')'+page)
	while succ==0:
		retry=retry+1
		try:
			rs=getMetas(page[20:])
			for r in rs:
				try:
					d[r][count]=rs[r]
				except:
					d[r]={count:rs[r]}
			#meta.write('\n')
			succ=1
		except:
			if retry>300:break  #retry 30 times
			print(str(retry),end=' ')
	print()
	if succ==0:
		#e.write(page)
		e.write('error: '+str(retry)+'   '+page)

for item in d:
	meta.write(item+'\t')
meta.write('\n')

for i in range(1,count+1):
	for item in d:
		try:meta.write(d[item][i]+'\t')
		except:meta.write(''+'\t')
	meta.write('\n')

	
#print(d)

		
