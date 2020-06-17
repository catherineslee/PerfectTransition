from Song import Track
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Playlist(object):
    client_credentials_manager = SpotifyClientCredentials(client_id = '3807740e1a274c5185d6723967a00f5b', 
    client_secret = '8718585c5b1f453689655c20034988ee')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False

    id = ''
    track_ids = []
    tracks = []

    def __init__(self, id, track_ids):
        self.id = id
        self.track_ids = track_ids

    def get_track_ids(self):
        return self.track_ids
    
    def get_playlist_id(self):
        return self.id

    def get_tracks(self):
        return self.tracks
    
    #creates a list of Track objects
    #loops through tracks ids in sets
    #param index of song
    def set_tracks(self, index):
        song_set = []                                   #list of track objects
        for i in range(len(self.track_ids)):            #loops through the tracks
            song = Track(self.track_ids[i])             #creates a Track object with the track id
            song.set_info(index)                        #calls method that retrieves info of song
            song_set.append(song)                       #adds to list
            index += 1
        return song_set



    