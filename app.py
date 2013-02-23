# Copyright (c) Paul Tagliamonte <tag@pault.ag>, 2013

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
