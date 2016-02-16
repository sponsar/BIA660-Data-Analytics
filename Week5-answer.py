"""
Count the number of August Reviews for an item on Amazon
"""
import urllib2,re,sys,time

browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

#read the link
f=open('in.txt')
prefix=f.readline().strip()
f.close()

page=1
augustNum=0
noMorePages=False

while True:
    
    #print 'page',page
    
    url=prefix+'/ref=cm_cr_pr_btm_link_'+str(page)+'?ie=UTF8&showViewpoints=1&sortBy=recent&reviewerType=all_reviews&formatType=all_formats&filterByStar=all_stars&pageNumber='+str(page)    
    
    for i in range(0,5): #try each page 5 times    
        #print 'attempt',i+1
        try:
            response=browser.open(url)    
        except Exception:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR LINK:',url
            print error_type, 'Line:', error_info.tb_lineno
            continue

        html=response.read()#read the html  
          
        if html.find('Sorry, no reviews match your current selections')!=-1:
            noMorePages=True           
            break # no more pages

        #revs=re.finditer('a-link-normal author.*?>(.*?)</a>.*review-date">on (.*?) ',html)
        revs=re.finditer('<span class="a-size-base a-color-secondary review-date">on August(.*?)</span>',html)
        
        total=0 #count how many reviews you got in this page. If 0, something went wrong and you should try again.
        for rev in revs: 
            total+=1


        print "page", page, "attempt", i, total
        '''
        if total>0:
            augustNum+=total
            break # at least 1 review was found, stop trying this page.
        '''
        #time.sleep(2) #sleep after every attempt
    
    if noMorePages: break
    page+=1


#print augustNum
fw=open('out.txt','w')
fw.write(str(augustNum))
fw.close()



