import tweepy
from pymongo.errors import DuplicateKeyError

from twtstrmr.logger import get_logger
from twtstrmr.utils import save_status_to_db, update_status_in_db

logger = get_logger('twtstrmr.twitter')


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    """Authentication handler to Twitter API.

    Arguments:
        consumer_key {str} -- consumer token
        consumer_secret {str} -- consumer token secret
        access_token {str} -- access token
        access_token_secret {str} -- access token secret

    Returns:
        tweepy.API -- a wrapper for the API as provided by Twitter
    """
    auth_ = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_.set_access_token(access_token, access_token_secret)
    return tweepy.API(
        auth_,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=3,
        retry_delay=5,
        retry_errors=set([401, 404, 500, 503]))


class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, collection=None):
        super().__init__()
        self.collection = collection

    def on_status(self, status):
        status = status._json
        try:
            save_status_to_db(status=status, collection=self.collection)
        except DuplicateKeyError:
            update_status_in_db(status=status, collection=self.collection)
            logger.info("Updated earlier found duplicate key @"
                        f"{status['id_str']}")

    def on_error(self, status_code):
        if status_code == 420:
            logger.info("Reconnecting the stream, with backoff...")
            return True
