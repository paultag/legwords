# Copyright (c) Paul Tagliamonte <tag@pault.ag>, 2013

from flask import Flask, render_template, request, redirect
from legwords import WORDS
from legwords.core import db
from legwords.photos import create_photo_url
import random


app = Flask(__name__)


@app.template_filter("photo_url")
def photo_url(leg):
    return create_photo_url(leg['_id'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rate")
def rate():
    legs = db.legislators.find()
    offset = random.randint(0, legs.count())
    leg = legs[offset]
    return render_template("rate.html", **{
        "legislator": leg,
        "photo": create_photo_url(leg['_id']),
        "words": WORDS,
    })


@app.route("/report", methods=["POST"])
def report():
    form = request.form
    reaction = form['reaction']
    legislator = form['legid']
    leg = db.legislators.find_one({"_id": legislator})
    if leg is None:
        return redirect("/rate")
    if reaction in leg['words']:
        leg['words'][reaction] += 1
    else:
        leg['words'][reaction] = 1
    db.legislators.save(leg, safe=True)
    return redirect("/rate")


@app.route("/leaderboard")
def leaderboard():
    env = {
        "words": WORDS,
        "results": {}
    }
    for word in WORDS:
        env['results'][word] = db.legislators.find().sort(
            "words.%s" % (word), -1)[:5]

    return render_template("leaderboard.html", **env)


if __name__ == '__main__':
    app.run(debug=True)
