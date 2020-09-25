from os import getenv

import tidalapi
from ..classes import Song, Playlist

TIDAL_USER = getenv('TIDAL_USER')
TIDAL_PASS = getenv('TIDAL_PASS')


def get_session(username: str, password: str) -> tidalapi.Session:
    session = tidalapi.Session()
    session.login(username, password)

    assert(session.check_login())
    return session


def parse(playlist_url: str) -> Playlist:
    # Start TIDAL session
    session = get_session(TIDAL_USER, TIDAL_PASS)

    # Create instance of Playlist object
    playlist = Playlist()

    # Extract TIDAL playlist ID from URL
    playlist_id = playlist_url[34:]

    # Parse title, description, and creator
    tidal_playlist = session.get_playlist(playlist_id)
    playlist.title = tidal_playlist.name
    playlist.description = tidal_playlist.description
    playlist.creator = tidal_playlist.creator

    # Parse tracks
    tidal_playlist_tracks = session.get_playlist_tracks(playlist_id)
    for track in tidal_playlist_tracks:
        song = Song()
        song.title = track.name
        for artist in track.artists:
            song.artists.append(artist.name)
        # ISRC's are not available via tidalapi
        playlist.songs.append(song)

    return playlist
