import os
from utls import * 

def processfile(dir,pushlist,linkcheck,topdown=True):
	for root, dirs, files in os.walk(dir, topdown):
		for name in files:
			filename=os.path.join(name)
			fullpathname=os.path.join(root,name)
			if '.ssi' in filename or '.html' in filename or '.xml' in filename:
				#print(fullpathname)
				asteriskFile(fullpathname)
				result=checkLinks(fullpathname)
				oldname=fullpathname
				fullpathname=re.sub(r'summary.html','index.html',fullpathname)
				os.rename(oldname,fullpathname)
				pushlist.write(formatFilename(fullpathname)+'\n')
				linkcheck.write('===='+formatFilename(fullpathname)+'====\n')
				linkcheck.write(formatResult(result)+'\n')
			elif 'omega' in root: 
				pushlist.write(formatFilename(fullpathname)+'\n')
				
dir = os.getcwd() 
pushlist = open('pushlist.txt','w')
linkcheck=open('linkcheck.txt','w')
processfile(dir,pushlist,linkcheck)