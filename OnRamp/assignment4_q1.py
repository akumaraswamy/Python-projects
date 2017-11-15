"""
Logistic Regression on IRIS Data Set - Assignment 4 Q1
@auhor Aruna Kumaraswamy

"""
import pandas as pd
import scipy.optimize as opt
import numpy as np
import os

# Read Input File
file_path = os.getcwd() + '\iris.csv'
iris_data = pd.read_csv(file_path)

def Z_ScoreNormalization(data,targetColName): 
    for i in data.columns:
        if i == targetColName:  # do not modify target values
            continue

        mean = data[i].mean()
        std = data[i].std()
        data[i] = data[i].apply(lambda d: float(d - mean) / float(std))  # perform z-score normalization

# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Hypothesis and cost
def cost(theta, X, y):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    m = len(X)
    hw = sigmoid(X * theta.T)
    JW_part_1 = np.multiply(y, np.log(hw))
    JW_part_0 = np.multiply((1 - y), np.log(1 - hw))
    JW = (1/m)*(np.sum(-JW_part_1-JW_part_0))
    return JW

# Gradient calculation
def gradient(theta, X, y):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    hw = sigmoid(X * theta.T)
    num_features = 4
    grad = np.zeros(num_features)
    error = hw - y
    #calculate the new gradient applying the error adjustment to features
    for i in range(num_features):
        term = np.multiply(error, X[:, i])
        grad[i] = np.sum(term) / len(X)

    return grad

# Predict
def predict(theta, X):
    probability = sigmoid(X * theta.T)
    #print probability
    return [1 if x >= 0.5 else 0 for x in probability]

def calAccuracy(testLabel, predictLable):
    count = 0
    for i in range(len(testLabel)):
        if testLabel[i] == predictLable[i]:
            count += 1
    print "Accuracy : ",(float(count) / len(testLabel)) * 100

Z_ScoreNormalization(iris_data,'class')
#iris_data.insert(0, 'Ones', 1)

#Binary labelling
class_array = iris_data['class'].values
class_array = np.where(class_array == 'Iris-setosa',1,0)
iris_data['class'] = class_array
#iris_data = iris_data.sort_values(['sepal_width'])

#Separate feature and label
cols = iris_data.shape[1]
X = iris_data.iloc[:,0:cols-1]
y = iris_data.iloc[:,cols-1:cols]

X = np.array(X.values)
y = np.array(y.values)
theta = np.zeros(4)

#Minimization function for gradient descent
result = opt.fmin_tnc(func=cost, x0=theta, fprime=gradient, args=(X, y))
#print 'fmin_tnc',cost(result[0], X, y)
print 'iris - Logistic regression training completed'

#Predict using the new theta value from grd
theta_min = np.matrix(result[0])
predictions = predict(theta_min, X)

#Accuracy of precited vs assigned label
calAccuracy(y,predictions)

from sklearn import linear_model
from sklearn.model_selection import train_test_split

#Accuracy is not good in the previos model.Discussed with Zheng and using sklearn to
#train and calculate the accuracy.
trainX,testX,trainY,testY = train_test_split(X,y,test_size=.20)
logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(trainX, trainY)
print '\n'
print 'Logistic regression using sklearn '
calAccuracy(testY,logreg.predict(testX))
