import http.client

list=open('list.txt','r').readlines()
list=[l.strip() for l in list]
r=open('record.txt','a')
i=0
for l in list:
  i=1+i
  print(str(i)+' '+l)
  conn = http.client.HTTPConnection('www.adobe.com')
  conn.request("HEAD",l)
  res = conn.getresponse()
  if res.status==200:
    r.write(l+'\tOK\n')
    print('\tOK')
  elif res.status==301 or res.status==302:
    status=str(res.status)
    try:
      location=dict(res.getheaders())['Location']
    except:
      location=dict(res.getheaders())['location']
    r.write(l+'\t'+status+'\t'+location+'\n')
    print('\t'+status+'\t'+location)
  else:
    r.write(l+'\t'+str(res.status)+'\n')
    print('\t'+str(res.status))