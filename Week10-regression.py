"""
A simple script that demonstrates how we classify textual data with sklearn.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
import re



#read the reviews and their polarities from a given file
def loadData(fname):
    reviews=[]
    labels=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')
        review=re.sub("not( )+","not",review.lower())
        #review=re.sub("[,.]"," ",review)
        #review=re.sub("<br>"," ",review)
        reviews.append(review)    
        labels.append(int(rating))
    f.close()
    return reviews,labels

rev_train,labels_train=loadData('txt1.txt')
rev_test,labels_test=loadData('txt2.txt')

#Build a counter based on the training dataset
counter = CountVectorizer(stop_words=stopwords.words('english'))
#counter = CountVectorizer(stop_words='english')
counter.fit(rev_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#build a Logistic Regression classifier on the training data
LR=LogisticRegression ()
LR.fit(counts_train,labels_train)

#use the classifier to predict
predicted=LR.predict(counts_test)
#print type(predicted)


#print the accuracy
print accuracy_score(predicted,labels_test)
