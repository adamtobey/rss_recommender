from main import app
from data import Data

class Articles(object):

    @staticmethod
    def articles_for_feed(feed_id):
        try:
            return Data.load("articles", feed_id)["articles"]
        except FileNotFoundError:
            return None

    def get(feed_id, article_id):
        articles = Articles.articles_for_feed(feed_id)
        if articles is None:
            return None
        else:
            if article_id in articles:
                return articles[article_id]
            else:
                return None
