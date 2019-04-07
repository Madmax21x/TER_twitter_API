#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

import ter_credentials as ter_c
import numpy
import pandas as pda
import re
import matplotlib.pyplot as plt


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
        for tweet in Cursor(self.twitter_client.user_timeline,
        id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends,
        id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,
        id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


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
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pda.DataFrame(data=[tweet.text for tweet in tweets],
        columns=['tweets'])

        df['id'] = numpy.array([tweet.id for tweet in tweets])
        df['len'] = numpy.array([len(tweet.text) for tweet in tweets])
        df['date'] = numpy.array([tweet.created_at for tweet in tweets])
        df['source'] = numpy.array([tweet.source for tweet in tweets])
        df['likes'] = numpy.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = numpy.array([tweet.retweet_count for tweet in tweets])

        return df


# ================================ Main ===================================== #
if __name__ == "__main__":
    """
    La première partie permet de récuper dans un fichier certains tweets
    avec certains mots clées : ici la "hash_tag_list"
    On peut préciser le nom du compte twitter qu'on veut analyser : par défault
    ce sera mon compte.

    Pour l'instant tout n'est pas au point car pour un compte ou il y a des
    tweets en continu ex : donaldtrump ; le débit de tweets ne s'arrête jamais.
    """

    hash_tag_list = ["Donald Trump", "Macron", "France"]
    fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('EmmanuelMacron')  # précise nom du compte
    twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    # Pour récupérer juste le 1er tweet de ma timeline ou celle d'un compte : #
    # print(twitter_client.get_user_timeline_tweets(1))

    """
    on stock dans tweets les x (ici x =200) derniers tweets d'un compte twitter
    username you can use :
    realDonaldTrump ; EmmanuelMacron ; futuroscope ; SFR ; Apple ; univbordeaux

    =>Toute la partie Analyse de la var tweets ou sont stockées tous les tweets
    se fait dans la class TweetAnalyser() : on utilise la bibliotèque pandas
    pour pouvoir stocker les tweets dans un tableau avec certaines indexations.
    Pour connaitre toutes les indexations possibles : print(dir(tweets[0]))

    => On peut choisir d'afficher ce tableau avec : print(df.head(10))
    ou 10 est le nombre de tweets qu'on veut afficher
    """
    # twitter_client = TwitterClient()
    # tweet_analyser = TweetAnalyser()
    # api = twitter_client.get_twiiter_client_api()

    # tweets = api.user_timeline(screen_name="univbordeaux", count=200)
    # tweets = api.followers(screen_name="Maxence_21_")

    # df = tweet_analyser.tweets_to_data_frame(tweets)

    # print(df.head(10))
    # print(dir(tweets[0])) # pour obtenir les key words dont on a besoin
    # print(tweets[0].retweet_count)

    """
    # Sentiment Analysis # (Ne marche qu'en anglais mais possible en fr)
    """
    # df['sentiment'] = numpy.array([tweet_analyser.analyze_sentiment(tweet)
    # for tweet in df['tweets']])

    """ Get average length over all tweets. """
    # print(numpy.mean(df['len']))

    """ Get the number of likes for the most liked tweet. """
    # print(numpy.max(df['likes']))

    """ Get the number of retweets for the most retweeted tweet. """
    # print(numpy.max(df['retweets']))

    """
    PLOT :
    Pour s'amuser, on peut créer des graphiques avec certaines infos :
    Ici on peut avoir séparément un plot des likes en fonciton du temps des
    tweets d'un certain compte avec Time likes
    On peut avoir la même chose pour les retweets
    Enfin, on peut avoir la combinaison des deux
    """

    # Time Likes
    # time_likes = pda.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), color='r')

    # Time Retweets
    # time_retweets = pda.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), color='r')

    # time_likes.plot(figsize=(16, 4), label="like", legend=True)
    # time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    # plt.show()
