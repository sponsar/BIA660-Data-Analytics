#encoding=utf8
from sklearn.metrics import accuracy_score
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, SGDClassifier
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.calibration import CalibratedClassifierCV #0.7546934
from sklearn.neighbors import KNeighborsClassifier,NearestCentroid#0.585, 0.587
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC #0.607, 0.771, 0.8095
from sklearn.ensemble import AdaBoostClassifier,BaggingClassifier,ExtraTreesClassifier,RandomForestClassifier#0.78875, 0.75, 0.7645, 0.7295
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.svm import SVC
from scipy.stats import randint as sp_randint
from random import random
#from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import re
import nltk
stopword=stopwords.words('english')

stemmer=SnowballStemmer('english')


def loadData(filename):
	reviews=[]
	labels=[]
	f=open(filename)
	for line in f:
		review,rating=line.strip().split('\t')

		review=review.lower()
		
		review=re.sub("not ","not",review)
		review=re.sub("barely ","not",review)
		review=re.sub("merely ","not",review)
		review=re.sub("hardly ","not",review)
		review=re.sub("rarely ","not",review)
		#review=re.sub("&#39;t ","not",review)
		#review=re.sub("<br>",' ',review)#可有可无
		#review=re.sub("[,.]"," ",review)

		'''
		list1=review.split()#tokenize!!!!!!!
		#list1=nltk.word_tokenize(review)
		list2=[stemmer.stem(word) for word in list1]#stem will lower every word
		review=' '.join(list2)
		'''
		
		#review=re.sub("[,.]"," ",review)
		#review=re.sub(" .*?&#39;.*? "," ",review)
		



		reviews.append(review)
		labels.append(int(rating))
	f.close()
	return reviews,labels


rev_train,labels_train=loadData("txt6000.txt")
rev_test,labels_test=loadData("txt1000.txt")


#Build a counter based on the training dataset
#counter = CountVectorizer(stop_words=stopwords.words('english'))
#counter = CountVectorizer(stop_words='english')
#counter = CountVectorizer()
#counter.fit(rev_train)




#count the number of times each term appears in a document and transform each doc into a count vector
#counts_train = counter.fit_transform(rev_train)
#counts_train = counter.transform(rev_train)#transform the training data
#counts_test = counter.transform(rev_test)#transform the testing data


#pick 3 classifiers
clf1 = LogisticRegression(solver='liblinear')#0.87 C=3, fit_intercept=False, max_iter=1, multi_class='ovr'
clf2 = KNeighborsClassifier(n_neighbors=503)#0.778
clf3 = MultinomialNB()#0.862 alpha=0.21,fit_prior=False
#clf3 = MultinomialNB()
clf4 = DecisionTreeClassifier(max_depth=22,max_features=4000,class_weight=None)#random
clf5 = AdaBoostClassifier()#0.752
#clf5 = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1),n_estimators=50,algorithm="SAMME")#0.788
clf6 = RandomForestClassifier(n_estimators=100)#random, every time gets different answer
clf7 = SGDClassifier(n_jobs=-1, shuffle=True)#0.872 random,every time gets different answer, if we make shuffle=False, no random any more
clf8 = SVC()

#clf1 = LogisticRegression()#0.787
#clf2 = KNeighborsClassifier(n_neighbors=19)#0.673
#clf3 = MultinomialNB()#0.823
#clf4 = DecisionTreeClassifier(max_depth=22,max_features=4000,class_weight=None)
#clf5 = AdaBoostClassifier()

#build a voting classifer
#eclf = VotingClassifier(estimators=[('1', clf1), ('2', clf2), ('3', clf3)], voting='soft', weights=[3,1,2]) 
eclf = VotingClassifier(estimators=[('lr', clf1), ('mnb', clf3)], voting='soft',weights=[0.787,0.823])
#eclf = VotingClassifier(estimators=[('1', clf1), ('3', clf3), ('5', clf5)], voting='soft')

pipleline_clf = Pipeline([('vect', TfidfVectorizer(use_idf=False, ngram_range=[1,2], norm=None, sublinear_tf=True, smooth_idf=True)), ('eclf', eclf)])
'''
parameters={"eclf__max_depth": [3, None],
            "eclf__max_features": sp_randint(1, 11),
            "eclf__min_samples_split": sp_randint(1, 11),
            "eclf__min_samples_leaf": sp_randint(1, 11),
            "eclf__bootstrap": [True, False],
            "eclf__criterion": ["gini", "entropy"]}
'''
'''
parameters={"vect__ngram_range": ([1,1],[1,2]),
			"vect__use_idf": (True, False), 
			"vect__norm": ('l2', None), #and l1
			"vect__smooth_idf": (True, False), 
			"vect__sublinear_tf": (True, False)
			#"vect__max_df": (0.2, 0.3, 0.7, 0.8)
			#"vect__min_df": (1e-2, 1e-3, 1e-4)
			}
			#"eclf__weights": ( [1,1],[1,2],[2,1] ) }
'''

parameters = {'eclf__C': (1,2,3)
			  }
#solver : {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’}



#grid_search = GridSearchCV(Pipeline([('vect', TfidfVectorizer(use_idf=False, ngram_range=[1,2], norm=None, sublinear_tf=True, smooth_idf=True)), ('eclf', clf1)]), parameters, n_jobs=-1, verbose=1,cv=2)

pipleline_clf.fit(rev_train,labels_train)

'''
best_parameters, score, _ = max(grid_search.grid_scores_, key=lambda x: x[1])
for param_name in sorted(parameters.keys()):
	print("%s: %r" % (param_name, best_parameters[param_name]))
#print score
print grid_search.best_score_#the same
'''
'''
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
	print("%s: %r" % (param_name, best_parameters[param_name]))
print grid_search.best_score_
'''

#predicted=pipleline_clf.predict(rev_test)
proba=pipleline_clf.predict_proba(rev_test)

#prolist=[0.4+i*0.01 for i in range(1,31)]
#for pro in prolist:
ans=[]
for x, probability in proba:
	if probability>0.61:
		ans.append(1)
	else:
		ans.append(0)
a='\n'.join(str(i) for i in ans)
fw=open('test2.txt','w')
fw.write(a)
fw.close()
#print pipleline_clf.score(rev_test,labels_test)
#print accuracy_score(predicted,labels_test)



