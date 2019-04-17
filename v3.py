#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import datetime

import ter_credentials as ter_c
import numpy as npy
import pandas as pda
import re
import matplotlib.pyplot as plt
import json
import collections

# ========================= Twitter Client ================================= #
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,
        id=self.twitter_user, tweet_mode='extended').items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends,
        id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_follower_list(self, num_follower):
        follower_list = []
        for follower in Cursor(self.twitter_client.followers,
        id=self.twitter_user).items(num_follower):
            follower_list.append(follower)
        return follower_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,
        id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_hashtag_tweets(self, num_tweets, query, language=None, start_date=None):
        hashtag_tweets = []
        for tweet in Cursor(self.twitter_client.search,
                            q=query,
                            lang=language,
                            tweet_mode='extended',
                            since=start_date).items(num_tweets):
            # if tweet.created_at < end_date and tweet.created_at > start_date:
            hashtag_tweets.append(tweet)
        return hashtag_tweets

    def get_other_hashtag(self, num_tweets, query, language=None):
        tweets_hash = self.get_hashtag_tweets(num_tweets, query, language)
        liste_to_clean = ['que','est','une','Une','pas','suis', 'elle', 'Elle',
        'Nous', 'nous','ont','vous','Vous', 'avons', 'avez', 'pour', 'Pour',
        'par']

        tweets_text = []
        for tweet in tweets_hash:
            if 'retweeted_status' in dir(tweet):
                tweets_text.append(tweet.retweeted_status.full_text)
            else:
                tweets_text.append(tweet.full_text)

        # Les mots les plus fréquents dans les tweets avec un #
        for text in tweets_text:
            for elem in liste_to_clean:
                if elem in text:
                    text = text.replace(elem, '')
            counts = collections.Counter(text.split())
            counts.most_common()
            liste_frequent = []
            liste_hashtags = []
            for cle, values in counts.items():
                if values >= 2 and len(cle) >= 3:
                    liste_frequent.append({cle, values})
                if cle[0] == '#':
                    liste_hashtags.append({cle, values})
        return (liste_frequent, liste_hashtags)

    def get_trends(self, country_WOE_ID=23424819):
        # France_WOE_ID = 23424819
        country_trends = self.twitter_client.trends_place(country_WOE_ID)

        trends = json.loads(json.dumps(country_trends, indent=1))
        liste_tweets = []
        for trend in trends[0]["trends"]:
            # si on veut juste récupérer juste le hashtag
            # liste_tweets.append(trend['name'])
            # si on récupère plus d'info
            liste_tweets.append(trend)

        return liste_tweets


# ========================= Twitter Authenticater ========================= #
class TwitterAuthenticator():
    """
    Class for authentification.
    """

    def authenticate_twitter_app(self):
        auth = OAuthHandler(ter_c.CONSUMER_KEY, ter_c.CONSUMER_SECRET)
        auth.set_access_token(ter_c.ACCESS_TOKEN, ter_c.ACCESS_TOKEN_SECRET)
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


# ========================== Tweet Analyser ================================ #
class TweetAnalyser():
    """
    Functionality for analysing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        # emoji_pattern = re.compile("["
        # u"\U0001F600-\U0001F64F"  # emoticons
        # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        # u"\U0001F680-\U0001F6FF"  # transport & map symbols
        # u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        #                    "]+", flags=re.UNICODE)
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        # return emoji_pattern.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", tweet)

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pda.DataFrame(data=[tweet.full_text for tweet in tweets],
        columns=['tweets'])

        df['id'] = npy.array([tweet.id for tweet in tweets])
        df['len'] = npy.array([len(tweet.full_text) for tweet in tweets])
        df['date'] = npy.array([tweet.created_at for tweet in tweets])
        df['source'] = npy.array([tweet.source for tweet in tweets])
        df['likes'] = npy.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = npy.array([tweet.retweet_count for tweet in tweets])
        df['sentiment'] = npy.array([self.analyze_sentiment(tweet.full_text)for tweet in tweets])

        return df

# ========================= Twitter InfoFollower ============================ #

class FollowerAnalyzer():
    """
    Functionality for analysing and categorizing information about followers.
    """

    def followers_to_data_frame(self, followers):

        df = pda.DataFrame(data=[follower.screen_name for follower in
        followers], columns=['screen_name'])
        df['location'] = npy.array([follower.location for follower in
        followers])
        df['protected'] = npy.array([follower.protected for follower in
        followers])
        df['verified'] = npy.array([follower.verified for follower in
        followers])
        df['num_follower'] = npy.array([follower.followers_count for follower
        in followers])
        df['num_friends'] = npy.array([follower.friends_count for follower
        in followers])
        df['num_tweet'] = npy.array([follower.statuses_count for follower
        in followers])
        return df


# ================================ Main ===================================== #
if __name__ == "__main__":
    # _hashtag = input(" Type in hashtag or key word wanted :\n"
    # "(ex: sfr ; sncf ; france)\n")
    # _l = input("Which language ? (ex: en ; fr)\n")
    # _nb = int(input("Number of tweets ?\n"))
    # _nb_df = int(input("How many tweets do you want to show"
    # "in the data frame ?\n"))

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser()

    start_date = datetime.datetime(2019, 3, 28, 0, 0, 0)
    # end_date = datetime.datetime(2018, 3, 28, 0, 0, 0)
    date_since = "2019-04-11"
    tweets = twitter_client.get_hashtag_tweets(12, 'sfr', 'fr', date_since)

    # tweets = twitter_client.get_hashtag_tweets(_nb, _hashtag, _l)
    df = tweet_analyser.tweets_to_data_frame(tweets)
    print(df.head(10))
