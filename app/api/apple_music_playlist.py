from . import Song


class AppleMusicPlaylist:
    def __init__(self, url):
        self.playlist_url = url
        self.storefront = self.get_storefront()
        self.playlist_id = self.get_playlist_id()
        self.playlist = {
            "title": self.get_playlist_title(),
            "description": self.get_playlist_desc(),
            "curator": self.get_playlist_curator(),
            "date": self.get_playlist_date(),
            "songs": self.get_playlist_songs()
        }

    def get_storefront(self):
        url = self.playlist_url
        return url[url.find("apple.com/") + 10:url.find("/playlist")]

    def get_playlist_id(self):
        url = self.playlist_url
        return url[url.rfind("/") + 1:]
