# -*- coding: utf-8 -*-
#将所有网址爬下来
import urllib,urllib2,re,sys,time

import urllib
import urllib2
import cookielib

#browser=urllib2.build_opener()
#browser.addheaders=[('User-agent', 'Mozilla/5.0')]

###登录页的url
lgurl = 'https://secure.indeed.com/account/login'
hds = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36' }  

###用cookielib模块创建一个对象，再用urlllib2模块创建一个cookie的handler
cookie = cookielib.CookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookie)

##登录需要提交的表单
pstdata = {'form_tk':'1a5t48smv0mu302l', #填入form_tk
	'email':'406665325@qq.com', #填入网站的用户名
	'password':'sponsar1029', #填入网站密码
	}
dt = urllib.urlencode(pstdata) #表单数据编码成url识别的格式
req = urllib2.Request(url = lgurl,data = dt,headers = hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
response = opener.open(req)#请求网页，返回句柄
page = response.read()#读取并返回网页内容



fileWriter=open('indeed.txt','w')

StartWith=0#0,50,100,150
LinkNum=StartWith

while True:
	url="http://www.indeed.com/resumes?q=%22data+scientist%22&co=US&start="+str(StartWith) 
	try:
	    response=opener.open(url)
	except Exception as e:
	    error_type, error_obj, error_info = sys.exc_info()
	    print 'ERROR FOR LINK:',url
	    print error_type, 'Line:', error_info.tb_lineno
	    break
	#time.sleep(1)
	html=response.read()
	if html.find("The page you are looking for was not found.")!=-1: break
	results=re.finditer('data-tn-link.*?href="(.*?)sp=0".*?rel="nofollow"',html)
	for result in results:
	    fileWriter.write("http://www.indeed.com"+result.group(1)+'\n')
	    LinkNum+=1
	StartWith+=50
	print "total links",LinkNum
print "finish"
fileWriter.close()
