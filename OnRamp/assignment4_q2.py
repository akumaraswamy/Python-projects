import pandas
import os
import numpy as np
from numpy.linalg import inv


relativePath = os.getcwd()

dataFilePath = relativePath+"/Resources/OnlineNewsPopularity.csv"
news_data = pandas.read_csv(dataFilePath)

# Filter columns and split for CV
def dataFilter(data, targetColumn, columnName=[], isSplit=False):
    if len(columnName) == 0:  # if column names are not given then create X with all the attributes
        columnName = [col for col in data.columns if col not in targetColumn]

    dataFrame = data[columnName]
    labelFrame = data[[targetColumn]]

    if isSplit:  # if isSplit=True the split the data into two parts one for training and other for testing
        size = len(dataFrame)
        trainingData = dataFrame.loc[range(1, size / 2)]
        trainingLabel = labelFrame.loc[range(1, size / 2)]
        testData = dataFrame.loc[range(size / 2, size)]
        testLabel = labelFrame.loc[range(size / 2, size)]
        return trainingData, np.asarray(trainingLabel).flatten(), testData, np.asarray(testLabel).flatten()

    return dataFrame, np.asarray(labelFrame).flatten()

def calOptimalWeight(dataFrame, target):  # this function calculates W'=(X^TX)^-1X^TY

    innerProduct = (dataFrame.T).dot(dataFrame)  # calculating X^TX
    inverse = inv(innerProduct)  # calculate (X^TX)^-1
    product = inverse.dot(dataFrame.T)  # (X^TX)^-1X^T
    weight = product.dot(target)  # (X^TX)^-1X^TY
    print weight.shape

    return weight  # return W'

def predict(weights, X):  # this function calculates Y'=W^TX or y'=XW
    predictedValue = X.dot(weights)

    return predictedValue


def calSSE(target, predicted):  # calculate sum of squared error
    m = len(target)
    SSE = ((np.asarray(target) - np.asarray(predicted)) ** 2) / float(2 * m)
    return sum(SSE)


def select_features(data):
    threshold = 100
    prev_sse_sum = 0
    header = ''
    cols = news_data.shape[1]
    selected_cols = []
    for i in range(0,cols-1):
        selected_cols.append(i)
        selected_data = news_data[selected_cols]
        classifier = news_data['shares']
        header =''
        for header_col_idx in selected_cols:
            header += news_data.columns.values[header_col_idx] + ','
        print 'Selected Features ', header
        #Predict
        weights = calOptimalWeight(selected_data,classifier)
        predictions = predict(weights, selected_data)
        #Cal SSR
        sse_sum = calSSE(classifier,predictions)
        diff = prev_sse_sum -  sse_sum
        print diff
        if (prev_sse_sum == 0):
            prev_sse_sum = sse_sum
        else:
            if (diff < threshold):
                break
            else:
                prev_sse_sum = sse_sum
                continue
    print '\n Assignment 4-2'
    print '\nSelected Features ',header
    print '\nSum of Squared Errors ',sse_sum

select_features(news_data)







