from credentials import *
import tweepy
import logging
import pymongo

tweepy_client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    access_token=API_KEY,
    access_token_secret=API_KEY_SECRET,
    wait_on_rate_limit=True
)

if tweepy_client:
    logging.critical('\nAuthentication OK')
else:
    logging.critical('\nAuthentication failed, please verify your credentials')

mongo_client = pymongo.MongoClient(host="mongodb", port=27017)
db = mongo_client.twitter

# Search for Andrew Ng tweets

response = tweepy_client.get_user(
    username='andrewyng',
    user_fields=['name', 'id', 'created_at']
)

user = response.data

print(f'{user.name} with username {user} created their twitter account on {user.created_at}\n')

cursor = tweepy.Paginator(
    method=tweepy_client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
).flatten(limit=20)

# clear andrew_tweets documents
db.andrew_tweets.delete_many({})

for tweet in cursor:
    print(f'**{user.name} at {tweet.created_at} wrote:\n{tweet.text}\n')
    db.andrew_tweets.insert_one(dict(tweet))

# Seach for 'machine learning' tweets

query = "machine learning lang:en -is:retweet"

cursor = tweepy.Paginator(
    method=tweepy_client.search_recent_tweets,
    query=query,
    tweet_fields=['created_at'],
).flatten(limit=20)

# clear machine_learning_tweets documents
db.machine_learning_tweets.delete_many({})

for tweet in cursor:
    print(f'TWEETED ON {user.created_at}:\n{tweet.text}\n')
    db.machine_learning_tweets.insert_one(dict(tweet))

