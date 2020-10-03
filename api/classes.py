class Song:
    def __init__(self):
        self.title = ''
        self.artists = []
        self.isrc = None


class Playlist:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.creator = ''
        self.songs = []
        self.excluded_songs = []


class PlaylistCreatorResponse:
    def __init__(self):
        self.playlist = Playlist()
        self.playlist_url = ''
