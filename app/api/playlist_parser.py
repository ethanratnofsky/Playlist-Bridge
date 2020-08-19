# TODO: why are these imports underlined red?
from spotify_playlist_parser import SpotifyPlaylistParser  # TODO: create SpotifyPlaylistParser
from apple_music_playlist_parser import AppleMusicPlaylistParser
from tidal_playlist_parser import TidalPlaylistParser  # TODO: create TidalPlaylistParser


class PlaylistParser:
    def __init__(self, url):
        self.url = url

    def parse(self):
        url = self.url
        if url.startswith("http://open.spotify.com/"):
            return SpotifyPlaylistParser(url).playlist
        elif url.startswith("https://music.apple.com/"):
            return AppleMusicPlaylistParser(url).playlist
        elif url.startswith("http://tidal.com/"):
            return TidalPlaylistParser(url).playlist
