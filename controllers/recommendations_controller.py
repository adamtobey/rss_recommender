from main import app
from flask import abort
from models.articles import Articles
from components.article_recommender import ArticleRecommender
from config import Config
import json

@app.route("/recommendations/by_article/<feed_id>/<article_id>")
def by_article(feed_id, article_id):
    article = Articles.get(feed_id, article_id)
    articles = Articles.articles_for_feed(feed_id)
    rank = ArticleRecommender(article['classification'], articles)
    return json.dumps(rank.recommend(10, exclude_ids=[article_id]))

@app.route("/recommendations/for_user")
def for_user():
    user_affinity = Config.user_affinity
    articles = Articles.all_articles()
    rank = ArticleRecommender(user_affinity, articles)
    return json.dumps(rank.recommend(10))
