from .playlist_parsers import tidal_parser


def bridge(src: str, dest: str, playlist_url: str):
    if src == 'tidal':
        playlist = tidal_parser.parse(playlist_url)
    #
    # if dest == 'spotify':
    #     print(spotify_creator.create(playlist))
