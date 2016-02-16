import re
f=open('in.html')
html=f.read()
f.close()
fw=open('out.txt','w')
TopixQuotes=dict()#make a map[string,int]
quotes=re.finditer('<div class="htmlxquoteauthor"> (.*?) wrote: </div>',html)
for quote in quotes:
	name=quote.group(1).lower()#name of being quoted
	if name in TopixQuotes:
		TopixQuotes[name]+=1
	else:
		TopixQuotes[name]=1
listName=TopixQuotes.keys()#to sort, we need to get all the keys of the map
listName.sort()
for i in listName:
	print i+'\t'+str(TopixQuotes[i])
	#fw.write(listName[i]+'\t'+str(TopixQuotes[listName[i]])+'\n')
fw.close()
