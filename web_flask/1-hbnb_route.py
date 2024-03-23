#!/usr/bin/python3
""" script starts a Flask web app """
from flask import Flask


# initialize flask
app = Flask(__name__)

# define route for app's home dir
@app.route("/", strict_slashes=False)
def hbnb():
    """
    This is the content that gets dsiplayed
    when user visits home
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_dir():
    """ hbnb dir """
    return "HBNB"


if __name__ == "__main__":
    """ run only when called directly"""
    app.run(host="0.0.0.0", port=5000)
