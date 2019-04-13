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

    def get_hashtag_tweets(self, num_tweets, query, language=None, start_date=None, end_date=None):
        hashtag_tweets = []
        for tweet in Cursor(self.twitter_client.search,
        q=query, lang=language,  tweet_mode='extended', since=start_date).items(num_tweets):
            # if tweet.created_at < end_date and tweet.created_at > start_date:
            # if 'retweeted_status' in dir(tweet):
            #     hashtag_tweets.append(tweet.retweeted_status.full_text)
            # else:
            #     hashtag_tweets.append(tweet.full_text)
            hashtag_tweets.append(tweet)
        return hashtag_tweets

    def get_trends(self, country_WOE_ID):
        # trends = self.twitter_client.trends_place(1)
        # trend_data = []
        # liste_tweets =[]
        # for trend in trends[0]["trends"]:
        #     trend_tweets = []
        #     trend_tweets.append(trend['name'])
        #     #for tweet in Cursor(self.twitter_client.search, q = trend['name'], lang=language).items(num_tweets):
        #         #liste_tweets.append(tweet)
        #     trend_data.append(tuple(trend_tweets))
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
    """
    La première partie : permet de récuper dans un fichier certains tweets
    avec certains mots clés : ici la "hash_tag_list"

    Pour l'instant tout n'est pas au point car il y aura des tweets en continu
    ( un peu comme une boucle infinie ) si on utilise stream_tweets()

    La seconde partie :
    On peut préciser le nom du compte twitter qu'on veut analyser : par défault
    ce sera mon compte.

    On a pour le moment mis à disposition 3 méthodes :
    - get_user_timeline_tweets(Pour récupérer les tweets d'un compte en direct)
    - get_friend_list(Pour récupérer la liste d'amis d'un compte en direct)
    - get_home_timeline_tweets(Pour récupérer le 1er tweet de la timeline QUE
    de mon compte)

    """
    # 1ère partie #
    # hash_tag_list = ["Donald Trump", "Macron", "France"]
    # fetched_tweets_filename = "tweets.txt"
    #
    # twitter_streamer = TwitterStreamer()

    # ATTENTION : boucle infinie : #
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    # 2ème Partie #
    twitter_client = TwitterClient()  # précise nom du compte

    # Pour récupérer le 1er tweet de ma timeline ou celle d'un autre compte : #
    # print(twitter_client.get_user_timeline_tweets(1))

    # Pour récupérer le 1er follower ma liste de followers ou celle d'un autre
    # compte : #
    # print(twitter_client.get_follower_list(1))

    # Pour récupérer le 1er ami ma liste d'amis ou celle d'un autre compte : #
    # print(twitter_client.get_friend_list(1))

    # Pour récupérer le 1er tweet de la timeline QUE de mon compte : #
    # print(twitter_client.get_home_timeline_tweets(1))

    # Pour récupérer certains tweet avec un certain hashtag #
    # print(twitter_client.get_hashtag_tweets(20, 'teich', 'fr'))
    tweet_analyser = TweetAnalyser()

    start_date = datetime.datetime(2019, 4, 8, 0, 0, 0)
    # end_date = datetime.datetime(2018, 3, 28, 0, 0, 0)

    tweets = twitter_client.get_hashtag_tweets(20, 'sfr', 'fr', start_date)
    # tweets = twitter_client.get_hashtag_tweets(20, 'App', 'en')
    # df = tweet_analyser.tweets_to_data_frame(tweets)
    # print(df)
    # (tweets)

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
    #
    # api = twitter_client.get_twitter_client_api()
    #
    # tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
    # # # tweets = api.followers(screen_name="")
    #
    # df = tweet_analyser.tweets_to_data_frame(tweets)

    # print(df.head(10))
    # print(dir(tweets[0])) # pour obtenir les key words dont on a besoin
    # print(tweets[0].retweet_count)

    """
    -> On stock aussi dans un tableau les informations qu'on peut avoir sur les
    followers d'un utilisateur (localisation, nombre de followers, amis..)
    On affiche le tableau avec print(df)
    """
    # twitter_client = TwitterClient('EmmanuelMacron')
    # follower_analyser = FollowerAnalyzer()
    #
    # follower_list = twitter_client.get_follower_list(20)
    #
    # df = follower_analyser.followers_to_data_frame(follower_list)
    # print(df)

    """
    # Sentiment Analysis # (Ne marche qu'en anglais mais possible en fr)
    """
    # df['sentiment'] = npy.array([tweet_analyser.analyze_sentiment(tweet)for tweet in df['tweets']])
    # print(df.head(20))
    """ Get average length over all tweets. """
    # print(npy.mean(df['len']))

    """ Get the number of likes for the most liked tweet. """
    # print(npy.max(df['likes']))

    """ Get the number of retweets for the most retweeted tweet. """
    # print(npy.max(df['retweets']))

    """
    PLOT :
    Pour s'amuser, on peut créer des graphiques avec certaines infos :
    Ici on peut avoir séparément un plot des likes en fonciton du temps des
    tweets d'un certain compte avec Time likes
    On peut avoir la même chose pour les retweets
    Enfin, on peut avoir la combinaison des deux
    """

    # # Time Likes
    # time_likes = pda.Series(data=df['likes'].values, index=df['date'])
    # # time_likes.plot(figsize=(16, 4), color='r')
    #
    # # Time Retweets
    # time_retweets = pda.Series(data=df['retweets'].values, index=df['date'])
    # # time_retweets.plot(figsize=(16, 4), color='r')
    #
    # time_likes.plot(figsize=(16, 4), label="like", legend=True)
    # time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    # plt.show()
