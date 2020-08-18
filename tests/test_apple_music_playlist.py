from app.api.apple_music_playlist_parser import AppleMusicPlaylistParser
from tests.constant_playlist_urls import *

url = AppleMusicPlaylistParser(APPLE_MUSIC_PLAYLIST_URL_1)

print("Apple Music Playlist URL: " + url.playlist_url)
print("Storefront: " + url.storefront.upper())
print("Apple Music Playlist ID: " + url.playlist_id)
