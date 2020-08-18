class Song:
    """
    A class used to represent a Song

    ...

    Attributes
    ----------
    name : str
        The name of the song
    artist : str
        The artist of the song
    album : str
        The album in which the song is included
    isrc : str
        The Internation Standard Recording Code (ISRC) for the song
    """

    def __init(self, name, artist, album, isrc):
        """
        Parameters
        ----------
        name : str
            The name of the song
        artist : str
            The artist of the song
        album : str
            The album in which the song is included
        isrc : str
            The Internation Standard Recording Code (ISRC) for the song
        """
        self.name = name
        self.artist = artist
        self.album = album
        self.isrc = isrc
