import secrets
from os import getenv
from urllib.parse import urlencode

import requests
from flask import abort, Flask, redirect, render_template, request, session, url_for

from api import bridger

# Spotify API endpoints
SPOTIFY_AUTH_URL = getenv('SPOTIFY_AUTH_URL')
SPOTIFY_TOKEN_URL = getenv('SPOTIFY_TOKEN_URL')

# Spotify client information
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
REDIRECT_URI = getenv('REDIRECT_URI')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.jinja_options = {
    'trim_blocks': True,
    'lstrip_blocks': True
}


@app.route('/')
def index():
    # Clear current session data and get new session id
    session.clear()
    session['id'] = secrets.token_urlsafe(16)

    return render_template('index.html')


@app.route('/auth-spotify')
def auth_spotify():
    # Get query parameters
    session_id = request.args.get('session_id')

    # Verify session ID
    if session_id != session.get('id'):
        print('ERROR: Session ID mismatch.')  # TODO: Log this as an error
        abort(400)  # 400 Bad Request

    # Generate and remember random URL-safe string to prevent Cross-Site Request Forgery
    state = secrets.token_urlsafe(16)
    session['spotify_auth_state'] = state

    # Define scope for authorization
    scope = 'user-read-private ' \
            'playlist-modify-public '

    # GET request query parameters
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scope,
        'show_dialog': 'true',
    }

    # Redirect user to Spotify Accounts service for authorization
    return redirect(f'{SPOTIFY_AUTH_URL}/?{urlencode(params)}')


@app.route('/spotify-callback')
def spotify_callback():
    # Get query parameters
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')

    # Verify state ID
    if state != session.get('spotify_auth_state'):
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

    # Save tokens to session
    session['spotify_tokens'] = tokens_response.json()

    return redirect(url_for('bridge', session_id=session.get('id')))


@app.route('/bridge')
def bridge():
    # Verify session ID
    session_id = request.args.get('session_id')
    if session_id != session.get('id'):
        print('ERROR: Session ID mismatch.')  # TODO: Log this as an error
        abort(400)  # 400 Bad Request

    # Get form data
    src_service = session.get('form_data').get('src_service')
    dest_service = session.get('form_data').get('dest_service')
    playlist_url = session.get('form_data').get('playlist_url')

    # Bridge!
    playlist_creator_response = bridger.bridge(src_service, dest_service, playlist_url)

    return render_template('summary.html',
                           playlist=playlist_creator_response.playlist,
                           playlist_url=playlist_creator_response.playlist_url)


@app.route('/submit', methods=['POST'])
def submit():
    # Save form data to session
    session['form_data'] = request.form

    if session.get('form_data').get('dest_service') == 'Spotify':
        # If destination service is Spotify, we need authorization
        return redirect(url_for('auth_spotify', session_id=session.get('id')))
    else:
        return redirect(url_for('bridge', session_id=session.get('id')))


@app.route('/development')
def development():
    from api.classes import Playlist, PlaylistCreatorResponse, Song

    playlist_creator_response = PlaylistCreatorResponse()
    playlist_creator_response.playlist_url = 'https://google.com'

    song1 = Song()
    song1.title = 'Song1'
    song1.artists = ['Artist1']
    song2 = Song()
    song2.title = 'Song2'
    song2.artists = ['Artist1', 'Artist2']
    song3 = Song()
    song3.title = 'Song3'
    song3.artists = ['Artist1', 'Artist2', 'Artist3']

    songs = [song1, song2, song3]

    playlist = Playlist()
    playlist.name = 'Playlist Title'
    playlist.description = 'Test playlist.'
    playlist.creator = 'Developer'
    playlist.songs = songs * 3

    playlist_creator_response.playlist = playlist

    return render_template('summary.html',
                           playlist=playlist_creator_response.playlist,
                           excluded_songs=songs,
                           playlist_url=playlist_creator_response.playlist_url)
