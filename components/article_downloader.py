from goose3 import Goose
import feedparser
from data import Data
from hashlib import md5
from models.feeds import Feeds
from components.article_classifier import ArticleClassifier

# TODO want some logging/error handling since a single article error fails the whole process
class ArticleDownloader(object):

    def __init__(self, url, feed_id):
        self.goose = Goose({'enable_image_fetching':False})
        self.url = url
        self.feed_id = feed_id
        # TODO race condition overwrites modification but will fix with SQL database
        self.feed_articles = Feeds.get(self.feed_id)
        if self.feed_articles is None:
            self.feed_articles = {}

    def uid(self, article):
        if 'guid' in article.__dict__:
            id = article.guid
        else:
            id = article.link
        return md5(bytes(id, 'UTF-8')).hexdigest()

    def parse(self, url, uid, title, article):
        # TODO classifier version identifier could be helpful
        return {
            "id": uid,
            "title": title,
            "url": url,
            "classification": ArticleClassifier(article.title, article.cleaned_text).classify()
        }

    def fetch_article(self, url, uid, title):
        article = self.goose.extract(url=self.url)
        # TODO will never re-classify articles
        if uid not in self.feed_articles:
            self.feed_articles[uid] = self.parse(url, uid, title, article)

    def fetch(self):
        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            # TODO filter based on update time to avoid refetching too much
            self.fetch_article(entry.link, self.uid(entry), entry.title)
        self.persist()

    def persist(self):
        Data.save(self.feed_articles, "articles", self.feed_id)
