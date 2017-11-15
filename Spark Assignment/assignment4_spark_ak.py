"""
Assignment 4 - Fake data CSV processing - Dataframe

@author Aruna Kumaraswamy
"""
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import StringType
from pyspark import SQLContext
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import BooleanType, IntegerType, StringType
from pyspark.sql.functions import col, avg


schema = StructType([
    StructField("Id", IntegerType()),
    StructField("Birth_Country", StringType()),
    StructField("Email", StringType()),
    StructField("First_Name", StringType()),
    StructField("Income", IntegerType()),
    StructField("Job", StringType()),
    StructField("Last_name", StringType()),
    StructField("Loan_Approved", StringType()),
    StructField("SSN", StringType())
])

conf = SparkConf().setMaster("local").setAppName("Assignment4CSV")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")

#Load fake_data.csv(check canvas files section) into spark dataframe
sqlContext = SQLContext(sc)
fake_data_df = sqlContext.read.csv("data/Fake_data.csv",header=True,schema=schema)
fake_data_df.registerTempTable('fakedata')

print 'Assignment 4 - Fake Data Processing using data frame'
print fake_data_df.printSchema()

#Find birth country which has highest amount of people
print 'Birth Country with highest amount of people'
ctry_df = fake_data_df.groupBy('Birth_Country').count()
print ctry_df.sort('count', ascending=False).show(1)


#Find average income of people who are born in united states
print 'Average income of people who are born in united states'
avg_inc_sql = "select Birth_Country,Income from fakedata where Birth_Country = 'United States of America'"
avg_inc_df = sqlContext.sql(avg_inc_sql)
print avg_inc_df.agg({"Income":"avg"}).show()
print("\n")

#How many people has income over 100,000 but their loan is not approved.
print 'Number of people has income over 100,000 but their loan is not approved.'
loan_app_sql = "select count(*) from fakedata where Income > 100000 and Loan_Approved='False'"
loan_app_df = sqlContext.sql(loan_app_sql)
print loan_app_df.show()
print("\n")

#Find top 10 people with highest income in United States. (Print their names, income and jobs)
print 'Top 10 people with highest income in United States'
top_income_sql = "select First_Name,Last_name,Income,Job from fakedata where Birth_Country = 'United States of America'"
tinc_df = sqlContext.sql(top_income_sql)
print tinc_df.sort('Income', ascending=False).show(10)
#print fake_data_df["First_Name","Last_name","Income","Job"].sort('Income', ascending=False).show(10)
print("\n")

#How many number of distinct jobs are there?
print 'Number of distinct jobs are there'
job_sql = "select Job from fakedata"
job_df = sqlContext.sql(job_sql)
unique_job =  job_df.select('Job').distinct()
print unique_job.count()
print("\n")

#How many writers earn less than 100,000?
print 'Number of writers earn less than 100,000'
writer_sql = "select count(*) from fakedata where Job='Writer' and Income < 100000"
print sqlContext.sql(writer_sql).show()

