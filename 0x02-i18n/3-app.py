#!/usr/bin/env python3
"""Basic Flask app for displaying 'Hello world' with Babel integration."""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


class Config:
    """Configuration for Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve user based on the login_as URL parameter."""
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set user on Flask global object before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match with our supported languages."""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the correct timezone."""
    timezone = request.args.get('timezone')
    if g.user and g.user.get('timezone'):
        timezone = g.user.get('timezone')
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

    # Determine current time
    user_timezone = pytz.timezone(get_timezone())
    current_time = datetime.now(user_timezone).strftime('%b %d, %Y, %I:%M:%S %p')

    if g.user:
        welcome_message = _('logged_in_as', username=g.user['name'])
    else:
        welcome_message = _('not_logged_in')

    current_time_message = _('current_time_is', current_time=current_time)

    return render_template(
        '3-index.html',
        home_title=home_title,
        home_header=home_header,
        welcome_message=welcome_message,
        current_time_message=current_time_message
    )


if __name__ == '__main__':
    app.run(debug=True)
