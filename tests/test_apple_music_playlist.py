from app.api.apple_music_playlist import AppleMusicPlaylist
from tests.constant_playlist_urls import *

url = AppleMusicPlaylist(APPLE_MUSIC_PLAYLIST_URL_3)

print("Apple Music Playlist URL: " + url.playlist_url)
print("Storefront: " + url.storefront.upper())
print("Apple Music Playlist ID: " + url.playlist_id)

print("\n")

print("Playlist Object: ")
print(url.playlist)
