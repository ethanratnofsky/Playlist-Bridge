import datetime

import requests
# TODO: why are these imports underlined in red?
from playlist import Playlist
from song import Song


class AppleMusicPlaylistParser:
    """
    A class used to parse a playlist URL from Apple Music

    Attributes
    ----------
    playlist_url : str
        The Apple Music Playlist URL
    storefront : str
        The Apple Music Storefront for the playlist
    playlist_id : str
        The Apple Music Playlist ID for the playlist
    raw_playlist : dict
        Decoded JSON directly from API response that represents the playlist
    parsed_playlist : Playlist
        Parsed playlist from raw_playlist

    Methods
    -------
    get_storefront()
        Parses the playlist URL to determine the storefront
    get_playlist_id()
        Parses the playlist URL to determine the playlist ID
    get_raw_playlist()
        Accesses API endpoint to retrieve and decode Playlist JSON response
    parse_playlist()
        Parses raw playlist dict from API response
    """

    def __init__(self, url):
        """
        Parameters
        ----------
        url : str
            The Apple Music Playlist URL
        """
        self.playlist_url = url
        self.storefront = self.get_storefront()
        self.playlist_id = self.get_playlist_id()
        self.raw_playlist = self.get_raw_playlist()
        self.parsed_playlist = self.parse_playlist()

    def get_storefront(self):
        """Parses the playlist URL to determine the storefront.

        The storefront is necessary for accessing Apple Music's API endpoint.

        Returns
        -------
        storefront : str
            A two-character string that represents the storefront
        """

        url = self.playlist_url
        return url[url.find("apple.com/") + 10:url.find("/playlist")]

    def get_playlist_id(self):
        """Parses the playlist URL to determine the playlist ID.

        The playlist ID is necessary for accessing Apple Music's API endpoint.

        Returns
        -------
        playlist_id : str
            The playlist ID
        """

        url = self.playlist_url
        return url[url.rfind("/") + 1:]

    def get_raw_playlist(self):
        """Accesses API endpoint to retrieve and decode Playlist JSON response.

        The raw playlist JSON response is necessary for parsing.

        Returns
        -------
        raw_playlist : dict
            A dict that represents the raw Playlist object
        """

        # TODO: need necessary authentication to access Apple Music API
        # TODO: load endpoint from env/config/settings file?
        response = requests.get(
            f"https://api.music.apple.com/v1/catalog/{self.storefront}/playlists/{self.playlist_id}")
        return response.json()

    def parse_playlist(self):
        """Parses raw playlist dict from API response.

        Parsing the raw playlist to a standard object allows for easier access to necessary attributes.

        Returns
        -------
        parsed_playlist : Playlist
            A Playlist object that represents the parsed playlist
        """

        raw_playlist = self.raw_playlist

        parsed_playlist = Playlist()
        parsed_playlist.title = raw_playlist["data"][0]["attributes"]["name"]
        parsed_playlist.description = raw_playlist["data"][0]["attributes"]["description"]["standard"]
        parsed_playlist.curator = raw_playlist["data"][0]["attributes"]["curatorName"]
        parsed_playlist.date_modified = datetime.date.fromisoformat(
            raw_playlist["data"][0]["attributes"]["lastModifiedDate"][:10])

        raw_song_list = raw_playlist["data"][0]["relationships"]["tracks"]["data"]
        for raw_song in raw_song_list:
            song = Song()
            song.name = raw_song["attributes"]["name"]
            song.artist = raw_song["attributes"]["artistName"]
            # TODO: define song.album
            song.isrc = raw_song["attributes"]["isrc"]

            parsed_playlist.songs.append(song)

        return parsed_playlist
