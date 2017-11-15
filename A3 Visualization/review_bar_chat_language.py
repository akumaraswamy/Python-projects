# -*- coding: utf-8 -*-
"""
Bar chart for language usage in reviews
@author: Aruna Kumaraswamy
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

d = os.getcwd()

# Read the input delimited text
business_reviews = pd.read_table(d+"/resources/ReviewID.txt",delimiter=':',names=['language'],usecols=[1])
#Interested only in language column
aggr_df = business_reviews.groupby([business_reviews['language']]).size()

#Calculate the percentage
aggr_df = pd.DataFrame(aggr_df,columns=['count'])
count = business_reviews['language'].count()
aggr_df['count'] = (aggr_df['count']/count)*100


plt.figure(figsize=(10,10), dpi=300).add_subplot(111)
ax = aggr_df.plot(kind='bar', stacked=False, color=['teal'])

plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches(15, 10)

plt.ylabel('Language Count')
plt.xlabel('Language')
plt.title('Language used in reviews')
#plt.savefig("business_review_lang_bar.png", dpi=300) 