# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:14:36 2015

@author: sponsar
"""

#import the two libraries we will be using in this script
import urllib2,re,sys

#make a new browser, this will download pages from the web for us. This is done by calling the 
#build_opener() method from the urllib2 library
browser=urllib2.build_opener()

#desguise the browser, so that websites think it is an actual browser running on a computer
browser.addheaders=[('User-agent', 'Mozilla/5.0')]


#number of pages you want to retrieve (remember: 10 freelancers per page)
#pagesToGet=100


#create a new file, which we will use to store the links to the freelancers. The 'w' parameter signifies that the file will be used for writing.
fileWriter=open('out.txt','w')

def load_in_txt(fname):
    new_name=set()
    whatever=open(fname)
    #add every word in the file to the set
    for line in whatever:
        new_name.add(line.strip())# remember to strip to remove the lin-change character
    whatever.close()

    return new_name

names=load_in_txt("in.txt")#set of names

#for every number in the range from 1 to pageNum+1  
for name in names:
    
    #print 'processing page :', page
    
    #make the full page url by appending the page num to the end of the standard prefix
    #we use the str() function because we cannot concatenate strings with numbers. We need
    #to convert the number to a string first.
    #url='https://www.freelancer.com/freelancers/skills/all/'+str(page)
    url='https://www.freelancer.com/u/' + name + ".html"
    try:
        #use the browser to get the url.
        response=browser.open(url)    
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR LINK:',url
        print error_type, 'Line:', error_info.tb_lineno
        continue
    
    #read the response in html format. This is essentially a long piece of text
    myHTML=response.read()

    unique=set()#remember unique usernames	


    #users=re.finditer('/u/(.*?)"',myHTML)#get all the matches
    users=re.finditer('saveByline">\n(.*)',myHTML)#get all the matches
    for user in users:
        username=user.group()
        header=username[username.find('>')+1:username.find('&nbsp')].strip()
        #print username        
        
    
    fileWriter.write(name + '@' + header + '\n')
    
    
    
    '''
    for user in users:
        username=user.group(1) # get the username
        if username.find('%')==-1:
            unique.add(username) #check to avoid adding the <%- username %>.html construct

    #write the results
    for username in unique:
        fileWriter.write('https://www.freelancer.com/u/'+username+'\n')
'''

#close the file. File that are opened must always be closed to make sure everything is actually written and finalized.
fileWriter.close()


