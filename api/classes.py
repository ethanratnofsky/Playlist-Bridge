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


class PlaylistCreatorResponse:
    def __init__(self):
        self.playlist = Playlist()
        self.excluded_songs = []
        self.playlist_url = ''
