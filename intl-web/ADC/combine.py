
#将meta输出的结果与序号结合

number=open('number.txt','r')
num=number.readlines()
num.pop(0)
num=[n.split() for n in num]
num=dict(num)
e=open('error.txt','w')
print(num)

m=open('metas.txt','r')
rlines=m.readlines()

c=open('combine.txt','w')
c.write('No.\t'+rlines.pop(0))
for l in rlines:
	url=l.split('\t')[43]
	try:
		c.write(num[url]+'\t'+l)
	except:
		e.write(url)
	