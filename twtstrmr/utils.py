from pymongo.errors import DuplicateKeyError
from twtstrmr.logger import get_logger

logger = get_logger('twtstrmr.utils')


def save_status_to_db(status=None, collection=None):
    """Save status object to collection.

    Keyword Arguments:
        status {dict} -- JSON representation of a Status object
        (default: {None})
        collection {pymongo.collection.Collection} -- A Mongo collection.
        (default: {None})
    """
    id_ = {"_id": status['id_str']}
    new_document = {**id_, **status}
    try:
        collection.insert_one(new_document)
    except DuplicateKeyError:
        logger.error(f"Found duplicate key @{status['id_str']}")
        raise


def update_status_in_db(status=None, collection=None):
    status_query = {'_id': status['id_str']}
    new_values = {"$set": {"id_str": status['id_str']}}
    collection.update_one(status_query, new_values)


def read_keywords_file(filename):
    """ reads keywords from text file and return a list of keywords """
    keywords = []

    with open(filename) as f:
        for line in f:
            keywords.append(line.strip('\n').lower())

    return set(keywords)
