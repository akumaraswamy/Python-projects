# -*- coding: utf-8 -*-
"""
Pie chart for total reviews by business 
@author: Aruna Kumaraswamy
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


relativePath=os.getcwd()

dataFilePath=relativePath+"/resources/barGraph.csv"

business_reviews = pd.read_csv(dataFilePath)

business_reviews['total_reviews'] = business_reviews['anticipation']+business_reviews['enjoyment']+business_reviews['sad']+ business_reviews['disgust']+business_reviews['anger']+business_reviews['surprise']+business_reviews['fear']+business_reviews['trust']
                  
colors=['red','purple','yellow','green','orange','teal','blue','black']                  
explode = (0,0.1,0,0,0,0)

# Create a pie chart
plt.pie(
    business_reviews['total_reviews'],
    labels=business_reviews['Business'],
    # with no shadows
    shadow=False,
    # with colors
    colors=colors,
    # with one slide exploded out
    explode=explode,
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    )

# View the plot drop above
plt.axis('equal')

# View the plot
plt.tight_layout()
plt.show()
#plt.savefig("business_review_pie.png", dpi=300) 