# Author: Jishi Tong
# Email: tjishi@adobe.com
# Last update: 2011-01-05
# Getting project status from skippy.adobe.com

filename='list.txt'  #default file name of agenda.
log='log.txt'  #the file name to save the report
retry=10  #retry times if fail connection
t1=['FR','DE','JP','UK','SE']
t2=['IT','NO','DK','FI','NL','ES']
t3=['BR','KR','CN','TW','HK_ZH','LA','MX','CAFR','MENA','EEUROPE','SEA','AP','AFRICA']
t4=['EE','LT','LV','SK','HU','BG','CZ','HR','PL','RO','RS','RU','SI','TR','UA']

def unescape(s):
  s = s.replace("&lt;", "<")
  s = s.replace("&gt;", ">")
  s = s.replace("&#34;", '"')
  s = s.replace("\\r\\n",'\n')
  s = s.replace("\\n",'\n')
  s = s.replace("\\t", "\t")
  # this has to be last:
  s = s.replace("&amp;", "&")
  return s

import urllib.request,urllib.parse,re,http.cookiejar,getpass, codecs
import xlwt3 as xlwt
from datetime import datetime

_monthnames = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July',
               'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
while True:
  try:
    f=open(filename,'rb')
    content=f.read()
    pt=re.compile(r'Project No.\s*([\d\w-]+)')
    project_list=list(re.findall(pt,str(content)))
    total=len(project_list)
    if total==0:
      print('No project name found in "'+filename+'", please check and input the agenda file name: ')
      filename=input().strip()
      continue
    print(str(total)+' projects in total.')
    break
  except exception as e:
    filename=input().strip()

description_needed=True
log=open(log,'w')

wb = xlwt.Workbook()
ws = wb.add_sheet('Result')
strStyle = xlwt.easyxf('font: name Calibri')
dateStyle = xlwt.easyxf('font: name Calibri',num_format_str='YY/MM/DD')

ws.write(0, 0, 'Project Id', strStyle)
ws.write(0, 1, 'Status', strStyle)
ws.write(0, 2, 'Start Date', strStyle)
ws.write(0, 3, 'Due Date', strStyle)
ws.write(0, 4, 'Countries involved', strStyle)
ws.write(0, 5, 'Countries done', strStyle)
ws.write(0, 6, 'Countries staged', strStyle)
ws.write(0, 7, 'In progress', strStyle)
ws.write(0, 8, 'Idiom', strStyle)
ws.write(0, 9, 'Description', strStyle)
ws.write(0, 10, 'Notes', strStyle)
ws.write(0, 11, 'Priority', strStyle)
ws.write(0, 12, 'Link', strStyle)

total=len(project_list)

cookie=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
urllib.request.install_opener(opener)

while True:
  print('Username: ')
  username=input().strip()
  psd=getpass.getpass().strip()
  params=urllib.parse.urlencode({"username":username,"password":psd,"login":1,"submit":"login"})
  params=params.encode()
  print('Connecting and authenticating to skippy...')

  i=0
  while i<retry:
    try:
      f=urllib.request.urlopen('https://skippy.adobe.com/cgi-bin/admin.cgi',params)
      break
    except Exception as e:
      print(str(e))
      i=i+1
  if(i==retry):
    print('Connection error after '+str(retry)+' retries1')
    exit()

  i=0
  while i<retry:
    try:
      f=urllib.request.urlopen('https://skippy.adobe.com/cgi-bin/admin.cgi',params)
      break
    except:
      i=i+1
  if(i==retry):
    print('Connection error after '+retry+' retries2')
    exit()
  if(re.search('Quick search',str(f.read()))!=None):break
  else:print('Wrong username or password.')

count=0

for p in project_list:
  count=count+1
  print('('+str(count)+'/'+str(total)+') Grabing '+p+' ...')
  urlpars=urllib.parse.urlencode({'jumpto':p})
  
  i=0
  while i<retry:
    try:
      f=urllib.request.urlopen('https://skippy.adobe.com/cgi-bin/admin.cgi?%s'%urlpars)
      break
    except:
      i=i+1
  if(i==retry):
    print(p+' Connection error after '+retry+' retries')
    continue

  content=str(f.read())
  if re.search(r'Project with ID.*does not exists',content)!=None:
    print('Wrong project number, please check')
    continue  
  try:countries_involve=re.search(r'Countries Involved.*?<div class="columns-2-aaB-B">.*?(?:<b>)?(.*?)<br>',content).group(1)
  except:countries_involve=''
  try:priority=re.search(r'name="priority" value="(..)" checked>',content).group(1)
  except:priority='N/A'
  if '<select'in countries_involve:countries_involve=''
  countries_involve=str(countries_involve).replace('</b>','')
  countries_involve=countries_involve.replace('<b>','')
  
  if_done=re.search(r'No more changes can be made to the project.',content)!=None
  try:status=re.search(r'name="status" value="([^<>]*?)" checked="checked" />',content).group(1)
  except:status='Done'  
  try:title=re.search(r'<label for="name">Name:</label>.*?<input id="shortDesc" type="text" name="shortDesc" value="(.*?)" size="40">',content).group(1)
  except:title=re.search(r'<label for="name">Name:</label>.*?<div class="columns-2-aaB-B">\\n\s*(.*?)\\n ',content).group(1)
  start_date=re.search(r'<label for="start_date">Start date:</label>.*\n.*\n.*\n(.*)\n',unescape(content)).group(1).strip()
  month_due=re.search(r'name="monthDue".*?selected="selected".*?>(.*?)<',content).group(1)
  day_due=re.search(r'name="dayDue".*?selected="selected".*?>(.*?)<',content).group(1)
  year_due=re.search(r'name="yearDue".*?selected="selected".*?>(.*?)<',content).group(1)
  due_date=month_due+' '+day_due+' '+year_due
  description=re.search(r'<h3>Description</h3>.*?textarea.*?>(.*?)</textarea>',content).group(1)
  remarks=re.search(r'<h3>Remarks:</h3>.*?textarea.*?>(.*?)</textarea>',content).group(1)
  try:countries_ready=re.search(r'Countries Ready.*?<div class="columns-2-aaB-B">.*?n\s*(.*?)<br>',content,re.S).group(1)
  except:countries_ready=''
  countries_staged=str(re.findall(r'\d{8}.*?&gt;([^\\]*?)staged?',content,re.S))
  countries_staged=re.split(r"['|\[|\]|\s|,| ]",countries_staged)
  countries_ready_temp=countries_ready.split(',')
  if 'T1' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t1
  if 'T2' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t2
  if 'T3' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t3
  if 'T4' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t4
  countries_staged=[i for i in countries_staged if i!='' and i not in countries_ready_temp]
  countries_staged=re.sub(r"[\[|\]|']",'',str(countries_staged))
  
  countries_ready_temp=countries_staged.split(', ')+countries_ready.split(',')
  if 'T1' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t1
  if 'T2' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t2
  if 'T3' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t3
  if 'T4' in countries_ready_temp: countries_ready_temp=countries_ready_temp+t4
  
  countries_involve_temp=countries_involve.replace(' ','').split(',')
  if 'T1' in countries_involve_temp: countries_involve_temp=countries_involve_temp+t1
  if 'T2' in countries_involve_temp: countries_involve_temp=countries_involve_temp+t2
  if 'T3' in countries_involve_temp: countries_involve_temp=countries_involve_temp+t3
  if 'T4' in countries_involve_temp: countries_involve_temp=countries_involve_temp+t4
  countries_not_ready=[i for i in countries_involve_temp if i not in countries_ready_temp]
  countries_not_ready=re.sub(r"[\[|\]|']",'',str(countries_not_ready))
  countries_not_ready=re.sub(r'(T1,|T2,|T3,|T4,)','',countries_not_ready)
  
  try:idiom_name=re.search(r'(?:WorldServer|Idiom project name).*?([\d\w_-]+)',unescape(content),re.I|re.S).group(1)
  except:idiom_name=''
  #print(idiom_name)


  ########## write to file ############
  log.write(p+' - '+unescape(title)+'\n')
  ws.write(count, 0, p+' - '+unescape(title), strStyle)
  if if_done:
    log.write('**CLOSED**'+'\n')
    ws.write(count, 1, 'Done', strStyle)
  else:
    ws.write(count, 1, status, strStyle)
  log.write('Priority: '+priority+'\n')
  log.write('Start Date: '+ start_date+'\n')
  try:[mm, dd, yy] = start_date.split(' ')
  except Exception as e:
    err=open('error.log','a')
    err.write('https://skippy.adobe.com/cgi-bin/admin.cgi?Tabs=project&jumpto='+p)
    
  ws.write(count, 2, datetime(int(yy), _monthnames.index(mm)+1, int(dd)), dateStyle)

  log.write('Due Date: '+due_date+'\n')  
  [mm, dd, yy] = due_date.split(' ')
  ws.write(count, 3, datetime(int(yy), _monthnames.index(mm)+1, int(dd)), dateStyle)
  
  log.write('Countries involved: '+ str(countries_involve)+'\n')
  ws.write(count, 4, str(countries_involve), strStyle)
  log.write('Countries Ready: '+ str(countries_ready)+'\n')  
  ws.write(count, 5, str(countries_ready), strStyle)
  log.write('Countries Staged: '+ str(countries_staged)+'\n')
  ws.write(count, 6, str(countries_staged), strStyle)
  log.write('Countries NOT ready nor staged: '+str(countries_not_ready)+'\n')
  ws.write(count, 7, str(countries_not_ready), strStyle)
  log.write('Idiom Name: '+idiom_name+'\n')
  ws.write(count, 8, idiom_name, strStyle)
  log.write('-'*10+'\n')
  log.write(unescape(description)+'\n')
  ws.write(count, 9, unescape(description),strStyle)
  log.write('-'*10+'\n')
  log.write(unescape(remarks)+'\n')
  ws.write(count, 10, unescape(remarks),strStyle)
  ws.write(count, 11, priority, strStyle)
  ws.write(count, 12, 'https://skippy.adobe.com/cgi-bin/admin.cgi?Tabs=project&jumpto='+p)
  log.write('\n'+'='*80+'\n')
  log.flush()
  wb.save('result.xls')

