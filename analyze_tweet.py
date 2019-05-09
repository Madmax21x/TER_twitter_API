#!/usr/bin/env python3
# -*- coding: utf8 -*-
import numpy as npy
import pandas as pda
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import re
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import plot
import cufflinks
import matplotlib.pyplot as plt
import pandas as pda

cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='pearl', offline=True)

plotly.tools.set_credentials_file(username='Maxmaz_21', api_key='ZdVMeKJACewRzgFGxZzo')


# ============================== cleaning =================================== #
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())


# ============================== sentiment ================================== #
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


# ============================== Pie graph ================================== #
def generate_pie_graph(df):
    """
    To see data distribution
    """
    _x = ['Positive', 'Negative', 'Neutral']
    _y = [df['Sentiment'].value_counts()['Positive'],
        df['Sentiment'].value_counts()['Negative'],
        df['Sentiment'].value_counts()['Neutral']]
    trace1 = {
      "hole": 0.7,
      "labels": _x,
      "marker": {
        "colors": ["#CEA447", "#16335B", "#43AEA8"],
        "line": {"color": "gray"}
      },
      "name": "Test",
      "type": "pie",
      "uid": "a682f7",
      "values": _y
    }
    data = Data([trace1])
    layout = {
      "autosize": True,
      "font": {"family": "Roboto"},
      "height": 480,
      "hiddenlabels": [None],
      "hovermode": "closest",
      "legend": {
        "x": 0.3029690069703334,
        "y": 0.5880331896725336
      },
      "margin": {
        "r": 10,
        "t": 55,
        "b": 40,
        "l": 60
      },
      "paper_bgcolor": "rgba(255, 255, 255, 0)",
      "showlegend": True,
      "title": "Sentiment Anlaysis",
      "titlefont": {"family": "Roboto"},
      "width": 485
    }
    frame1 = {
      "layout": {
        "autosize": True,
        "font": {"family": "Roboto"},
        "height": 300,
        "hovermode": "closest",
        "legend": {
          "x": 0.23419500988308342,
          "y": 0.6814430984363011,
          "font": {"size": 11}
        },
        "margin": {
          "r": 10,
          "t": 55,
          "b": 40,
          "l": 10
        },
        "paper_bgcolor": "rgba(255, 255, 255, 0)",
        "showlegend": True,
        "title": "Autre titre",
        "titlefont": {
          "family": "Roboto",
          "size": 15
        },
        "width": 300
      },
      "name": "workspace-breakpoint-0"
    }
    frames = Frames([frame1])

    # Frames are not yet supported for use with Python.
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)


# ============================== Wordcloud ================================== #
def generate_worcloud(df):
    """
    Word Frequency in a wordcloud image.
    """
    all_tweets = ' '.join(tweet for tweet in df['clean_tweet'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(all_tweets)

    plt.figure(figsize = (16,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# ============================= frequencies ================================= #
def plot_frequencies(df):
    all_tweets = ' '.join(tweet for tweet in df['clean_tweet'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(all_tweets)

    df_freq = pda.DataFrame.from_dict(data=wordcloud.words_, orient='index')
    df_freq = df_freq.head(20)
    df_freq.plot.bar(figsize = (16,4))
    plt.xticks(fontsize=5, rotation=30)
    plt.show()


# ================================ Main ===================================== #
if __name__ == "__main__":
    # Read excel file into df
    df = pda.read_excel('test1.xlsx')

    # # get info
    # df.info()

    # # show first five
    # print(df.head(5))

    # # Add new sentiment column & clean tweets
    df['clean_tweet'] = df['Tweets'].apply(lambda x: clean_tweet(x))
    df['Sentiment'] = df['clean_tweet'].apply(lambda x: analyze_sentiment(x))

    # # generate Pie Graph of sentiment
    # generate_pie_graph(df)

    # # words Frequency
    # generate_worcloud(df)

    # # plot the frequencies
    # plot_frequencies(df)
