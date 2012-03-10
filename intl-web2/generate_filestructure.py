'''
create a file structure for a push list
if the file existed, will backup the old one, with a '_BAK' and a timestamp attached to the file name
'''
import os
import shutil
import time

r=open('push.txt','r')
lines=r.readlines()
lines=[l.strip() for l in lines]
index=[l+'index.html' for l in lines if l.endswith('/')]
others=[l for l in lines if not l.endswith('/')]
lines=index+others
lines=[l for l in lines if l!='']

for line in lines:
	root=os.getcwd()
	p=line.split('/')
	lenth=len(p)
	for path in p:
		if path!=p[-1]:
			root=os.path.join(root,path)
			try:os.mkdir(root)
			except:print('error: "'+root+'" already exists')
		if path==p[-1]:
			try:
				open(os.path.join(root,path),'r')
				shutil.copy(os.path.join(root,path),os.path.join(root,path.replace('.','_BAK_'+time.strftime("%Y%m%d%H%M",time.localtime())+'.')))
				open(os.path.join(root,path),'w')
			except:
				open(os.path.join(root,path),'w')