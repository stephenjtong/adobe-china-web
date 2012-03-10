import os
#import sys

#sys.setrecursionlimit(100000)
def getFileList(path='.'):
	for fileName in os.listdir ( path ):
		print (fileName+'|'+str(os.path.isdir(fileName)))
		if fileName.find('_BAK')!=-1 and fileName.find('_BAKs')==-1:
			print(fileName)
		if (os.path.isdir(fileName) and (fileName!='_notes')and  fileName!= '_bak'):
			listfiles(fileName)

listfiles()