import os
import json
import time
import requests
from sqlalchemy import create_engine, MetaData

from twitter import TwitterAPI
from bootstrapper import Bootstrapper
from screenshot import take_screenshot

PG_CONNECTION_STRING = os.environ['PG_CONNECTION_STRING']
TARGET_USER = os.environ['TARGET_USER']

class TweetDaemon:
    def __init__(self, twitter, pg_client, meta, user):
        self._twitter = twitter
        self._pg_client = pg_client
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
        tweets = self._twitter.get_tweets(self._user)
        for tweet in tweets:
            if tweet['id'] in self._tweets:
                continue
            print("Adding tweet with id:", tweet['id'])
            filename = take_screenshot(TARGET_USER, tweet['id'])
            tweet_obj = {
                'tweet_id': tweet['id'],
                'text': tweet['text'],
                'added_on': tweet['created_at'],
                'screenshot_url': filename
            }
            insert_tweet = self._tweets_table.insert(tweet_obj)
            self._pg_client.execute(insert_tweet)
            self._tweets.add(tweet['id'])
        return True

    def run(self):
        while(True):
            print("iterating")
            try:
                self.iterate()
            except Exception:
                pass
            time.sleep(15)

if __name__ == '__main__':
    twitter = TwitterAPI()
    pg_client = create_engine(PG_CONNECTION_STRING).connect()
    meta = MetaData()
    meta.reflect(bind=pg_client)
    daemon = TweetDaemon(twitter, pg_client, meta, TARGET_USER)
    daemon.run()
