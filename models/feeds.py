from data import Data

FEED_FIELDS = []

class Feeds(object):

    @staticmethod
    def create_feed(feed_info):
        feeds = Feeds.all_feeds()
        next_id = str(max([int(id) for id in feeds.keys()]) + 1)
        try:
            feed = {
                "title": feed_info["title"],
                "description": feed_info["description"],
                "url": feed_info["url"]
            }
            feeds[next_id] = feed
            Data.save(feeds, "subscribed_feeds")
            return next_id
        except:
            return None

    @staticmethod
    def all_feeds():
        return Data.load("subscribed_feeds")

    @staticmethod
    def get(feed_id):
        return Feeds.all_feeds()[feed_id]
