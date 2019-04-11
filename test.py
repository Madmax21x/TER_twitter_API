from v3 import *

if __name__ == '__main__':

    text = ("Liste des choix : \n - hash_tag_list : stream API : type (1)\n"
    "- To select a twitter account and get information : type (2)\n"
    "- To get tweets for a specific hashtag : type (3)\n"
    "- If you want to do sentiment anaysis : type (4)\n"
    "- To get the list of followers for a twitter account : type(5)\n"
    "- To get specific infomations about a tweet : type (6)\n"
    "- To plot a graph of likes or retweets through time for on account:"
    " type(7)\n")

    _continue = True

    while _continue is True:
        choice = int(input(text))
        # if not os.path.isfile(param): ValueError("need a python file")
        assert isinstance(choice, int), "%s is not a int" % choice
        if choice not in [1,2,3,4,5,6, 7]:
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
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 2:
                _account = input("Type in twitter account\n(ex:realDonaldTrump"
                "; EmmanuelMacron ; futuroscope ; SFR ; Apple ; univbordeaux)\n")
                twitter_client = TwitterClient(_account)

                answer = input(" Get the first tweet of account timeline ? y/n\n")
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
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 3:
                _account = input("Type in twitter account\n(ex:realDonaldTrump"
                "; EmmanuelMacron ; futuroscope ; SFR ; Apple ; univbordeaux)\n")

                _hashtag = input(" Type in hashtag or key word wanted :\n"
                "(ex: sfr ; sncf ; france)\n")

                _lang = input("Which language ? (ex: en ; fr)\n")
                _nb = int(input("How many tweets ?\n"))

                _nb_df = int(input("How many tweets do you want to show"
                "in the data frame ?\n"))

                twitter_client = TwitterClient(_account)
                tweet_analyser = TweetAnalyser()

                _get_txt = ("- get_user_timeline_tweets : type(1)\n"
                            "- get_friend_list : type(2)\n"
                            "- get_home_timeline_tweets type(2)\n")
                get_choice = int(input(_get_txt))

                # start_date = datetime.datetime(2019, 4, 8, 0, 0, 0)
                # end_date = datetime.datetime(2018, 3, 28, 0, 0, 0)
                # tweets = twitter_client.get_hashtag_tweets(20, 'sfr', 'fr', start_date)

                if get_choice == 1:
                    pass
                elif get_choice == 2:
                    pass
                elif get_choice ==3:
                    pass
                tweets = twitter_client.get_hashtag_tweets(_nb, _hashtag, _lang)
                df = tweet_analyser.tweets_to_data_frame(tweets)
                df['sentiment'] = npy.array([tweet_analyser.analyze_sentiment(tweet)for tweet in df['tweets']])
                print(df.head(_nb_df))
                print()
                print("#===================== CONTINUE ?====================#")
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 4:
                print(" - Only available in English for now.")

                # df['sentiment'] = npy.array([tweet_analyser.analyze_sentiment(tweet)for tweet in df['tweets']])
                # print(df.head(20))
                print("#===================== CONTINUE ?====================#")
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 5:
                print("#===================== CONTINUE ?====================#")
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 6:
                print("#===================== CONTINUE ?====================#")
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
            elif choice == 7:
                print("#===================== CONTINUE ?====================#")
                answer = int(input(" Continue ? 0/1\n"))
                if answer == 0:
                    _continue = False
