#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import api
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
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


# ========================= Twitter Streamer =============================== #


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentification & the connection to the
        # twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
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
        except BaseException as e:
            print(" Error on_data: %s" % str(e))
        return True

    def on_error(self, status):  # how I deal with errors
        print(status)


# ================================ Main ===================================== #

if __name__ == "__main__":
    hash_tag_list = ["Donald Trump", "Macron", "France"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
