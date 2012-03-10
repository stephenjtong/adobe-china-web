import codecs
f=codecs.open("a.txt","r","utf-8")
fileList=f.readlines()
for line in fileList:
    l=line.strip().split('\t')
    f2=codecs.open(l[1],"w","utf-8")
    f2.write(l[0])
