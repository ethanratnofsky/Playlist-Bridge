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

    def __init__(self):
        self.name = ""
        self.artist = ""
        self.album = ""
        self.isrc = ""
