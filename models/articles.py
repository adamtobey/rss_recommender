from main import app
from data import Data

class Articles(object):

    @staticmethod
    def all_articles():
        try:
            return Data.load("articles", "1")["articles"]
        except FileNotFoundError:
            return None

    @staticmethod
    def articles_for_feed(feed_id):
        try:
            return Data.load("articles", feed_id)["articles"]
        except FileNotFoundError:
            return None

    @staticmethod
    def get(feed_id, article_id):
        articles = Articles.articles_for_feed(feed_id)
        if articles is None:
            return None
        else:
            if article_id in articles:
                return articles[article_id]
            else:
                return None
