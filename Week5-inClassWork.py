# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:50:00 2015

@author: sponsar
"""

import urllib2,re,sys,time

browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

infile=open("in.txt")
link=infile.readline().strip()
infile.close()

count=0
page=1
while True:
    url=link+'/ref=cm_cr_pr_btm_link_'+str(page)+'?ie=UTF8&showViewpoints=1&sortBy=recent&reviewerType=all_reviews&formatType=all_formats&filterByStar=all_stars&pageNumber='+str(page)
    #url=link+'/ref=cm_cr_pr_btm_link_'+str(page)+'?ie=UTF8&showViewpoints=1&sortBy=helpful&reviewerType=all_reviews&filterByStar=all_stars&pageNumber='+str(page)
    try:
        response=browser.open(url)    
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR LINK:',url
        print error_type, 'Line:', error_info.tb_lineno
        continue
    
    html=response.read()
    #if re.search('Sorry, no reviews match your current selections',html): break
    if html.find('Sorry, no reviews match your current selections')!=-1:break


    #m=len(re.findall('<span class="a-size-base a-color-secondary review-date">on August(.*?)</span>',html))
    #count+=m
    reviews=re.finditer('<span class="a-size-base a-color-secondary review-date">on August(.*?)</span>',html)
    m=0
    for review in reviews:
        m+=1        
        count+=1
    print 'page',page,m
    page+=1

    time.sleep(2)
print count
fileWriter=open('out.txt','w')
fileWriter.write(str(count))
fileWriter.close()


