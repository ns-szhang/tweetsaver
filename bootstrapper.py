"""
Bootstrapper for the TweetSaver app. This only needs to be run once,
when the database is first initialized.
"""

import os
import json
import time
import requests

from sqlalchemy import create_engine, MetaData
from twitter import TwitterAPI

PG_CONNECTION_STRING = os.environ['PG_CONNECTION_STRING']

class Bootstrapper:
    def __init__(self, twitter, pg_client, meta, user):
        self._twitter = twitter
        self._pg_client = pg_client
        self.oldest_tweet = None
        self._tweets_table = meta.tables['tweets']
        self._tweets = set()
        self._user = user
        self.get_all_tweets()

    def get_all_tweets(self):
        '''Get the set of tweet ids already in the database'''
        tweets = self._pg_client.execute(self._tweets_table.select())
        for tweet in tweets:
            self._tweets.add(tweet.tweet_id)
        return self._tweets

    def iterate(self):
        tweets = self._twitter.get_tweets(
            self._user, max_id=self.oldest_tweet, count=200)
        if len(tweets) is 0:
            return False
        for tweet in tweets:
            if self.oldest_tweet is None or self.oldest_tweet > tweet['id']:
                self.oldest_tweet = tweet['id'] - 1
            if tweet['id'] in self._tweets:
                continue
            tweet_obj = {
                'tweet_id': tweet['id'],
                'text': tweet['text'],
                'added_on': tweet['created_at']
            }
            print(tweet['id'])
            insert_tweet = self._tweets_table.insert(tweet_obj)
            self._pg_client.execute(insert_tweet)
            self._tweets.add(tweet['id'])
        return True

    def bootstrap(self):
        while(self.iterate()):
            time.sleep(1)

if __name__ == '__main__':
    twitter = TwitterAPI()
    pg_client = create_engine(PG_CONNECTION_STRING).connect()
    meta = MetaData()
    meta.reflect(bind=pg_client)
    bootstrapper = Bootstrapper(twitter, pg_client, meta, 'rmsephy')
    bootstrapper.bootstrap()
