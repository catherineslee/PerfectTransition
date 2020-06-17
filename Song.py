from math import trunc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Track(object):
    client_credentials_manager = SpotifyClientCredentials(client_id = '3807740e1a274c5185d6723967a00f5b', 
    client_secret = '8718585c5b1f453689655c20034988ee')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    id = ''
    energy = 0.0
    dance = 0.0
    valence = 0.0
    acoustic = 0.0
    key = 0
    mode = 0
    index = 0

    def __init__(self, id):
        self.id = id
    
    def set_info(self, index):
        self.index = index
        track_info = self.sp.audio_features(self.id)
        self.energy = track_info[0]['energy']
        self.dance = track_info[0]['danceability']
        self.valence = track_info[0]['valence']
        self.acoustic = track_info[0]['acousticness']
        self.key = track_info[0]['key']
        self.mode = track_info[0]['mode']

    def get_index(self):
        return self.index
    
    def increment_index(self):
        self.index += 1

    #gets the average values of dance, energy, valence, and acousticness
    def get_music_avg(self):
        d = (self.dance * 10)
        e = (self.energy * 10)
        v = (self.valence * 10)
        a = (1-self.acoustic) * 10
        return float('%.3f'%((d + e + v + a)/4))
    
    #if song is in minor key then A is appended
    #if song is in major keh then B is appended
    def get_key(self):
        val = str(int(self.key))
        if(self.mode == 0):
            val += 'A'
        else:
            val += 'B'
        return val