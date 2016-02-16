import re
f=open('in.txt')
fw=open("out.txt",'w')
for line in f:
    line=re.sub('not ','not',line.strip())
    line=re.sub('Not ','Not',line.strip())
    fw.write(line+'\n')
f.close()
fw.close()
