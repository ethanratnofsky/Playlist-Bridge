# Playlist Bridge
Playlist Bridge is a web application built to convert music playlists from one streaming service to another.

[[index.html]](/templates/index.html)
![Screenshot of Playlist Bridge homepage](/screenshots/playlist-bridge_index.png)

# Inspiration
This web application was inspired by the idea of sharing music playlists made on one streaming service with users of a different streaming service. Specifically, I wanted to share my TIDAL playlists with a friend who used Apple Music. However, neither did my friend have a TIDAL subscription nor did I have an Apple Music Subscription. So, to play each other's playlists we would either have to share our respective login creditials with each other or re-create the playlist song by song on our respective music streaming service (both of which are less than ideal). Futhermore, given my recent aquisition of beginner web development skills from a summer internship, I decided to start developing a web application that would handle bridging the gap between music streaming services. Enter Playlist Bridge.

# Usage
The production version of the web application is current live at https://playlistbridge.herokuapp.com!

# Languages and Libraries
* Python
  * [Flask](https://flask.palletsprojects.com/en/1.1.x/) micro web framework
  * ...all Python dependencies can be found in [requirements.txt](/requirements.txt).
* HTML
  * [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) (from Flask)
* CSS
* JavaScript
  * [jQuery](https://jquery.com/) (from Flask)

# Supported Music Streaming Services
**Source Services:**
* TIDAL (via [tidalapi](https://github.com/tamland/python-tidal))
* (Spotify coming soon via [Spotify Web API](https://developer.spotify.com/documentation/web-api/))

**Destination Serices:**
* Spotify (via [Spotify Web API](https://developer.spotify.com/documentation/web-api/))
* (Apple Music coming soon via [Apple Music API](https://developer.apple.com/documentation/applemusicapi/))

# Roadmap
Check the [projects](https://github.com/ethanratnofsky/Playlist-Bridge/projects) tab of this GitHub repository to preview my future plans and progress for this project!

# Authors and Acknowledgement
I, Ethan Ratnofsky, am the sole contributor to this project! I'd also like to acknowledge Kyle Quinn as being an amazing web development mentor during my summer/fall internship!
