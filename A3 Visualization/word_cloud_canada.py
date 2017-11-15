# -*- coding: utf-8 -*-
"""
Wordcloud - Assignment 3
@author: Aruna Kumaraswamy
"""

import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud

d = os.getcwd()
filepath=d+"/resources/canada_housing.txt"

# Read the whole text.
def wordCloud(path):

    text = open(path).read() #read the entire file in one go
    #print text
    words_more_letters = ''
    
    words = text.split()
    for i in words:
        if len(i) >= 4:
            words_more_letters += i + ' '
    
    print words_more_letters
    wordcloud = WordCloud().generate(words_more_letters)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud)
    plt.axis("off")
    print ('Wait for the white background version ...')
    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(background_color="white", max_words=2000,max_font_size=40, relative_scaling=.4).generate(words_more_letters)

    plt.figure()

    plt.imshow(wordcloud)

    plt.axis("off")

    plt.show()





wordCloud(filepath)