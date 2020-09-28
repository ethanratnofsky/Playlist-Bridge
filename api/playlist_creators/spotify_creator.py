from os import getenv

import requests
from flask import session

from ..classes import Playlist, PlaylistCreatorResponse

# Spotify API endpoints
SPOTIFY_PROFILE_URL = getenv('SPOTIFY_PROFILE_URL')
SPOTIFY_USER_PLAYLISTS_URL = getenv('SPOTIFY_USER_PLAYLISTS_URL')

# Spotify access token
ACCESS_TOKEN = session.get('spotify_tokens').get('access_token')


def get_user_id() -> str:
    # GET request header field
    header = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    return requests.get(SPOTIFY_PROFILE_URL, headers=header).json().get('id')


def create_playlist(user_id: str, playlist: Playlist) -> dict:
    # POST request header fields
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    # POST request body parameters
    payload = {
        'name': playlist.title,
        'public': True,
        'collaborative': False,
        'description': playlist.description
    }

    # Create Spotify playlist by making POST request to Spotify API endpoint
    response = requests.post(SPOTIFY_USER_PLAYLISTS_URL.format(user_id=user_id), headers=headers, data=payload)

    return response.json()


def create(playlist: Playlist) -> PlaylistCreatorResponse:
    # Get Spotify user ID
    user_id = get_user_id()

    # Create new Spotify playlist
    spotify_playlist = create_playlist(user_id, playlist)
