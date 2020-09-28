from os import getenv

import requests
from flask import session

from ..classes import Playlist, PlaylistCreatorResponse, Song

# Spotify API endpoints
SPOTIFY_PROFILE_URL = getenv('SPOTIFY_PROFILE_URL')
SPOTIFY_USER_PLAYLISTS_URL = getenv('SPOTIFY_USER_PLAYLISTS_URL')
SPOTIFY_SEARCH_URL = getenv('SPOTIFY_SEARCH_URL')

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


def search_spotify(song: Song) -> dict:
    # Parse song for title and primary artist
    song_title = song.title
    primary_artist = song.artists[0]

    # Remove segment of song title that specifies featured artist(s)
    # This is necessary because the 'featuring' segment can break the search query functionality
    # TODO: This may be easier to program with RegEx
    if ' (feat. ' in song_title:
        song_title = song_title[:song_title.find(' (feat. ')] + song_title[song_title.find(')', song_title.find(
            ' (feat. ')) + 1:]
    elif ' [feat. ' in song_title:
        song_title = song_title[:song_title.find(' [feat. ')] + song_title[song_title.find(']', song_title.find(
            ' [feat. ')) + 1:]

    # GET request header field
    header = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    # GET request query parameters
    params = {
        'q': song_title + ' ' + primary_artist,
        'type': 'track',
        'market': 'from_token',
        'limit': 1
    }

    # Search Spotify with for song title and primary artist name with GET request to Spotify API endpoint
    results = requests.get(SPOTIFY_SEARCH_URL, headers=header, params=params)

    return results.json()


def add_songs(songs: list, playlist_id: str):
    uris = []  # List of Spotify URIs for songs in playlist
    songs_not_found = []  # List of songs that are not found on Spotify

    # Iterate through given songs; search Spotify for their URIs
    for song in songs:
        search_results = search_spotify(song)


def create(src_playlist: Playlist) -> PlaylistCreatorResponse:
    # Get Spotify user ID
    user_id = get_user_id()

    # Create new Spotify playlist
    spotify_playlist = create_playlist(user_id, src_playlist)

    # Add songs to new Spotify playlist
    add_songs(src_playlist.songs, spotify_playlist.get('id'))
