import os
import json
import requests

class TwitterAPI:
    def __init__(self):
        self.public_key = os.environ['TWITTER_PUBLIC_KEY']
        self.secret_key = os.environ['TWITTER_SECRET_KEY']
        self.access_token = self._get_token()

    def _get_token(self):
        # url = "https://api.twitter.com/oauth2/token"
        # data = {'grant_type': 'client_credentials'}
        # res = requests.post(
            # url, data=data, auth=(self.public_key, self.secret_key))
        # access_token = res.json()['access_token']
        access_token = "AAAAAAAAAAAAAAAAAAAAALfD1wAAAAAAod04RiiFxpvJrqSVXPEMxPJatns%3Dg19UsdQ66JFHUT6tmYgGPivqJfieBzOugb9VJVUlAxP1KYmxlC"
        return "Bearer {}".format(access_token)

    def get_tweets(self, username, max_id=None, count=20):
        params = {
            'screen_name': username,
            'trim_user': True,
            'count': count
        }
        if max_id is not None:
            params['max_id'] = max_id
        headers = {
            "Authorization": self.access_token
        }
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        res = requests.get(url, params=params, headers=headers)
        return res.json()
