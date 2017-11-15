"""
Assignment 4 - Fake data CSV processing - RDD

@author Aruna Kumaraswamy
"""
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("Assignment4RDD")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")

#Load fake_data.csv(check canvas files section) into spark RDD
fake_rdd =  sc.textFile('data/Fake_data.csv').map(lambda line: line.split(","))


print 'Assignment 4 - Fake Data Processing using RDD'

#Find birth country which has highest amount of people
print 'Birth Country with highest amount of people'
#print fake_rdd.top(5)
ctry_map_values = fake_rdd.map(lambda x: (x[1],1))
ctr_cnt_rdd = ctry_map_values.reduceByKey(lambda x,y: x+y,1)
print ctr_cnt_rdd.map(lambda s: (-1*s[1],s[0])).takeOrdered(1)
print '\n'

#Find average income of people who are born in united states
print 'Average income of people who are born in united states'
usa_rdd = fake_rdd.filter(lambda x: x[1] == 'United States of America')
usa_inc_rdd = usa_rdd.map(lambda x: ('United States',float(x[4])))
income_sum = usa_inc_rdd.combineByKey(lambda value: (value,1), lambda x,value: (x[0]+value,x[1]+1), lambda x,y: (x[0]+y[0],x[1]+y[1]))
avg_inc_rdd = income_sum.map(lambda (label,(sum_count,value)): (label,sum_count/value))
print avg_inc_rdd.top(5)

print("\n")

#How many people has income over 100,000 but their loan is not approved.
print 'Number of people has income over 100,000 but their loan is not approved.'
#inc_loan_rdd  = fake_rdd.map(lambda x: (float(x[4]),x[7]))
#print inc_loan_rdd.top(5)

loan_rdd = fake_rdd.filter(lambda x: x[4]>100000 and x[7]=='False')
print loan_rdd.count()
print("\n")

#Find top 10 people with highest income in United States. (Print their names, income and jobs)
print 'Top 10 people with highest income in United States'
print usa_rdd.map(lambda s: (-1*float(s[4]),s[3],s[6])).takeOrdered(10)
print("\n")

#How many number of distinct jobs are there?
print 'Number of distinct jobs are there'
jobs_rdd = fake_rdd.map(lambda x: x[5])
print jobs_rdd.top(5)
print jobs_rdd.distinct().count()
print("\n")

#How many writers earn less than 100,000?
print 'Number of writers earn less than 100,000'
writer_rdd = fake_rdd.filter(lambda x: 'Writer' in x[5]).map(lambda x: ('Writer',float(x[4])))
print writer_rdd.filter(lambda x: x[1]<100000).count()