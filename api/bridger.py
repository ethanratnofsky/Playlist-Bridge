from .classes import Playlist, PlaylistCreatorResponse
from .playlist_creators import spotify_creator
from .playlist_parsers import tidal_parser
from flask import abort


def bridge(src: str, dest: str, playlist_url: str) -> PlaylistCreatorResponse:
    playlist = Playlist()
    if src == 'tidal':
        playlist = tidal_parser.parse(playlist_url)
    else:
        print('ERROR: Unknown source service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error

    if dest == 'spotify':
        return spotify_creator.create(playlist)
    else:
        print('ERROR: Unknown destination service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error
