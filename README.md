# Perfect Transition

Perfect Transition is a program that allows for reordering playlists by factors of danceability, energy level, valence, and acousticness. The program then reorders again based on each song's key to create a seamless transition throughout a playlist.

## Installation
```bash
pip install spotipy
```
or upgrade
```bash
pip install spotipy --upgrade
```

## Quick Start

A full set of examples can be found in the [online documentation](https://spotipy.readthedocs.io/en/2.12.0/) and in the [Spotipy examples directory](https://github.com/plamere/spotipy/tree/master/examples). 

To get started, install spotipy and create an app on https://developer.spotify.com/dashboard/login. Add a redirect URI to the app and add your new CLIENT_ID, CLIENT_SECRET, REDIRECT_URI to your environment:

**With user authentication**
```bash
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = 'CLIENT_ID', 
    client_secret = 'CLIENT_SECRET', 
    redirect_uri = 'REDIRECT_URI',
    username = 'USER_ID'))
```
