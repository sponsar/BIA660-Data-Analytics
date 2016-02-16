"""
A simple script that demonstrates how we classify textual data with sklearn.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier,NearestCentroid#0.585, 0.587
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV,PassiveAggressiveClassifier#0.7548, 0.749, 0.743
from sklearn.linear_model import SGDClassifier,RidgeClassifier,RidgeClassifierCV#0.733, 0.725, 0.744
from sklearn.ensemble import AdaBoostClassifier,BaggingClassifier,ExtraTreesClassifier,RandomForestClassifier#0.634, 0.6586, 0.6929, 0.669
from sklearn.dummy import DummyClassifier#0.499
from sklearn.calibration import CalibratedClassifierCV #0.7477 with some problems
from sklearn.tree import DecisionTreeClassifier,ExtraTreeClassifier#0.619, 0.6038
from sklearn.naive_bayes import MultinomialNB,BernoulliNB#0.7707, 0.7665



#read the reviews and their polarities from a given file
def loadData(fname):
    reviews=[]
    labels=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')  
        reviews.append(review.lower())    
        labels.append(int(rating))
    f.close()
    return reviews,labels

rev_test=[]
labels_test=[]
f1=open('in.txt')
f2=open('correct.txt')
for line in f1:
	rev_test.append(line.strip().lower())
for line in f2:
	labels_test.append(int(line))
f1.close()
f2.close()

rev_train,labels_train=loadData('train.txt')#list of reviews

#Build a counter based on the training dataset
counter = CountVectorizer()
counter.fit(rev_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data       #actually, it's a matrix
counts_test = counter.transform(rev_test)#transform the testing data

#build a 3-NN classifier on the training data
'''
KNN=KNeighborsClassifier(3)
KNN.fit(counts_train,labels_train)
'''

RL=DecisionTreeClassifier(max_depth=6)
RL.fit(counts_train,labels_train)

#use the classifier to predict
predicted=RL.predict(counts_test)#return a list

#print the accuracy
print accuracy_score(predicted,labels_test)
