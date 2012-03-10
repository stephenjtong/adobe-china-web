import re
import http.client

e=open('error.txt','w')

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

sq=r'<a[^<>]*popup[^><]*>'			

p=re.compile(sq,re.I)

log=open('log.txt','w')
f=open('list.txt','r')
links=f.readlines()
links=[l.strip() for l in links]
total=len(links)
counts=0
isfind=False

for link in links:
	counts=counts+1
	print(str(counts)+'/'+str(total))
	print_link=link.replace('.html','_print.html')
	r=readURL(print_link)
	#print(r)
	if r[0]==200:
		content=r[1]
	else:
		r=readURL(link)
		content=r[1]
		if r[0]!=200:
			print(str(r[0])+': '+link)
			e.write(str(r[0])+': '+link+'\n')
		
	content=r[1]
	content=str(content)
	#print(content)
	results=p.findall(content)
	if results==[]:continue
	isfind=True
	results=[r.strip() for r in results]
	log.write(link+'\t')
	for r in results:
		log.write(r+'\t')
	if isfind:log.write('\n')
	
	
