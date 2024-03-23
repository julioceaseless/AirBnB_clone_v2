#!/usr/bin/python3
""" script starts a Flask web app """
from flask import Flask
from markupsafe import escape
from flask import render_template


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


@app.route("/python/<custom_text>", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
def custom_url(custom_text="is_cool"):
    """ displays a custom text on url /python/<url> with default value """
    new_text = escape(custom_text.replace("_", " "))
    return f"Python {new_text}"


@app.route("/number/<int:n>", strict_slashes=False)
def num_path(n):
    """ displays text only if number is passed on the url"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def num_html(n):
    """ displays number passed in url in html body"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def odd_or_even(n):
    """ checks if number is even or odd"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    """ run only when called directly"""
    app.run(host="0.0.0.0", port=5000)
