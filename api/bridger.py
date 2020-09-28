from .classes import Playlist, PlaylistCreatorResponse
from .playlist_creators import spotify_creator
from .playlist_parsers import tidal_parser
from flask import abort, session


def bridge(src: str, dest: str, playlist_url: str) -> PlaylistCreatorResponse:
    playlist = Playlist()

    # Parse playlist from source service
    if src == 'tidal':
        playlist = tidal_parser.parse(playlist_url)
    else:
        print('ERROR: Unknown source service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error

    # Return playlist created with destination service
    if dest == 'spotify':
        access_token = session.get('spotify_tokens').get('access_token')
        return spotify_creator.create(playlist, access_token)
    else:
        print('ERROR: Unknown destination service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error
