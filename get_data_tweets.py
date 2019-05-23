#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import ter_credentials as ter_c
import pandas as pda


# ========================= Twitter Client ================================= #
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def stream(self, data, file_name, df):
        i = 0
        for tweet in Cursor(self.twitter_client.search, q=data, count=70, lang='fr', tweet_mode='extended').items():
            print(i, end='\r')
            if 'extended_tweet' in tweet._json:
                df.loc[i, 'Tweets'] = tweet._json['full_text']

            if 'retweeted_status' in tweet._json:
                if 'extended_tweet' in tweet._json['retweeted_status']:
                    df.loc[i, 'Tweets'] = tweet._json['retweeted_status']['full_text']
                else:
                    df.loc[i, 'Tweets'] = tweet._json['full_text']
            else:
                df.loc[i, 'Tweets'] = tweet._json['full_text']

            df.loc[i, 'User'] = tweet.user.name
            df.loc[i, 'User_statuses_count'] = tweet.user.statuses_count
            df.loc[i, 'user_followers'] = tweet.user.followers_count
            df.loc[i, 'User_location'] = tweet.user.location
            df.loc[i, 'User_verified'] = tweet.user.verified
            df.loc[i, 'fav_count'] = tweet.favorite_count
            df.loc[i, 'rt_count'] = tweet.retweet_count
            df.loc[i, 'tweet_date'] = tweet.created_at
            df.to_excel('{}.xlsx'.format(file_name))
            i += 1
            if i == 1000:
                return df
                break
            else:
                pass


# ========================= Twitter Authenticater ========================= #
class TwitterAuthenticator():
    """
    Class for authentification.
    """

    def authenticate_twitter_app(self):
        auth = OAuthHandler(ter_c.CONSUMER_KEY, ter_c.CONSUMER_SECRET)
        auth.set_access_token(ter_c.ACCESS_TOKEN, ter_c.ACCESS_TOKEN_SECRET)
        return auth


# ================================ Main ===================================== #
if __name__ == "__main__":

    # tweet_analyser = TweetAnalyser()
    print('test run')
    twitter_client = TwitterClient()

    _df = pda.DataFrame(columns = ['Tweets', 'User', 'User_statuses_count',
                             'user_followers', 'User_location', 'User_verified',
                             'fav_count', 'rt_count', 'tweet_date'])

    __df = twitter_client.stream(data=['CaseLawAnalytic'], file_name='my_tweets_predictice', df=_df)

    # __df.info()
    # print(__df.head(5))
