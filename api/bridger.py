def bridge(src, dest, playlist_url):
    if src == 'tidal':
        playlist = tidal_parser(playlist_url)
    # elif src == 'spotify':
    #     playlist = spotify_parser(playlist_url)
    # elif src == 'apple_music':
    #     playlist = apple_music_parser(playlist_url)
    #
    # if dest == 'spotify':
    #     print(spotify_creator(playlist))
    # elif dest == 'apple_music':
    #     print(apple_music_creator(playlist))
