# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 07:17:08 2017
Airbnb First time booking prediction

@author: Aruna Kumaraswamy

"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

  
def generation_by_age(age_values):
    gen_values = []
    for x in age_values:
        if (x > 70):
            gen_values.append('silent')
        elif (x > 53) and (x <= 70):
            gen_values.append('boomer')
        elif (x > 41) and (x <= 53):
            gen_values.append('genx')
        elif (x > 21) and (x <= 41):
            gen_values.append('geny')
        elif (x <= 21):
            gen_values.append('genz')
    return gen_values

seed = 7
np.random.seed(seed)

print 'Feature Selection begins'
print 'Processing -  User data'

booking_df = pd.read_csv("train_users_2.csv",parse_dates=True) 
target = booking_df['country_destination']
booking_df = booking_df.drop(['country_destination'],axis=1)

# Convert age to numeric and retain age in the range 18:100
booking_df['age'] = booking_df['age'].fillna(0)
age_array = booking_df['age'].values
#Susbtitue the birth year with age
age_array = np.where(age_array > 1900, 2014-age_array, age_array)
#If age more than 100, then assume 100 as maximum
age_array = np.where(age_array > 100, 100, age_array)
#If age less than 18, then assume 18 as minimum
age_array = np.where(age_array <18, 18, age_array)
booking_df['age'] = age_array

age_int_values = age_array.astype(np.int)
gen_values = generation_by_age(age_int_values)
booking_df['generation'] = gen_values

#Time first active
booking_df['timestamp_first_active'] = booking_df['timestamp_first_active'].astype(str)
tfa_array = booking_df['timestamp_first_active'].values
tfa_month_array = [ x[4:6] for x in tfa_array]
tfa_yr_array = [ x[:4] for x in tfa_array]
booking_df['tfa_mon'] = tfa_month_array
booking_df['tfa_yr'] = tfa_yr_array
booking_df = booking_df.drop(['timestamp_first_active'],axis=1)

#Date Account Created 
booking_df['date_account_created'] = booking_df['date_account_created'].astype(str)
dac_array = booking_df['date_account_created'].values
dac_dates = [x.split('-') for x in dac_array]
dac_month_array = [ x[0] for x in dac_dates]
dac_day_array = [ x[1] for x in dac_dates]
booking_df['dac_mon'] = dac_month_array
booking_df['dac_day'] = dac_day_array
booking_df = booking_df.drop(['date_account_created'], axis=1)

#Less than 50% records have this populated, so drop               
booking_df = booking_df.drop(['date_first_booking'],axis=1)

#Fill missing values with 'missing'
booking_df['first_affiliate_tracked'] = booking_df['first_affiliate_tracked'].fillna('missing')

# One Hot Encoding of the discrete features
ohe_features = ['generation','gender','language','affiliate_channel','affiliate_provider',
               'first_affiliate_tracked','signup_method','signup_app','first_device_type','first_browser' ]
for ohf in ohe_features:
    ohe_df = pd.get_dummies(booking_df[ohf], prefix=ohf)
    booking_df = booking_df.drop([ohf], axis=1)
    booking_df = pd.concat((booking_df,ohe_df),axis=1)


# Read sessions csv and group by user id to sum the elapsed time
print 'Processing Session data'
session_df = pd.read_csv('sessions.csv')
session_df.loc[session_df['secs_elapsed'].isnull() ,'secs_elapsed'] = 0
session_group_df = session_df.groupby('user_id').agg({'action':np.size,'action_type':np.size,'device_type':np.size,'secs_elapsed': np.sum})

session_group_df['id'] = session_group_df.index
joined_df = pd.merge(booking_df,session_group_df,on='id',how='left')# on='user_id',
joined_df.loc[joined_df['secs_elapsed'].isnull() ,'secs_elapsed'] = 0
joined_df.loc[joined_df['action_type'].isnull() ,'action_type'] = 0
joined_df.loc[joined_df['action'].isnull() ,'action'] = 0
joined_df.loc[joined_df['device_type'].isnull() ,'device_type'] = 0

#joined_df.to_csv('airbnb_updated_train_2.csv')
joined_df = joined_df.drop(['id'],axis=1)
train_vals = joined_df.values
print 'Feature Selection - Completed'

le = preprocessing.LabelEncoder()
le = le.fit(target)
train_Y = le.transform(target)

trainX,testX,trainY,testY = train_test_split(train_vals,train_Y,test_size=.20)

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(trainX,trainY)

print("\n\nNaive Bayes Performance")
print accuracy_score(testY,nb.predict(testX))


print '\n RandomForest Classifier'
classes = le.inverse_transform([0,1,2,3,4,5,6,7,8,9,10,11])
rf = RandomForestClassifier(max_depth=12,random_state=seed, n_estimators=100)
clf = rf.fit(trainX, trainY)
predY = clf.predict(testX)
print 'Accuracy: ',accuracy_score(testY,predY)
print(classification_report(testY, predY,target_names=classes))

print '\n Neural Network'
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier(random_state=seed)
nn.fit(trainX,trainY)
print accuracy_score(testY,nn.predict(testX))
#svm = svm.SVC()
#clf = svm.fit(trainX,trainY)

print '\n Gradient Boost'
grd = GradientBoostingClassifier(n_estimators=50,random_state=seed,max_leaf_nodes=12)
grd.fit(trainX,trainY)
grd_pred_y = grd.predict(testX)
print 'Accuracy: ',accuracy_score(testY,grd_pred_y)
print(classification_report(testY, grd_pred_y,target_names=classes))
