import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# Get the User object for twitter...
user = api.get_user('thibaultmrs')
# print(user)
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
# print(friend.screen_name)

print(user)
lol = api.me()
a = 44.831170
b = -0.572560

k = api.trends_closest(a, b)
print(k)
print("s")

print("4")

myself = api.me()
print(myself)

# for followers in user.followers():
# print(followers)

# followers = api.followers()
# print(followers)

#followers_id = api.followers_ids()


# === permet de récupérer les derniers tweets avec ce hashtag

# cricTweet = tweepy.Cursor(api.search, q='ryanair').items(10)
#
# number = 0
# for tweet in cricTweet:
#    print(tweet.created_at, tweet.text, tweet.lang)
#    number += 1
# print(number)


# === pour avoir les derniers tweets de l'utilisateur

user_tweet = api.user_timeline()
for tweet in user_tweet:
    print(tweet)

# === récupérer les tweets qui ont été retweetés

user_retweet = api.retweets_of_me
for tweet in user_retweet:
    print(tweet)
