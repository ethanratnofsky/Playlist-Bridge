import datetime


class Playlist:
    """
    A class used to represent a Playlist

    ...

    Attributes
    ----------
    title : str
        The title of the playlist
    description : str
        The description of the playlist
    curator : str
        The curator of the playlist
    date_modified : date
        The date that the playlist was last modified
    songs: List(Song)
        A list of the songs in the playlist
    """

    def __init__(self):
        self.title = ""
        self.description = ""
        self.curator = ""
        self.date_modified = datetime.date.today()
        self.songs = []
