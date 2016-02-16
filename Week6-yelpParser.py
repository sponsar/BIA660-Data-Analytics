import re

#read the file
f=open('in.html')
html=f.read()
f.close()

fw=open('out.txt','w')

#split the html into segments, 1 segment for each review
segments=html.split('<div class="review review--with-sidebar"')

#for each segment
for segment in segments[2:]:
 
    match=re.search('itemprop="author" content="(.*?)">\
.*?class="user-location">(.*?)</li>.*?\
friends_c-common_sprite"></i> <b>(.*?)</b>.*?\
review_c-common_sprite"></i> <b>(.*?)</b>.*?\
itemprop="ratingValue" content="(.*?)".*?\
itemprop="datePublished".*?>(.*?)<',segment,re.S)

    name=match.group(1).strip()
    location=match.group(2).strip()[3:-4]
    fnum=match.group(3).strip()
    rnum=match.group(4).strip()
    stars=match.group(5).strip()
    date=match.group(6).strip()
    fw.write(name+'\t'+location+'\t'+fnum+'\t'+rnum+'\t'+stars+'\t'+date+'\n') 

fw.close()
