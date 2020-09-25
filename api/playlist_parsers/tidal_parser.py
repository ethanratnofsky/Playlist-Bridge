from os import getenv

import tidalapi
from ..classes import Song, Playlist

TIDAL_USER = getenv('TIDAL_USER')
TIDAL_PASS = getenv('TIDAL_PASS')


def get_session(username, password):
    session = tidalapi.Session()
    session.login(username, password)

    assert(session.check_login())
    return session


def parse(playlist_url: str):
    session = get_session(TIDAL_USER, TIDAL_PASS)
