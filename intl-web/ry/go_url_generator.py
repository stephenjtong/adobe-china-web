import xml.etree.ElementTree as etree
import re
import http.client
import codecs

def process_geos(geos):
  geos=re.split(r"[\s,]",geos)
  geos=[g for g in geos if g!='']
  return geos

  
def getLinkStatus(url,baseurl='www.stage.adobe.com', timeout=30):
	retry=0
	while retry<30:
		try:
			if url.find('https://')==0:	
				tempurl=url.split('/')
				tempbase=tempurl[2]
				try:
					tempurl='/'+tempurl[3].split('?')[0]
				except:
					tempurl='/'
				conn = http.client.HTTPSConnection(tempbase, timeout=timeout)
				conn.request("HEAD",tempurl)
			##################??http###############
			elif url.find('http://')==0:
				tempurl=url.split('/')
				tempbase=tempurl[2]
				try:
					tempurl='/'+tempurl[3].split('?')[0]
				except:
					tempurl='/'
				conn = http.client.HTTPConnection(tempbase, timeout=timeout)
				conn.request("HEAD",tempurl)
			##################???????################
			elif url.find('/')==0:
				conn = http.client.HTTPConnection(baseurl, timeout=timeout)
				conn.request("HEAD",url)
			else: #???????
				tempurl='error' 
				try:tempurl=r2a(filename,url)
				except:pass #???ssi??,raise??exception
				conn = http.client.HTTPConnection(baseurl, timeout=timeout)
				conn.request("HEAD",tempurl)
			res = conn.getresponse()
			return res.status
		except Exception as e:
			retry=retry+1
			print('Error: '+str(e))
	return 404


f=open('result.txt','w')
  

tree = etree.parse('go.xml')
root = tree.getroot()
baseurl=root.get('base')
for child in root:
  gourl=child.find('gourl').text
  des=child.find('destination').text
  geos=child.find('geos').text
  geos=process_geos(geos)
  for g in geos:
    d='/'+g+des
    print('testing '+d)
    if getLinkStatus(d,baseurl)==200 or getLinkStatus(d,baseurl)==301:
      f.write(gourl+'_'+g+'\t'+'/'+g+des+'\n')
    else:
      f.write(gourl+'_'+g+'\t'+des+'\n')
    
  



