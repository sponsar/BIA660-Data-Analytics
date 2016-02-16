import nltk
import nltk.data
from nltk.util import ngrams
from nltk.corpus import stopwords
import re


f=open('in.txt')
text=f.read().strip().lower()
f.close()

sentences=re.split('\.',text)
fw=open("out.txt",'w')

stopword=stopwords.words('english')

for sentence in sentences:
    
    nouns=set()
    
    sentence=re.sub('[^（a-z\d）]',' ',sentence)#replace chars that are not letters or numbers with a space
    sentence=re.sub(' +',' ',sentence).strip()#remove duplicate spaces

    #tokenize the sentence
    terms = sentence.split()#this is a list of words in a sentence
    
    tagged_terms=nltk.pos_tag(terms)#do POS tagging on the tokenized sentence

    for pair in tagged_terms: 
        
        #if the word is an adjective
        if pair[1].startswith('NN'): 
            nouns.add(pair[0])

    threegrams = ngrams(terms,3) #compute 3-grams
    
    #for each 3gram
    for tg in threegrams:  
        if tg[0] in stopword or tg[1] in stopword or tg[2] in stopword: continue
        if (tg[0] in nouns  and tg[1] in nouns ) or (tg[1] in nouns  and tg[2] in nouns ) or (tg[0] in nouns  and tg[2] in nouns):
            fw.write(tg[0]+' '+tg[1]+' '+tg[2]+'\n')
fw.close()




