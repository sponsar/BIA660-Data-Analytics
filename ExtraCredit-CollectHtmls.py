# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,time,os,cookielib

if not os.path.exists("allHTML"):
	os.mkdir("allHTML")

browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

f=open('indeed3.txt')

count=0
for link in f:
	url=link.strip()
	try:
	    response=opener.open(url)    
	except Exception as e:
	    error_type, error_obj, error_info = sys.exc_info()
	    print 'ERROR FOR LINK:',url
	    print error_type, 'Line:', error_info.tb_lineno
	    continue
	html=response.read()
	count+=1
	results=re.finditer('id="resume-contact".*?>(.*?)</h1>',html)
	for result in results:
		name=result.group(1)
		#name=re.sub('/','\:',name)
		fw=open('allHTML/'+name+'.txt','w')
		fw.write(html)
		fw.close()
	print count
f.close()
