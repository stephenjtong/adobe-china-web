#!/usr/bin/python
import urllib.request
import urllib.error
import re

def downURL(url,filename):
    print (url)
    print (filename)
    try:
        fp = urllib.request.urlopen(url)
    except:
        print ('download exception')
        return 0
    op = open(filename,"wb")
    op.write(fp.read())

#downURL('http://www.sohu.com','http.log')

def getURL(url):
    try:
        fp = urllib.request.urlopen(url)
    except:
        print ('get url exception')
        return 0
    
    pattern = re.compile("http://sports.sina.com.cn/[^\>]+.shtml")
    s = fp.read()
    urls = pattern.findall(str(s))
    fp.close()
    return urls

def spider(startURL,times):
    urls = []
    urls.append(startURL)
    i = 0
    while 1:
        if i > times:
            break;
        if len(urls)>0:
            url = urls.pop(0)
            print (url,len(urls))
            downURL(url,str(i)+'.htm')
            i = i + 1
            if len(urls)<times:
                urllist = getURL(url)
                for url in urllist:
                    if urls.count(url) == 0:
                        urls.append(url)
        else:
            break
    return 1
spider('http://www.sina.com.cn',10) 