from data import Data

class Feeds(object):

    @staticmethod
    def all_feeds():
        return Data.load("subscribed_feeds")

    @staticmethod
    def get(feed_id):
        return Feeds.all_feeds()[feed_id]
