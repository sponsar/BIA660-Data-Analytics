# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 15:59:48 2015

@author: xinyao huang
"""

def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

negLex=loadLexicon('negative-words.txt')#set
negAns=dict()
file_writer=open('winner.txt','w')
data_conn=open('input.txt')

for line in data_conn: # for every line in the file (1 review per line)
    negSet=set()
    line=line.strip()    
    
    words=line.split(' ') # list
    
    for word in words: #for every word in the review
        if word in negLex: # if the word is in the negative lexicon
            if word in negSet:
                continue
            else:
                negSet.add(word)
                if word in negAns:
                    negAns[word]+=1
                else:
                    negAns[word]=1

max=0
ans=""
for word in negAns:
    if negAns[word]>max:
        max=negAns[word]
        ans=word
file_writer.write(ans)
file_writer.close()
data_conn.close()




