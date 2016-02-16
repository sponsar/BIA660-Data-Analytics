'''
fw=open('out.txt','w') 
fr=open('in.txt')
for line in fr:
    toks=line.strip().split() #strip and split
    newSent=toks[0] #start a new sentence with only the first word
    for i in range(1,len(toks)):#for each position after the first one
        if toks[i-1].lower()=='not': #if the previous word is 'not'
            newSent+=toks[i]#add the current word to the new sentence
        else:#otherwise, add a space and THEN the current word to the new sentence
            newSent+=' '+toks[i]
    fw.write(newSent+'\n') 
fr.close()
fw.close()

'''
import re

fw=open('out.txt','w') 
fr=open('in.txt')
for line in fr: 
    #add a space in the beginning. We do this to match 'not' in the beginning of the sentence
    line=' '+line 
    
    #\\1 represents the first parenthesized group, 
    #which in this case is [nN][oO][tT] and matches not,noT,nOt,nOT,Not,NoT,NOt,NOT 
    line=re.sub(' ([nN][oO][tT]) ',' \\1',line)#\\1 represents the first parenthesized group, which in this case is [nN][oO][tT] 
    
    fw.write(line.strip()+'\n') 
fr.close()
fw.close()
