from flask import Flask, request, abort
import os
import pathlib
import json
app = Flask(__name__)

# DATA

DATA_DIR = "data"

class Data(object):
    @staticmethod
    def load(*names):
        *dirs, name = names
        with open(os.path.join(DATA_DIR, *dirs, "{}.json".format(name))) as inf:
            return json.load(inf)

    @staticmethod
    def save(data, *names):
        *dirs, name = names
        path = os.path.join(DATA_DIR, *dirs, "{}.json".format(name))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as outf:
            json.dump(data, outf)

# ARTICLES MODEL

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

# ARTICLES CONTROLLER

@app.route("/articles/<feed_id>/<article_id>")
def articles_show(feed_id, article_id):
    article = Articles.get(feed_id, article_id)
    if article is None:
        abort(404)
    else:
        return json.dumps(article)

@app.route("/articles/<feed_id>/<article_id>/recommendations")
def articles_recommendations(feed_id, article_id):
    article = Articles.get(feed_id, article_id)
    articles = Articles.articles_for_feed(feed_id)
    rank = ArticleRecommender(article, articles)
    return json.dumps(rank.recommend(10))

# ARTICLE RECOMMENDER

import numpy as np

class ArticleRecommender(object):

    def __init__(self, base_article, other_articles):
        self.base_article = base_article
        self.base_id = base_article["id"]
        self.base_norm = np.array(base_article["classification"])
        self.base_norm = self.base_norm / np.linalg.norm(self.base_norm)
        self.other_articles = other_articles

    def recommend(self, limit):
        ranked = [
            (self.similarity(article), article_id)
            for article_id, article in self.other_articles.items()
            if article_id != self.base_id
        ]
        return [
            pair[1]
            for pair in reversed(sorted(ranked))
        ][:10] #TODO inefficient

    def similarity(self, article):
        comp = np.array(article["classification"])
        comp = comp / np.linalg.norm(comp)
        return self.base_norm.dot(comp)

# ARTICLE INDEX CONTROLLER

@app.route("/articles_index/<feed_id>")
def articles_index_show(feed_id):
    if feed_id is None:
        abort(404)
    else:
        articles = Articles.articles_for_feed(feed_id)
        if articles is None:
            abort(404)
        return json.dumps({
            "articles": articles
        })

# FEEDS MODEL

class Feeds(object):

    @staticmethod
    def all_feeds():
        return Data.load("subscribed_feeds")

    @staticmethod
    def get(feed_id):
        return Feeds.all_feeds()[feed_id]

# FEEDS CONTROLLER

@app.route('/feeds')
def feeds_index():
    return json.dumps({
        'feeds': Feeds.all_feeds()
    })

@app.route("/feeds/<feed_id>")
def feeds_show(feed_id):
    # feed_id = request.args.get('feed_id', None)
    if feed_id is None:
        abort(404)
    else:
        feed = Feeds.get(feed_id)
        return json.dumps({
            'feed_id': feed_id,
            'feed_title': feed['title'],
            'feed_description': feed['description']
        })
