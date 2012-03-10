'''
	This script reports any localized pages are availiable but without localized link on.
	Results will write to file 'log.txt'.	
'''

import re,urllib.request
from utls import * 

list=[i.strip() for i in open('list.txt','r').readlines()]
#list=[i.replace('www.adobe','www.stage.adobe') for i in list]
log=open('log.txt','w')
total=len(list)
num=0
error=open('error.log','w')
#eeurope=['ee','hu','lt','lv','sk','ro','si','rs','hr','tr']

for l in list:
	try:geo=re.search(r'\.com/(..)',l).group(1)
	except:continue
	
	num+=1
	print('('+str(num)+'/'+str(total)+') '+l)
	log.write(l+':\n')
	try:content=str(urllib.request.urlopen(l).read())
	except:pass
	pt=re.compile(r'<a[^<>]*href="([^"]*)[^>]*>([^<]*)')
	links=re.findall(pt,content)
	links=[(u,l) for u,l in links if '/go/' not in u and 
		'/cfusion/' not in u and 
		'/devnet' not in u and 
		'javascript' not in u and
		'/dam/' not in u and
		'/content/dotcom' not in u and
		'mailto' not in u and
		not re.search('^/../',u) and
		not re.search('adobe.com/../',u) and
		('www.adobe.com' in u or u[0]=='/')]
	#links=[i for i in links if (i[0][0]=='/')]
	#print(str(links))
	linkcount=0
	totallink=len(links)
	tel=re.findall(r'[\d\s.]{5,13}',content)
	#log.write('\n'.join(tel)+'\n')
	for link in links:
		url,title=link[0],link[1].strip()
		linkcount+=1
		print('\t('+str(num)+'/'+str(total)+') '+'('+str(linkcount)+'/'+str(totallink)+') '+title,'\n\t\t'+url)
		if url.find('/')==0:
			#if url.find('/go/')!=-1:
				#do something for /go/url
			if re.search('"/../',url)==None:
				if getLinkStatus('/'+geo+url)==200:
					log.write('\t'+title+'\t'+url+'\n')
		if 'www.adobe.com' in url:
			if re.search('adobe\.com/../',url)==None:
				if getLinkStatus('/'+geo+re.search('adobe\.com(.*)',url).group(1))==200:
					log.write('\t'+title+'\t'+url+'\n')
		if '/eeurope/' in url:
			if getLinkStatus(url.replace('eeurope',geo))==200:
				log.write('\t'+title+'\t'+url+'\n')
		if 'www.stage' in url:
			log.write('\t'+title+'\t'+url+'\n')
		'''if 'www.stage.adobe.com' in url:
			log.write('\t'+title+'\t'+url+'\n')'''
			
	log.write('='*50+'\n')
