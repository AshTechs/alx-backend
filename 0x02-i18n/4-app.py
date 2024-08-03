#!/usr/bin/env python3
"""
Basic Flask app for displaying 'Hello world' with Babel integration.

This module sets up a Flask application with Babel for language and timezone
support. The app has a single route that displays a localized 'Hello world'
message. It also includes functions to determine the appropriate locale and
timezone based on the request.

Classes:
    Config: Configuration class for Babel.

Functions:
    get_locale: Determines the best match with the supported languages.
    get_timezone: Determines the correct timezone based on the request.
    index: Route for the home page.

Usage:
    Run this module to start the Flask application.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """
    Configuration for Babel.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Determine the best match with our supported languages.

    This function checks the 'locale' parameter in the URL. If it's present and
    valid, it returns that locale. Otherwise, it uses the best match from the
    'Accept-Language' header in the request.

    Returns:
        str: The best matching locale.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Determine the correct timezone based on the request.

    This function checks the 'timezone' parameter in the URL. If it's present and
    valid, it returns that timezone. Otherwise, it defaults to the configured
    default timezone.

    Returns:
        str: The determined timezone.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """
    Route for the home page.

    This function handles the root URL ('/') and renders the '4-index.html'
    template with localized strings for the title and header.

    Returns:
        Response: The Flask response object with the rendered template.
    """
    home_title = _('home_title')
    home_header = _('home_header')
    return render_template(
        '4-index.html',
        home_title=home_title,
        home_header=home_header
    )


if __name__ == '__main__':
    app.run(debug=True)
