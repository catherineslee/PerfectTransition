from math import trunc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Track(object):
    client_credentials_manager = SpotifyClientCredentials(client_id = 'CLIENT_ID', 
    client_secret = 'CLIENT_SECRET')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    
    id = ''
    playlist_id = ''
    energy = 0.0
    valence = 0.0
    acoustic = 0.0
    speech = 0.0
    bpm = 0.0
    key = 0
    mode = 0
    index = 0
    date = ''

    def __init__(self, id, playlist_id):
        self.id = id
        self.playlist_id = playlist_id
    
    def set_info(self, index):
        self.index = index
        track_info = self.sp.audio_features(self.id)
        self.energy = track_info[0]['energy']
        self.valence = track_info[0]['valence']
        self.acoustic = track_info[0]['acousticness']
        self.speech = track_info[0]['speechiness']
        self.bpm = track_info[0]['tempo']
        self.key = track_info[0]['key']
        self.mode = track_info[0]['mode']
        self.date = self.sp.playlist_tracks(self.playlist_id, offset = index)['items'][0]['added_at'] 

    def get_index(self):
        return self.index
    
    def increment_index(self):
        self.index += 1

    #gets the average values of dance, energy, valence, and acousticness
    def get_music_avg(self):
        e = self.energy * 10 * 1.2
        v = self.valence * 10 * 1.5
        a = (1-self.acoustic) * 10
        s = self.speech * 10
        t = self.bpm / 10
        return float('%.3f'%((e + v + a + s + t)/5))
    
    #if song is in minor key then A is appended
    #if song is in major keh then B is appended
    def get_key(self):
        val = str(int(self.key))
        if(self.mode == 0):
            val += 'A'
        else:
            val += 'B'
        return val

    def get_date(self):
        return self.date