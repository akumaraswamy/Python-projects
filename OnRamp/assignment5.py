#Assignment 5: Classify reviews using NaiveBayes algorithm.
#@author: Aruna Kumaraswamy

import os
import re
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

relativePath = os.getcwd()

positiveTrainingPath = relativePath + "/resources/TrainingDataPositive.txt"  # file containing raw data
negativeTrainingPath = relativePath + "/resources/TrainingDataNegative.txt"  # file containing raw data
testDataPath = relativePath+"/resources/testSet.txt"
processedFilePath = relativePath+"/resources/processedReview.txt"

# pre-process data
def preProcessFile(fileName,review_type,mode):  # function to preprocessed the data
    file = open(fileName)
    writeFile = open(processedFilePath, mode)
    badChar = "[,!.?#@=\n]"  # list of bad characters to be removed from the SMS
    for line in file:
        line = line.lower().replace("\t",
                                    " ")  # First convert each word to lower case , then replace all tab space with single back space

        line = re.sub(badChar, "", line)  # using regular expression remove all bad character from the SMS

        arr = line.split(" ")  # split the line using space and put all the words into a list

        words = " ".join(word for word in
                         arr[0:len(arr)])  # rest of the words in the list are joined back to form the original sentence

        toWrite = review_type + "," + words  # line to be written: class label, SMS

        writeFile.write(toWrite)

        writeFile.write("\n")  # after writing every line put new line character.

    file.close()

    writeFile.close()



# create training labels
def getDataAndLabels():
    file = open(processedFilePath)  # read the processed file

    label = []

    data = []

    for line in file:
        arr = line.replace("\n", "").split(",")  # split with comma
        label.append(arr[0])  # first element is class label
        data.append(arr[1].replace("\n", ""))  # second element is SMS

    return data, label


# create testing labels
def createTestingLabel():
    test_label = []
    for i in range(0,4321):
        if (i<2989):
            test_label.append('positive')
        else:
            test_label.append('negative')
    return test_label

def getTestData():
    file = open(testDataPath)
    data = []

    for line in file:
        arr = line.replace("\n", "")
        data.append(arr.replace("\n", ""))  # second element is SMS

    return data

# classify

preProcessFile(positiveTrainingPath,"positive","w")
preProcessFile(negativeTrainingPath,"negative","a")
training_data,training_label = getDataAndLabels()
test_label = createTestingLabel()
test_data = getTestData()
print len(training_data),len(training_label)
print len(test_data),len(test_label)

count_vect = CountVectorizer()  # instance of count vectorize

X_train_counts = count_vect.fit_transform(training_data)  # create a numerical feature vector

tfidf_transformer = TfidfTransformer()  # calculate term frequency

X_train_tfidf = tfidf_transformer.fit_transform(
    X_train_counts)  # calculate Term Frequency times Inverse Document Frequency

model = MultinomialNB(fit_prior=True)  # create an instance of multinomial Naive Bayes

model.fit(X_train_tfidf, training_label)  # train the model

X_new_counts = count_vect.transform(test_data)

X_new_tfidf = tfidf_transformer.transform(
    X_new_counts)  # create Term Frequency times Inverse Document Frequency for test data

predLabel = model.predict(X_new_tfidf)  # predict the test data by using TFID

print "Accuracy :", np.mean(predLabel == test_label) * 100  # calculte accuracy
