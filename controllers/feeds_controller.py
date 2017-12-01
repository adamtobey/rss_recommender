from main import app
from models.feeds import Feeds
from flask import abort, request
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

@app.route("/feeds/create", methods=["POST"])
def add_feed():
    feed = request.form
    feed_id = Feeds.create_feed(feed)
    if feed_id is None:
        abort(400)
    else:
        return json.dumps({
            'feed_id': feed_id
        }), 201
