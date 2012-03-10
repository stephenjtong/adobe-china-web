import os
from utls import * 

def processfile(dir,pushlist,linkcheck,topdown=True):
	for root, dirs, files in os.walk(dir, topdown):
		for name in files:
			filename=os.path.join(name)
			fullpathname=os.path.join(root,name)
			if '.ssi' in filename or '.html' in filename:
				#print(fullpathname)
				asteriskFile(fullpathname)
				pushlist.write(formatFilename(fullpathname)+'\n')
				result=checkLinks(fullpathname)
				linkcheck.write('===='+formatFilename(fullpathname)+'====\n')
				linkcheck.write(formatResult(result)+'\n')
			elif 'omega' in root: 
				pushlist.write(formatFilename(fullpathname)+'\n')
				
dir = os.getcwd() 
pushlist = open('pushlist.txt','w')
linkcheck=open('linkcheck.txt','w')
processfile(dir,pushlist,linkcheck)