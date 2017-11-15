# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 21:49:15 2017

@author: aruna
"""

import json
import pandas as pd
import numpy as np
import time
import sklearn
from sklearn.feature_extraction import text as sk_fe_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, f1_score, recall_score
from TwitterAPI import TwitterAPI
from sklearn.metrics import confusion_matrix

#Set up the variables for your 'application'
consumerkey = 'qGQwrYNsIr8JTP0j0y4YjelNe'
consumersecret = 'dh3eUa9xKUJe6YHGgEW3VjfLCyHQETGy46mcbe7kZ1ZTdr69Sp'

#Setup your API key
api = TwitterAPI(consumerkey,consumersecret,auth_type='oAuth2')

def score(true,pred):
  return (precision_score(true,pred),
          recall_score(true,pred),
          f1_score(true,pred))

def print_score(s):
  print("""
Precision:  {:0.3}
Recall:     {:0.3}
F-Score:    {:0.3}
""".format(*s))

def searchTwitter2(query,api=api,n=100):
    r  =  []
    qs   =  0
    if   len(r)==0:
        r.extend([t for t in api.request("search/tweets",{'q':query,'count':n})])
        qs   +=1
        while len(r) < n:
            print("Querying twitter for {}. {}/{} gathered.".format(query,len(r),n))
            last =  r[-1]['id']
            r.extend([t for t in   api.request("search/tweets",{'q':query,'count':n,'max_id':last})])
            qs   += 1
            if   qs >  180:
                time.sleep(840)
                qs   =  0
        return r[:n]

def searchTwitter(query,feed="search/tweets",api=api,n=100):
  return [t for t in api.request(feed, {'q':query,'count':n})]

#Get JSON from Twitter
cats = searchTwitter2('#obama -#trump',n=2000) #cats -#dogs
dogs = searchTwitter2('#trump',n=2000) #dogs

# Convert the json returned by Twitter into a dataframe
cats_d = pd.read_json(json.dumps(cats))
dogs_d = pd.read_json(json.dumps(dogs))

#cats_d.to_csv('cats.csv',sep='\t', encoding='utf-8')
#dogs_d.to_csv('dogs.csv',sep='\t', encoding='utf-8')

# If you would like to look at the full data frame
cats_d.info()
dogs_d.info()

#Get text only and replace hashtags with blanks
#If you want to use the normalizer, import it above and pass x.replace() to the noramlizer function
cats_text = [x.replace('#obama',"") for x in cats_d['text']]
#print cats_text
dogs_text = [x.replace('#trump',"") for x in dogs_d['text']]
#print dogs_text

#Create features and return sparse matricies
vectorizer = sk_fe_text.CountVectorizer(cats_text+dogs_text)
vectorizer.fit(cats_text+dogs_text)
cats_tdm = vectorizer.transform(cats_text).toarray()
dogs_tdm = vectorizer.transform(dogs_text).toarray()

#Create visible matricies and combine
zeros = np.zeros((len(cats_text),1))
ones = np.ones((len(dogs_text),1))
catsdogs = np.concatenate((cats_tdm,dogs_tdm),axis=0)
y = np.ravel(np.concatenate((zeros,ones),axis=0))

#Create train/test split for modeling
trainX,testX,trainY,testY = train_test_split(catsdogs,y,test_size=.20)

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(trainX,trainY)

print("\n\nNaive Bayes Performance")
s = score(testY,nb.predict(testX))
print_score(s)

#SVM
from sklearn.svm import SVC
svm = SVC()
svm.fit(trainX,trainY)

print("\n\nSVM performance")
s = score(testY,svm.predict(testX))
print_score(s)

#Neural Network
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier()
nn.fit(trainX,trainY)

print("\n\nNeural Network Performance")
s = score(testY,nn.predict(testX))
print_score(s)

#KNN
from sklearn.neighbors import KNeighborsClassifier
knn1 = KNeighborsClassifier(n_neighbors=1)
knn5 = KNeighborsClassifier(n_neighbors=5)
knn5d = KNeighborsClassifier(n_neighbors=5,weights='distance')

knn1.fit(trainX,trainY)
knn5.fit(trainX,trainY)
knn5d.fit(trainX,trainY)

print("\n\nKNN 1 Neighbor Performance")
s = score(testY,knn1.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Performance")
s = score(testY,knn5.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Weighted Performance")
s = score(testY,knn5d.predict(testX))
print_score(s)
