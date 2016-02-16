from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
import nltk
import re


rev_train=[]
labels_train=[]
rev_test=[]
f=open("training.txt")
for line in f:
    review,rating=line.strip().split('\t')
    review=re.sub("not( )+","not",review.lower())
    review=re.sub("barely( )+","not",review)
    review=re.sub("merely( )+","not",review)
    review=re.sub("hardly( )+","not",review)
    review=re.sub("rarely( )+","not",review)
    #review=re.sub("[,.]"," ",review)
    #review=re.sub("&#39;","'",review)
    
    rev_train.append(review)    
    labels_train.append(int(rating))
f.close()

f=open("testing.txt")
for line in f:
    review=re.sub("not( )+","not",line.strip().lower())
    review=re.sub("barely( )+","not",review)
    review=re.sub("merely( )+","not",review)
    review=re.sub("hardly( )+","not",review)
    review=re.sub("rarely( )+","not",review)
    #review=re.sub("&#39;","'",review)
    #review=re.sub("[,.]"," ",review)
    
    rev_test.append(review)
f.close()


clf1 = LogisticRegression()#0.787
clf2 = KNeighborsClassifier(n_neighbors=19)
clf3 = MultinomialNB()#0.823
#clf4 = DecisionTreeClassifier(max_depth=22,max_features=4000,class_weight=None)
clf5 = AdaBoostClassifier()#base_estimator=DecisionTreeClassifier(max_depth=1, min_samples_leaf=1),n_estimators=50,algorithm="SAMME.R"
clf6 = SGDClassifier(n_jobs=-1, shuffle=False)

eclf = VotingClassifier(estimators=[('lr', clf1), ('mnb', clf3)], voting='soft', weights=[0.787,0.823])#0.787 0.823
#eclf = VotingClassifier(estimators=[('lr', clf1), ('knn', clf2), ('mnb', clf3)], voting='soft',weights=[0.8,0.62,0.837])
'''
parameters={"vect__ngram_range": ([1,1], [1,2]), #assume [1,2]
            "vect__use_idf": (True, False), #assume False
            "vect__norm": ('l2', None) #and l1, assume None
            #"vect__smooth_idf": (True, False), #assume True
            #"vect__sublinear_tf": (True, False)#assume True
            #"vect__max_df": (0.2, 0.3, 0.7, 0.8) #become worse
            #"vect__min_df": (1e-2, 1e-3, 1e-4, 1e-5) #nothing change
            #"eclf__weights": ( [1,1],[1,2],[2,1] ) 
            }
'''
'''
parameters = {'eclf__C': (1,2,3),
              'eclf__fit_intercept':(True,False),
              'eclf__solver':('newton-cg','lbfgs','liblinear','sag')
              }
'''
#ngram_range=[1,2], norm=None, use_idf=False, smooth_idf=True, sublinear_tf=True
#grid_search = GridSearchCV(Pipeline([('vect', TfidfVectorizer(use_idf=False, ngram_range=[1,2], norm=None, sublinear_tf=True, smooth_idf=True) ), ('eclf', clf1)]), parameters, n_jobs=-1, verbose=1)
pipleline_clf = Pipeline([('vect', TfidfVectorizer(ngram_range=[1,2], norm=None, use_idf=False, smooth_idf=True, sublinear_tf=True)), ('eclf', eclf)])

pipleline_clf.fit(rev_train,labels_train)

#predicted=pipleline_clf.predict(rev_test)
proba=pipleline_clf.predict_proba(rev_test)

ans=[]
for x, probability in proba:
    if probability>0.502:
        ans.append(1)
    else:
        ans.append(0)
labels='\n'.join(str(i) for i in ans)
fw=open("out.txt",'w')
fw.write(labels)
fw.close()
