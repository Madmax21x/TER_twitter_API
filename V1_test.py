#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import numpy as npy
import pandas as pda
import ter_credentials as ter_c


# ========================= Twitter Authenticater ========================= #
class TwitterAuthenticator():
    """
    Class for authentification.
    """

    def authenticate_twitter_app(self):
        auth = OAuthHandler(ter_c.CONSUMER_KEY, ter_c.CONSUMER_SECRET)
        auth.set_access_token(ter_c.ACCESS_TOKEN, ter_c.ACCESS_TOKEN_SECRET)
        return auth


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
                tf.close()
            return True
        except BaseException as e:
            print(" Error on_data: %s" % str(e))
        return True

    def on_error(self, status):  # how I deal with errors
        if status == 420:
            # Returning Fasle on_data_method in case rate limit occurs.
            return False
        print(status)


# ================================ Main ===================================== #
if __name__ == "__main__":

    # twitter_client = TwitterClient()
    # tweet_analyser = TweetAnalyser()
    print('test run')
