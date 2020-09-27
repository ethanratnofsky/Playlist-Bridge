class Song:
    def __init__(self):
        self.title = ''
        self.artists = []
        self.isrc = None


class Playlist:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.creator = ''
        self.songs = []


class PlaylistCreatorResponse:
    def __init__(self):
        self.songs_added = []
        self.songs_not_added = []
        self.playlist_url = ''
