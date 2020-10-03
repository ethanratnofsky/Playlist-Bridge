from flask import abort, session

from .classes import Playlist, PlaylistCreatorResponse
from .playlist_creators import spotify_creator
from .playlist_parsers import tidal_parser


def bridge(src: str, dest: str, playlist_url: str) -> PlaylistCreatorResponse:
    playlist = Playlist()

    # Parse playlist from source service
    if src == 'TIDAL':
        playlist = tidal_parser.parse(playlist_url)
        playlist.src_service = src
    else:
        print('ERROR: Unknown source service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error

    # Return playlist created with destination service
    if dest == 'Spotify':
        playlist.dest_service = dest
        return spotify_creator.create(playlist, session.get('spotify_tokens'))
    else:
        print('ERROR: Unknown destination service.')  # TODO: Log this as an error
        abort(500)  # 500 Internal Server Error
