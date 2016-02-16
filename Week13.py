# -*- coding: utf-8 -*-
from nltk.util import ngrams
from operator import itemgetter
from nltk.corpus import stopwords
import nltk,re
f1=open('emotions.txt')
f2=open('data.txt')
stop=stopwords.words('english')
wordDict=dict()

emotions=[dict() for i in range(8)]

firstLine=f1.readline().strip().split('\t')[1:]
for line in f1:#remove the first line
	l=line.strip().split('\t')
	wordDict[l[0]]=[l[i] for i in range(1,9)]#words that associated with emotion
f1.close()

for sentence in f2:
	sentence=re.sub('a1c',' ',sentence.strip())
	sentence=re.sub('[^a-z]','  ',sentence)
	terms=nltk.word_tokenize(sentence)
	tagged_terms=nltk.pos_tag(terms)
	nouns=set()
	for word,tag in tagged_terms:
		if tag.startswith('NN') and word not in stop:
			nouns.add(word)
	s=set(terms)#这个句子转换成set
	e=[0 for i in range(8)]#这个句子有哪些emotion
	for word in s:
		if word in wordDict:
			for i in range(8):
				if wordDict[word][i]=='1':
					e[i]=1
	for i in range(8):
		if e[i]==1:#如果这个句子有这种情感
			for noun in nouns:
				emotions[i][noun]=emotions[i].get(noun,0)+1
f2.close()

fw=open('out.txt','w')
for i in range(8):
	fw.write('20 most frequent nouns for '+firstLine[i]+':\n')
	#l=sorted(emotions[i],key=emotions[i].get,reverse=True)
	l=sorted(emotions[i].items(),key=itemgetter(1),reverse=True)
	for j in range(20):
		fw.write(l[j][0]+" : "+str(l[j][1])+'\n')
	fw.write('--------------------------\n')
fw.close()
