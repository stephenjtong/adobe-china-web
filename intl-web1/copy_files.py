#copy files to current directory

import os
import shutil

l=open('copy_list.txt','r')
lines=l.readlines()
lines=[l.strip() for l in lines]
base=os.getcwd()

for l in lines:
	dir=os.getcwd()
	p=l.split('/')
	#p[0]='mena'  #!!!!
	for path in p:
		if path!=p[-1]:
			dir=os.path.join(dir,path)
			try:os.mkdir(dir)
			except:pass
		if path==p[-1]:
			try:
				src=os.path.join(base,l)
				shutil.copy(src,dir)
			except:
				print(l)