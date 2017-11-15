# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 21:57:36 2017

@author: aruna
"""

import os

import matplotlib.pyplot as plt

from wordcloud import WordCloud



d = os.getcwd()

filepath="trumpSpeech.txt"

# Read the whole text.





def wordCloud(path):

    text = open(path).read() #read the entire file in one go

    wordcloud = WordCloud().generate(text)



    # Display the generated image:

    # the matplotlib way:

    plt.imshow(wordcloud)

    plt.axis("off")



    # take relative word frequencies into account, lower max_font_size

    wordcloud = WordCloud(background_color="white", max_words=2000,max_font_size=40, relative_scaling=.4).generate(text)

    plt.figure()

    plt.imshow(wordcloud)

    plt.axis("off")

    plt.show()





wordCloud(filepath)