from main import app
from models.feeds import Feeds
from flask import abort
import json

@app.route('/feeds')
def feeds_index():
    return json.dumps({
        'feeds': Feeds.all_feeds()
    })

@app.route("/feeds/<feed_id>")
def feeds_show(feed_id):
    if feed_id is None:
        abort(404)
    else:
        feed = Feeds.get(feed_id)
        return json.dumps({
            'feed_id': feed_id,
            'feed_title': feed['title'],
            'feed_description': feed['description']
        })
