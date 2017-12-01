from main import app
from flask import abort
from models.articles import Articles
import json

@app.route("/articles/<feed_id>/<article_id>")
def articles_show(feed_id, article_id):
    article = Articles.get(feed_id, article_id)
    if article is None:
        abort(404)
    else:
        return json.dumps(article)
