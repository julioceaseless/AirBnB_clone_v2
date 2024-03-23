#!/usr/bin/python3
""" script starts a Flask web app """
from flask import Flask
from markupsafe import escape


# initialize flask
app = Flask(__name__)


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


@app.route("/c/<custom_text>", strict_slashes=False)
def custom(custom_text):
    """ displays a custom text on url /c/<text> """
    new_text = escape(custom_text.replace("_", " "))
    return f"C {new_text}"


if __name__ == "__main__":
    """ run only when called directly"""
    app.run(host="0.0.0.0", port=5000)
