from utls import * 

r=open('list.txt','r')
e=open('error.txt','w')
lines=r.readlines()
i=0
for l in lines:
	i=i+1
	print(str(i)+' '+str(getLinkStatus(l,'',30))+' '+l)
	l=l.strip()
	if getLinkStatus(l,'',30)!=200:
		e.write(l+'\n')