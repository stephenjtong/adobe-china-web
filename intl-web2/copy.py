import os
import shutil

l=open('list.txt','r')
lines=l.readlines()
lines=[l.strip() for l in lines]
base='/data/www/sites/www-staging.adobe.com/docs'

for l in lines:
	dir=os.getcwd()
	p=l.split('/')
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