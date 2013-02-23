# Copyright (c) Paul Tagliamonte <tag@pault.ag>, 2013

from flask import Flask, render_template
from legwords.core import db
from legwords.photos import create_photo_url
import random


app = Flask(__name__)


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
        "photo": create_photo_url(leg['_id'])
    })


if __name__ == '__main__':
    app.run(debug=True)
