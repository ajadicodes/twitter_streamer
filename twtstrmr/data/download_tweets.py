# -*- coding: utf-8 -*-
import os

import click
import pymongo
import requests
import tweepy
from dotenv import find_dotenv, load_dotenv
from tweepy.error import TweepError

from twtstrmr.logger import get_logger
from twtstrmr.twitter import TwitterStreamListener, auth
from twtstrmr.utils import read_keywords_file

logger = get_logger('twtstrmr.data.download_tweets')


@click.command()
@click.argument('keywords_file', type=click.Path(exists=True))
def main(keywords_file):
    """ Download twitter messages in real time using Twitter Streaming API.
    """
    try:
        # prepare credentials for accessing twitter API
        consumer_key = os.environ.get('CONSUMER_KEY')
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

        if (consumer_key is None or consumer_secret is None or
                access_token is None or access_token_secret is None):
            raise EnvironmentError('Missing twitter API credentials.')
        api = auth(consumer_key=consumer_key,
                   consumer_secret=consumer_secret,
                   access_token=access_token,
                   access_token_secret=access_token_secret)

        db_name = os.environ.get('DB_NAME')
        if db_name is None:
            raise EnvironmentError('Database name is missing in evn file.')
        client = pymongo.MongoClient(host='localhost', port=27017,
                                     appname=__file__)
        db = client[db_name]
        filepath = os.path.basename(keywords_file)
        input_filename,  _ = os.path.splitext(filepath)
        collection = db[input_filename]

        twitterStreamListener = TwitterStreamListener(collection=collection)
        twitterStream = tweepy.Stream(auth=api.auth,
                                      listener=twitterStreamListener)

        keywords = read_keywords_file(filename=keywords_file)
        logger.info('Streamer App has started listening for keywords: '
                    f'{", ".join(keywords)}')
        twitterStream.filter(track=keywords, is_async=True)
    except requests.exceptions.HTTPError as e:
        logger.error("Checking internet connection failed, "
                     f"status code {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        logger.error("Could not establish a connection.")
    except (ValueError, TypeError, TweepError, KeyError,
            EnvironmentError) as e:
        logger.error(e)
    except KeyboardInterrupt:
        logger.info('Program interrupted by user. ')


if __name__ == '__main__':
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
