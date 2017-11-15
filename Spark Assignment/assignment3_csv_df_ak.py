"""
Assignment 3 - CSV, Text file processing

@author Aruna Kumaraswamy
"""
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import StringType
from pyspark import SQLContext


conf = SparkConf().setMaster("local").setAppName("Assignment3CSV")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")

#Import file people.txt located at the same location as people.json into a rdd using built-in CSV library.
#Import the CSV library at the beginning and use csv.reader() to load the data.
#people_rdd = sc.textFile('data/people.txt').map(lambda line: line.split(","))
#people_df = people_rdd.toDF(['name','age'])

sqlContext = SQLContext(sc)
people_df = sqlContext.read.csv("data/people.txt")

#Display the data in your rdd.
print 'Assignment 3 - people.txt via CSV Reader'
print people_df.show()