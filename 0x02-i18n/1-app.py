#!/usr/bin/env python3
"""Basic Flask app for displaying 'Hello world' with Babel integration."""

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration for Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def index():
    """Route for the home page."""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
