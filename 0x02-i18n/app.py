#!/usr/bin/env python3
"""Flask app with user login emulation, localization, and timezone support."""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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
    """Determine the best match with our supported languages based on priority."""
    # 1. Check if locale is provided in URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Check if the user has a preferred locale
    user = getattr(g, 'user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    # 3. Check the locale from the request header
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    if best_match:
        return best_match

    # 4. Fallback to the default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Determine the correct timezone based on priority."""
    # 1. Check if timezone is provided in URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass

    # 2. Check if the user has a preferred timezone
    user = getattr(g, 'user', None)
    if user and user['timezone']:
        try:
            return pytz.timezone(user['timezone']).zone
        except UnknownTimeZoneError:
            pass

    # 3. Fallback to the default timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user():
    """Retrieve user from URL parameter."""
    user_id = request.args.get('login_as', type=int)
    return users.get(user_id, None)


@app.before_request
def before_request():
    """Set user as global variable if logged in."""
    g.user = get_user()


@app.route('/')
def index():
    """Route for the home page."""
    home_title = _('home_title')
    home_header = _('home_header')

    # Determine the current time based on the inferred timezone
    timezone = get_timezone()
    now = datetime.now(pytz.timezone(timezone))
    formatted_time = now.strftime('%b %d, %Y, %I:%M:%S %p') if home_header == 'Hello world!' else now.strftime('%d %b %Y à %H:%M:%S')

    if g.user:
        welcome_message = _('logged_in_as', username=g.user['name'])
    else:
        welcome_message = _('not_logged_in')

    current_time_message = _('current_time_is', current_time=formatted_time)

    return render_template(
        'index.html',
        home_title=home_title,
        home_header=home_header,
        welcome_message=welcome_message,
        current_time_message=current_time_message
    )


if __name__ == '__main__':
    app.run(debug=True)
