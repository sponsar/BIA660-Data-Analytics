"""
A simple script that demonstrates how we classify textual data with sklearn.

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


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

rev_train,labels_train=loadData('reviews_train.txt')
rev_test,labels_test=loadData('reviews_test.txt')


#Build a counter based on the training dataset
counter = CountVectorizer()
counter.fit(rev_train)


#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#build an empty classifier 
DT = DecisionTreeClassifier( max_depth=None, \
max_features=None, class_weight=None)

iterations=10
acc=0

#try the classifier 10 times to get a more confident estimate
for i in range(iterations):
    #train all classifier on the same datasets
    DT.fit(counts_train,labels_train)

    #use hard voting to predict (majority voting)
    pred=DT.predict(counts_test)

    #get accuracy
    acc+=accuracy_score(pred,labels_test)

print acc/10
