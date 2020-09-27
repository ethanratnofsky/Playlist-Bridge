import requests
import secrets
from os import getenv
from urllib.parse import urlencode

from flask import abort, Flask, redirect, render_template, request, session, url_for

# Spotify authentication information
SPOTIFY_AUTH_URL = getenv('SPOTIFY_AUTH_URL')
SPOTIFY_TOKEN_URL = getenv('SPOTIFY_TOKEN_URL')
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
REDIRECT_URI = getenv('REDIRECT_URI')

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
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scope
    }

    # Redirect user to Spotify Accounts service for authorization
    return redirect(f'{SPOTIFY_AUTH_URL}/?{urlencode(payload)}')


@app.route('/spotify-callback')
def spotify_callback():
    # Get query parameters
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')

    # Verify state ID
    if state != session['spotify_auth_state']:
        print('ERROR: State ID mismatch.')  # TODO: Log this as an error
        abort(400)  # 400 Bad Request

    # Check for authorization error
    if error == 'access_denied':
        print('ERROR: User denied access.')  # TODO: Log this as an error
        abort(401)  # 401 Unauthorized

    # Request body parameters for POST request to Spotify Accounts service
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    # Make POST request to Spotify Accounts service to get token information
    tokens_response = requests.post(SPOTIFY_TOKEN_URL, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))

    # Check for non-success status code
    if tokens_response.status_code != 200:
        print('ERROR: Failed to get token data.')  # TODO: Log this as an error
        abort(tokens_response.status_code)

    # Parse response
    tokens = tokens_response.json()
    session['spotify_tokens'] = {
        'access_token': tokens.get('access_tokens'),
        'refresh_token': tokens.get('refresh_token')  # Do I need this?
    }

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
