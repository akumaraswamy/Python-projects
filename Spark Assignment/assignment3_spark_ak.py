"""
Assignment 3 - JSON, Text file processing

@author Aruna Kumaraswamy
"""
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

import csv
import StringIO

def loadRecord(line):
    """Parse a CSV line"""
    input = StringIO.StringIO(line)
    reader = csv.DictReader(input, fieldnames=["name", "age"])
    return reader.next()


conf = SparkConf().setMaster("local").setAppName("Assignment3")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")


#Import people.json file using HiveContext or sqlContext into a DataFrame.
hiveCtx = HiveContext(sc)

#Print schema information using printSchema() function.
people_json_df = hiveCtx.read.json("data/people.json")
#Next register the dataframe as a temporary table.
people_json_df.registerTempTable("people")
#Display distinct names from the people.json file by firing a SQL query on the temporary table created.
results = hiveCtx.sql("SELECT distinct name FROM people")
print 'Assignment 3 - people.json as hive table'
print people_json_df.printSchema()
print results.show()


#Import file people.txt located at the same location as people.json into a rdd using built-in CSV library.
#Import the CSV library at the beginning and use csv.reader() to load the data.
people_rdd = sc.textFile('data/people.txt').map(lambda line: line.split(","))
input = sc.textFile('data/people.txt').map(loadRecord)
print 'Assignment 3 - people.txt via CSV reader'
print input.collect()

