import pymongo
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Establish a connection to the MongoDB server
mdb_client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use within the MongoDB server
db = mdb_client.twitter

pg = create_engine('postgresql://postgres:1234@postgresdb:5432/twitter', echo=True)
sentiment_analyzer = SentimentIntensityAnalyzer()

def extract():    
    df_tweets = pd.concat([pd.DataFrame(db.andrew_tweets.find()), pd.DataFrame(db.machine_learning_tweets.find())])
    return df_tweets

def analyse_tweets(df_tweets):
    df_tweets['sentiment'] = [sentiment_analyzer.polarity_scores(text)['compound'] for text in df_tweets['text']]

def load(df_tweets):
    df_tweets.drop(columns=['_id', 'public_metrics']).to_sql('tweets', pg, if_exists='replace')

df = extract()
analyse_tweets(df)
load(df)

