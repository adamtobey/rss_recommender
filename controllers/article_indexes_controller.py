from main import app
import json
from models.articles import Articles
from flask import abort

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
