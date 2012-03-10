import re
import codecs

#提取filenames,返回list
def genPushList(filename): 
	f=codecs.open(filename,"r","utf-8")
	content=str(f.read())
	content=content.replace('\\','/')
	#print(content)
	p=re.compile('mm_filename="([^"]*)"')
	pushlist=list(set(p.findall(content)))
	#print(content)
	temp=pushlist[:]
	for file in temp:
		if '_bak' in file.lower() or 'copy' in file.lower(): pushlist.remove(file) #忽略_BAK的大小写
	#print(str(pushlist))
	pushlist.sort()
	return pushlist

pushlist=genPushList('ResultsReport.xml')

#print(str(pushlist))

f=open('pushlist.txt','w')
for file in pushlist:
	f.write(file+'\n')
