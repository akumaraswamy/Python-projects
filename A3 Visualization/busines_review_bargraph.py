# -*- coding: utf-8 -*-
"""
Bar graph for business reviews
@author: Aruna Kumaraswamy
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

d = os.getcwd()

#Read CSV file
business_reviews = pd.read_csv(d+"/resources/barGraph.csv")

#Create index and required columns
idx = pd.DataFrame(business_reviews['Business'])
df = pd.DataFrame({'Anticipation':business_reviews['anticipation'],'Enjoyment':business_reviews['enjoyment'],
                  'Sad':business_reviews['sad'],'Disgust':business_reviews['disgust'],
                'Anger':business_reviews['anger'],'Surprise':business_reviews['surprise'],
                'Fear':business_reviews['fear'],'Trust':business_reviews['trust'], })

df.index = idx
plt.figure(figsize=(10,10), dpi=300).add_subplot(111)
ax = df.plot(kind='bar', x=df.index, stacked=False, color=['red','purple','yellow','green','orange','teal','blue','black'])

plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches(15, 10)

plt.ylabel('Emotion Count')
plt.xlabel('Business')
plt.title('Business Review based on expressed emotion')
#plt.savefig("business_review_bar.png", dpi=300) 