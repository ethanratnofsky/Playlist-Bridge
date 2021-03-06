import json
import re
from os import getenv

import requests
from flask import abort

from ..classes import Playlist, PlaylistCreatorResponse, Song

# Spotify API endpoints
SPOTIFY_PROFILE_URL = getenv('SPOTIFY_PROFILE_URL')
SPOTIFY_USER_PLAYLISTS_URL = getenv('SPOTIFY_USER_PLAYLISTS_URL')
SPOTIFY_SEARCH_URL = getenv('SPOTIFY_SEARCH_URL')
SPOTIFY_ADD_SONGS_URL = getenv('SPOTIFY_ADD_SONGS_URL')


def get_user_id() -> str:
    # GET request header field
    header = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    response = requests.get(SPOTIFY_PROFILE_URL, headers=header)

    # Check for non-success status code
    if response.status_code != 200:
        print('ERROR: Error accessing Spotify user ID.')  # TODO: Log this as an error
        abort(response.status_code)

    return response.json().get('id')


def create_playlist(user_id: str, playlist: Playlist) -> dict:
    # POST request header fields
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    # POST request body parameters
    payload = {
        'name': playlist.name,
        'public': True,
        'collaborative': False,
        'description': playlist.description
    }

    # Create Spotify playlist by making POST request to Spotify API endpoint
    response = requests.post(SPOTIFY_USER_PLAYLISTS_URL.format(user_id=user_id), headers=headers, data=json.dumps(payload))

    # Check for non-success status code
    if response.status_code != 201:
        print('ERROR: Could not create a new Spotify playlist.')  # TODO: Log this as an error
        abort(response.status_code)

    return response.json()


def search_spotify(song: Song) -> dict:
    # Parse song for title and primary artist
    song_title = song.title
    primary_artist = song.artists[0]

    # Remove segment of song title that specifies featured artist(s)
    # This is necessary because the 'featuring' segment can break the search query functionality
    pattern = re.compile(r"\s[(\[]feat\.\s[^])]+[)\]]")
    match = pattern.search(song_title)
    if match:
        song_title = song_title.replace(match.group(), '')

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

    # Check for non-success status code
    if results.status_code != 200:
        print('ERROR: Error searching Spotify for song.')  # TODO: Log this as an error
        abort(results.status_code)

    return results.json()


def add_songs(playlist: Playlist, playlist_id: str) -> PlaylistCreatorResponse:
    uris = []  # List of Spotify URIs for songs in playlist
    excluded_songs = []  # List of songs not found on Spotify

    # Iterate through given songs; search Spotify for their URIs
    for song in playlist.songs:
        search_results = search_spotify(song)
        try:
            uris.append(search_results.get('tracks').get('items')[0].get('uri'))
        except IndexError:
            excluded_songs.append(song)

    playlist_creator_response = PlaylistCreatorResponse()
    playlist_creator_response.playlist = playlist
    playlist_creator_response.excluded_songs = excluded_songs

    # POST request header fields
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    # Make request to Spotify API endpoint to add songs (100 per request limit)
    temp_uris = []  # List to store 100 URIs at a time
    for uri in uris:
        temp_uris.append(uri)

        # Check if songs-per-request limit (100) is reached or end of URIs list is reached
        if (uri is uris[-1]) or (len(temp_uris) == 100):
            # If songs-per-request limit or end of URIs list reached, make request with 100 temp allocated song URIs

            # POST request body parameters
            payload = json.dumps(temp_uris)

            # Clear temp_uris list
            temp_uris.clear()

            # Make request for 100 songs to be added
            response = requests.post(SPOTIFY_ADD_SONGS_URL.format(playlist_id=playlist_id), headers=headers,
                                     data=payload)

            # Check for non-success status code
            if response.status_code != 201:
                print('ERROR: Could not add songs to Spotify playlist.')  # TODO: Log this as an error
                print(response.json().get('error').get('message'))
                abort(response.status_code)

    return playlist_creator_response


def create(src_playlist: Playlist, tokens: dict) -> PlaylistCreatorResponse:
    # Assign global variables for tokens
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = tokens.get('access_token')
    REFRESH_TOKEN = tokens.get('refresh_token')

    # Get Spotify user ID
    user_id = get_user_id()

    # Create new Spotify playlist
    spotify_playlist = create_playlist(user_id, src_playlist)

    # Add songs to new Spotify playlist
    playlist_creator_response = add_songs(src_playlist, spotify_playlist.get('id'))
    playlist_creator_response.playlist_url = spotify_playlist.get('external_urls').get('spotify')

    return playlist_creator_response
