import re
import codecs

def genPushList(filename): 
	f=codecs.open(filename,"r","utf-8")
	content=str(f.read())
	content=content.replace('\\','/')
	#print(content)
	p=re.compile('mm_filename=".*/(../.*?)"')
	pushlist=list(set(p.findall(content)))
	temp=pushlist[:]
	for file in temp:
		if '_bak' in file.lower(): pushlist.remove(file)
	#print(str(pushlist))
	return pushlist

pushlist=genPushList('ResultsReport.xml')
f=open('pushlist.txt','w')
for file in pushlist:
	f.print(file)
