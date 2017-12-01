from main import app
from flask import abort
from models.articles import Articles
from components.article_recommender import ArticleRecommender
import json

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
