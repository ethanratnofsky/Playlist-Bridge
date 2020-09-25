from .playlist_parsers import tidal_parser


def bridge(src, dest, playlist_url):
    if src == 'tidal':
        playlist = tidal_parser.parse(playlist_url)
    # elif src == 'spotify':
    #     playlist = spotify_parser.parse(playlist_url)
    # elif src == 'apple_music':
    #     playlist = apple_music_parser.parse(playlist_url)
    #
    # if dest == 'spotify':
    #     print(spotify_creator.create(playlist))
    # elif dest == 'apple_music':
    #     print(apple_music_creator.create(playlist))
