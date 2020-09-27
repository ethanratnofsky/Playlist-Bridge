import secrets
from os import getenv
from urllib.parse import urlencode

from flask import Flask, redirect, render_template, request, session, url_for

# Spotify authentication information
CLIENT_ID = getenv('CLIENT_ID')
REDIRECT_URI = getenv('REDIRECT_URI')
SPOTIFY_AUTH_URL = getenv('SPOTIFY_AUTH_URL')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth-spotify')
def auth_spotify():
    # Generate and remember random URL-safe string to prevent Cross-Site Request Forgery
    state = secrets.token_urlsafe(16)
    session['spotify_auth_state'] = state

    # Define scope for authorization
    scope = 'playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'

    # Query parameters for GET request to Spotify Accounts service
    query_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scope
    }

    # Redirect user to Spotify Accounts service for authorization
    return redirect(f'{SPOTIFY_AUTH_URL}/?{urlencode(query_params)}')


@app.route('/spotify-callback')
def spotify_callback():
    return 'success!'


@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    form = request.form

    if form['dest_service'] == 'spotify':
        return redirect(url_for('auth_spotify'))

    return 'doing things!'


if __name__ == '__main__':
    app.run(debug=True)
