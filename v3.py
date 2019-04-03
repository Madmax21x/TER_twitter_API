#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# os.chdir(os.getcwd() + "/../../../Documents")  # version WINDOWS
os.chdir(os.getcwd() + "/Documents")  # version MAC

cwd = os.getcwd()
fichier = open("key_ter.txt", "r")
text = fichier.read().strip()
fichier.close()
tempL = text.split(';')

consumer_key = tempL[0]
consumer_secret = tempL[1]
access_token = tempL[2]
access_token_secret = tempL[3]


# ========================= Twitter Client ================================= #
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twiiter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# ========================= Twitter Authenticater ========================= #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth


# ========================= Twitter Streamer =============================== #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentification & the connection to the
        # twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # filtrer les tweets à partir des hashtags
        stream.filter(track=hash_tag_list)


# ====================== Twitter Stream Listener =========================== #
class TwitterListener(StreamListener):

    """
     This is a basic listener class that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print(" Error on_data: %s" % str(e))
        return True

    def on_error(self, status):  # how I deal with errors
        if status == 420:
            # Returning Fasle on_data_method in case rate limit occurs.
            return False
        print(status)


# ========================== Tweet Analyser ================================ #
class TweetAnalyser():
    """
    Functionality for analysing and categorizing content from tweets.
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


# ================================ Main ===================================== #
if __name__ == "__main__":
    # hash_tag_list = ["Donald Trump", "Macron", "France"]
    # fetched_tweets_filename = "tweets.txt"

    # twitter_client = TwitterClient('Carlito_delaf')  # précise nom du compte
    # print(twitter_client.get_user_timeline_tweets(1))  # permet de recup 1er tweet de ma timeline
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser()
    api = twitter_client.get_twiiter_client_api()

    tweets = api.user_timeline(screen_name="EmmanuelMacron", count=20)

    df = tweet_analyser.tweets_to_data_frame(tweets)
    # print(df.head(20))

    # print(dir(tweets[0]))
    # print(tweets[0].retweet_count)

    # Get average length over all tweets.
    print(np.mean(df['len']))

    # Get the number of likes for the most liked tweet.
    print(np.max(df['likes']))

    # Get the number of retweets for the most retweeted tweet.
    print(np.max(df['retweets']))

    # Time Series
    time_likes = pd.Series(data=df['likes'].values, index=df['data'])
    time_likes.plot(figsize=(16, 4), color='r')
    plt.show()
