import logging

from datetime import datetime
from pprint import pformat

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from google.appengine.ext import webapp
from google.appengine.ext import deferred

import twitter

from models import Tweet, KeyStore

DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

class FetchTweets(webapp.RequestHandler):

    def get(self):
        key = 'last_id'
        keystore = KeyStore.get_by_key_name(key)
        last_id = keystore and keystore.value
        tweets = twitter.get_twitter_search('%23ukbeer', last_id)
        logger.info("Fetched %d tweets", len(tweets['results']))
        for tweet in tweets['results']:
            deferred.defer(store_tweet, tweet)
        logger.debug(pformat(tweets))
        last_id = tweets['max_id']
        if last_id:
            keystore = KeyStore.get_or_insert(key, name=key)
            keystore.value = tweets['max_id_str']
            keystore.put()
        self.response.out.write("Fetched %d tweets" % len(tweets['results']))

def store_tweet(data):
    logger.info("Adding tweet to datastore")
    logger.debug("Tweet data was:\n%s", pformat(data))
    tweet = Tweet(
        user_id=data['from_user_id'],
        username=data['from_user'],
        profile_image_url=data['profile_image_url'],
        message=data['text'],
        message_id=data['id'],
        created_at=datetime.strptime(data['created_at'], DATETIME_FORMAT),
    )
    if data['geo'] and data['geo']['type'] == 'Point':
        logger.debug("Adding location: %s", data['geo']['coordinates'])
        tweet.location = "%s,%s" % tuple(data['geo']['coordinates'])
    tweet.put()
