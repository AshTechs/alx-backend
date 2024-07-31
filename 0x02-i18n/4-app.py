#!/usr/bin/env python3
"""Basic Flask app for displaying 'Hello world' with Babel integration."""

from flask import Flask, render_template, request
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """Configuration for Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match with our supported languages."""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the correct timezone."""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Route for the home page."""
    home_title = _('home_title')
    home_header = _('home_header')
    return render_template(
            '4-index.html',
            home_title=home_title,
            home_header=home_header
    )


if __name__ == '__main__':
    app.run(debug=True)
