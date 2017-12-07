from models.feeds import Feeds
from components.article_downloader import ArticleDownloader
from multiprocessing import Pool

class FeedRefresher(object):

    def __init__(self, workers=8):
        self.workers = workers

    def fetch_feed(self, params):
        url, feed_id = params
        article_id = ArticleDownloader(url, feed_id).fetch()

    def fetch(self):
        feeds = [(feed['url'], feed['id']) for feed in Feeds.all_feeds().values()]
        with Pool(self.workers) as pool:
            pool.map(self.fetch_feed, feeds)
