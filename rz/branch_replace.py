#please turn off read only first

import codecs,re,time

list=open('list.txt','r').readlines()
list=[l.strip() for l in list]

print('\n***Please turn off read only first***\n')

while True:
  print('Please input pattern: ',end='')
  pattern=input().strip()
  print('Please input replace string: ',end='')
  rs=input().strip()
  for file in list:
    try:
      r=codecs.open(file,'r','utf8')
      #print(r.read())
    except Exception as e:
      print('*****'+str(e)+'*****')
    print(file+':\n')
    c=str(r.read())
    pattern=re.sub(r'[\(\)]','',pattern)
    print(pattern)
    for result in re.findall(pattern,c):
      print(result)#+'\t<=='+file+'\n')
  print('These will be replaced, do you wan to proceed?(yes) ',end='')
  confirm=input().strip()
  if confirm=='yes':break
  print()
  
#proceed replace
for file in list:
  try:
    r=codecs.open(file,'r','utf8')
    #print(r.read())
  except Exception as e:
    print('*****'+str(e)+'*****')
  c=str(r.read())
  r.close()
  try:
    w=codecs.open(file,'w','utf8')
    bak=codecs.open(file+'_BAK_'+time.strftime('%Y%m%d_%H%M%S'),'w','utf-8')
  except Exception as e:
    print('*****'+str(e)+'*****')
    exit()
  bak.write(c)
  bak.close()
  c=re.sub(pattern,rs,c)
  w.write(c)
  w.close()
  
  