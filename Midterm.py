# -*- coding: utf-8 -*-
"""
Created on Mon Oct 5 22:50:00 2015

@author: sponsar
"""

import urllib2,re,sys,time

browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]
fileWriter=open('reviews.txt','w')
noMorePages=False
page=1
reviewNum=0
while True:
    url='http://www.amazon.com/Samsung-UN105S9-Curved-105-Inch-Ultra/product-reviews/B00L403O8U/ref=cm_cr_pr_btm_link_'+str(page)+'?ie=UTF8&showViewpoints=1&sortBy=recent&reviewerType=all_reviews&filterByStar=all_stars&pageNumber='+str(page)
    for i in range(0,2):#try each page n times  
        try:
            response=browser.open(url)    
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR LINK:',url
            print error_type, 'Line:', error_info.tb_lineno
            continue
        #time.sleep(1)
        html=response.read()
        #if re.search('Sorry, no reviews match your current selections',html): break
        if html.find('Sorry, no reviews match your current selections')!=-1:
            noMorePages=True
            break
        if re.search('<div id=.*? class="a-section review">',html):
            results=re.finditer('<div id=.*? class="a-section review">' + \
                '.*?class="a-icon-alt">(.*?)</span>' + \
                '.*?<a class="a-size-base a-link-normal author" href=.*?">(.*?)</a>' + \
                '[\s,\S]*?a-color-secondary review-date">(.*?)</span>' + \
                '.*?<span class="a-size-base review-text">(.*?)</span>',html)
            #[\s,\S]*?
            for result in results:
                #result.group(1) star
                #result.group(2) author
                #result.group(3) date
                #result.group(4) reviewtext
                reviewNum+=1
                #split the <br>
                a=result.group(4).split('<br>')
                b=''
                for i in range(0,len(a)):
                    b+=a[i]+' '

                fileWriter.write("www.amazon.com"+'\t'+b+'\t'+result.group(1)+'\t'+result.group(3)+'\n')
            break
    if noMorePages:
        break
    page+=1
print "total pages",page-1
print "total reviews",reviewNum
fileWriter.close()


