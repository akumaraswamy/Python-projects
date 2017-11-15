""""
Using pyspark create a word count application of all the words of the file assignment_2_datafile.txt
Avoid counting trivial words such as vowels and pronouns.

@author Aruna Kumaraswamy
"""
from pyspark import SparkConf, SparkContext

print 'Assignment 2 - Spark Word Count Application'
conf = SparkConf().setMaster("local").setAppName("Assignment2")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")

#Read the file
wc_file_rdd = sc.textFile('data/assignment_2_datafile.txt')
#Lines are split into words and words less than 4 characters are filtered
wc_filter_rdd = wc_file_rdd.flatMap(lambda x:x.split(' ')).filter(lambda x:len(x)>3)
#Get a dictionary of the word and number of occurence of the word.
print wc_filter_rdd.countByValue()




