#!/usr/bin/env python3
# -*- coding: utf8 -*-
import numpy as npy
import pandas as pda
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import re
import cufflinks
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


# ================================ Main ===================================== #
if __name__ == "__main__":
    print("lol")
    # Read excel file into df
    df = pda.read_excel('test1.xlsx')

    # get info
    df.info()

    # show first five
    print(df.head(5))

    # Add new sentiment column
    df['clean_tweet'] = df['Tweets'].apply(lambda x: clean_tweet(x))
    df['Sentiment'] = df['clean_tweet'].apply(lambda x: analyze_sentiment(x))

    # see if has worked
    n = 500
    print('Original tweet:\n' + df['Tweets'][n])
    print()
    print('Clean tweet:\n'+df['clean_tweet'][n])
    print()
    print('Sentiment:\n'+df['Sentiment'][n])

    # see data distribution
    # df['Sentiment'].value_counts().py.plot(kind='bar',
    #                                 xTitle='Sentiment',
    #                                 yTitle='Count',
    #                                 title='Overall Sentiment Distribution')
    plotly.offline.plot(df['Sentiment'].value_counts()(kind='bar', xTitle='Sentiment'))

    # trace0 = go.Scatter(
    # x=[1, 2, 3, 4],
    # y=[10, 15, 13, 17]
    # )
    # trace1 = go.Scatter(
    #     x=[1, 2, 3, 4],
    #     y=[16, 5, 11, 9]
    # )
    # data = [trace0, trace1]
    #
    # ply.plot(data, filename = 'basic-line', auto_open=True)
