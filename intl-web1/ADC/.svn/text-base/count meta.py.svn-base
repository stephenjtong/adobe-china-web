
f=open('log.txt','r')
w=open('count.txt','w')


c=0
lines=f.readlines()
for l in lines:
	c=c+len(l.split('\t'))
	w.write(str(l.split('\t'))+'\n')
print(c)