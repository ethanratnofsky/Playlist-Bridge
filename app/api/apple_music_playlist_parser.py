import requests


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
    api_endpoint : str
        The Apple Music API endpoint for the playlist

    Methods
    -------
    get_storefront()
        Parses the playlist URL to determine the storefront
    get_playlist_id()
        Parses the playlist URL to determine the playlist ID
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
        self.api_endpoint = "https://api.music.apple.com/v1/catalog/{storefront}/playlists/{id}"\
            .format(storefront=self.storefront, id=self.playlist_id)
        # self.playlist = {
        #     "title": self.get_playlist_title(),
        #     "description": self.get_playlist_desc(),
        #     "curator": self.get_playlist_curator(),
        #     "date": self.get_playlist_date(),
        #     "songs": self.get_playlist_songs()
        # }

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
