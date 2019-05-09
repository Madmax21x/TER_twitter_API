# from v3 import *
from v3_text_blob import *
import pandas as pda
import numpy as npy
import matplotlib.pyplot as plt

if __name__ == '__main__':

    text = ("Liste des choix : \n - hash_tag_list : stream API : 1\n"
    "- To select a twitter account and get information : 2\n"
    "- To get tweets from user timeline: 3\n"
    "- To get tweets with a specific #hashtag : 4\n"
    "- To get the list of followers for a twitter account : 5\n"
    "- To get TRENDS : 6\n"
    "- To get other # Frequency : 7\n")

    _continue = True

    while _continue is True:
        choice = int(input(text))
        # if not os.path.isfile(param): ValueError("need a python file")
        assert isinstance(choice, int), "%s is not a int" % choice
        if choice not in [1, 2, 3, 4, 5, 6, 7]:
            print("choice has to be be between 1 & 7.")
        else:
            if choice == 1:
                _input_list = input("Type in hashtag words: (ex: Donald Trump"
                "; Macron; France ) :\n")
                hash_tag_list = []
                for elem in _input_list.split(';'):
                    hash_tag_list.append(elem)
                tweets_filename = "tweets.txt"
                twitter_streamer = TwitterStreamer()
                # ATTENTION : boucle infinie :#
                twitter_streamer.stream_tweets(tweets_filename, hash_tag_list)
                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 2:
                _account = input("Type in twitter account\n(ex:realDonaldTrump"
                "; EmmanuelMacron ; futuroscope ; SFR ; elonmusk ;"
                "univbordeaux)\n")
                twitter_client = TwitterClient(_account)

                answer = input("Get the first tweet of account timeline ? y/n\n")
                if answer == "y":
                    print(twitter_client.get_user_timeline_tweets(1))

                answer = input(" Get the first follower of account ? y/n\n")
                if answer == "y":
                    print(twitter_client.get_follower_list(1))

                answer = input(" Get the first friend of account ? y/n\n")
                if answer == "y":
                    print(twitter_client.get_friend_list(1))

                answer = input(" Get the first tweet my account timeline ? y/n\n")
                if answer == "y":
                    print(twitter_client.get_home_timeline_tweets(1))
                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 3:
                _account = input("Type in twitter account\n(ex:realDonaldTrump"
                "; EmmanuelMacron ; futuroscope ; SFR ; elonmusk ; univbordeaux)\n")
                _l = input("Which language ? (ex: en ; fr)\n")
                _nb = int(input("Number of tweets ?\n"))
                _nb_df = int(input("How many tweets do you want to show"
                " in the data frame ?\n"))

                twitter_client = TwitterClient(_account)
                tweet_analyser = TweetAnalyser()
                tweets = twitter_client.get_user_timeline_tweets(_nb)
                df = tweet_analyser.tweets_to_data_frame(tweets, _l)

                print(df.head(_nb_df))
                print()
                df_1 = pda.DataFrame(data=[_account], columns=['timeline Stats'])
                df_1[' average len'] = npy.mean(df['len'])
                df_1['+likes'] = npy.max(df['likes'])
                df_1['+retweets'] = npy.max(df['retweets'])
                print(df_1)
                print()
                _choice = input("-Plot nb of Likes through times : 1\n"
                "-Plot nb of retweets through times : 2\n"
                "-Plot both together : 3\n"
                "-Plot pie chart of sentiments : 4\n"
                "-Pass : ' '\n")

                if _choice == "1":
                    time_likes = pda.Series(data=df['likes'].values,
                                index=df['date'])
                    time_likes.plot(figsize=(16, 4), color='r')
                    plt.show()
                elif _choice == "2":
                    time_retweets = pda.Series(data=df['retweets'].values,
                                index=df['date'])
                    time_retweets.plot(figsize=(16, 4), color='r')
                    plt.show()
                elif _choice == "3":
                    time_likes = pda.Series(data=df['likes'].values,
                                index=df['date'])
                    time_retweets = pda.Series(data=df['retweets'].values,
                                index=df['date'])
                    time_likes.plot(figsize=(16, 4), label="like", legend=True)
                    time_retweets.plot(figsize=(16, 4), label="retweets",
                                legend=True)
                    plt.show()
                elif _choice == "4":
                    positive = 0
                    negative = 0
                    neutral = 0
                    for elem in df['sentiment'].values:
                        if elem > 0:
                            positive += 1
                        elif elem < 0:
                            negative += 1
                        else:
                            neutral += 1

                    colors = ['#00cec9', '#192a56', '#ffeaa7']
                    sizes = [positive, negative, neutral]
                    labels = 'Positive', 'Negative', 'Neutral'
                    plt.pie(x=sizes, shadow=True, colors=colors,
                            labels=labels, startangle=90, autopct='%.1f%%')
                    plt.show()
                print()
                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 4:
                _hashtag = input(" Type in hashtag or key word wanted :\n"
                "(ex: sfr ; sncf ; france)\n")
                _l = input("Which language ? (ex: en ; fr)\n")
                _nb = int(input("Number of tweets ?\n"))
                _nb_df = int(input("How many tweets do you want to show"
                "in the data frame ?\n"))

                twitter_client = TwitterClient()
                tweet_analyser = TweetAnalyser()

                # start_date = datetime.datetime(2019, 4, 8, 0, 0, 0)
                # end_date = datetime.datetime(2018, 3, 28, 0, 0, 0)
                # tweets = twitter_client.get_hashtag_tweets(20, 'sfr', 'fr', start_date)

                tweets = twitter_client.get_hashtag_tweets(_nb, _hashtag, _l)
                df = tweet_analyser.tweets_to_data_frame(tweets, _l)
                print(df.head(_nb_df))
                print()
                df_1 = pda.DataFrame(data=[_hashtag], columns=[' # Stats'])
                df_1[' average len'] = npy.mean(df['len'])
                df_1['+likes'] = npy.max(df['likes'])
                df_1['+retweets'] = npy.max(df['retweets'])
                print(df_1)
                print()
                _choice = input("-Plot nb of Likes through times : 1\n"
                "-Plot nb of retweets through times : 2\n"
                "-Plot both together : 3\n"
                "-Pass : ' '\n")

                if _choice == "1":
                    time_likes = pda.Series(data=df['likes'].values,
                                index=df['date'])
                    time_likes.plot(figsize=(16, 4), color='r')
                    plt.show()
                elif _choice == "2":
                    time_retweets = pda.Series(data=df['retweets'].values,
                                index=df['date'])
                    time_retweets.plot(figsize=(16, 4), color='r')
                    plt.show()
                elif _choice == "3":
                    time_likes = pda.Series(data=df['likes'].values,
                                index=df['date'])
                    time_retweets = pda.Series(data=df['retweets'].values,
                                index=df['date'])
                    time_likes.plot(figsize=(16, 4), label="like", legend=True)
                    time_retweets.plot(figsize=(16, 4), label="retweets",
                                legend=True)
                    plt.show()
                print()
                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 5:
                _account = input("Type in twitter account\n(ex:realDonaldTrump"
                "; EmmanuelMacron ; futuroscope ; SFR ; Apple ; univbordeaux)\n")
                _nb = int(input("Number of followers ?\n"))
                _nb_df = int(input("How many followers do you want to show"
                "in the data frame ?\n"))

                twitter_client = TwitterClient(_account)
                follower_analyser = FollowerAnalyzer()
                follower_list = twitter_client.get_follower_list(_nb)
                df = follower_analyser.followers_to_data_frame(follower_list)
                print(df.head(_nb_df))

                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 6:
                _woe_id = input("Type in WOE_ID :(default set to France)\n"
                " Bordeaux : 580778 ; Paris : 615702 ; N-Y : 2347591\n")
                twitter_client = TwitterClient()
                if _woe_id == '':
                    trends = twitter_client.get_trends()
                else:
                    trends = twitter_client.get_trends(int(_woe_id))

                print(trends)
                print()
                print("#===================== CONTINUE ?====================#")
                answer = input(" Continue ? y/n\n")
                if answer == "n":
                    _continue = False
            elif choice == 7:
                _hashtag = input(" Type in hashtag or key word wanted :\n"
                "(ex: sfr ; sncf ; france)\n")
                _l = input("Which language ? (ex: en ; fr)\n")
                _nb = int(input("Number of tweets ?\n"))

                twitter_client = TwitterClient()
                tweet_analyser = TweetAnalyser()

                # start_date = datetime.datetime(2019, 4, 8, 0, 0, 0)
                # end_date = datetime.datetime(2018, 3, 28, 0, 0, 0)
                # tweets = twitter_client.get_hashtag_tweets(20, 'sfr', 'fr', start_date)

                tweets = twitter_client.get_other_hashtag(_nb, _hashtag, _l)

                print("Les mots les plus fréquents:")
                print(tweets[0])
                print("Les hashtags présents:")
                print(tweets[1])
