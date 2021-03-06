import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Playlist import Playlist
from Song import Track

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = 'CLIENT_ID', 
    client_secret = 'CLIENT_SECRET', 
    redirect_uri = 'REDIRECT_URI',
    scope = "SCOPE",
    username = 'USER_ID'))

#create a list of all the ids of user's playlists
#param list of playlist names
#param list of number of tracks in each playlist
def get_playlists(playlist_name, track_totals):
    playlist_id = []
    playlists = sp.current_user_playlists()
    for list in playlists['items']:
        playlist_id.append(list['id'])
        playlist_name.append(list['name'])
        track_totals.append(list['tracks']['total'])
    
    return playlist_id
     
#returns the number of loops to go through tracks
#param list of playlist track totals
#param playlist number index
def get_loop_offset(track_totals, playlist_number):
    return int(track_totals[playlist_number]/100) + 1

#returns a total list of Track objects of given playlist
#param id of wanted playlist
#param offset
def get_tracks(playlist_id, offset):
    tracks= []
    for i in range(offset):
        track_id = get_song_set(playlist_id, i*100)
        playlist = Playlist(playlist_id, track_id)
        tracks += playlist.set_tracks(i*100)
    return tracks

#creates a list of song ids for each set of 100
#param id of playlist
#index of the song in playlist
def get_song_set(playlist_id, index):
    tracks = sp.playlist_tracks(playlist_id, offset = index) 
    track_ids = []
    for song_id in tracks['items']:
        track_ids.append(song_id['track']['id'])
    return track_ids
        
#compares the current song key with the next song key
def compare_keys(list, currSong, nextSong):
    curr = currSong.get_key()
    next = nextSong.get_key()
    if(curr == '8A'):
        list.append(key_val(curr, next, '1A', '3A', '11B', '4B','6B'))
    elif(curr == '3A'):
        list.append(key_val(curr, next, '8A', '10A', '6B', '11B', '1B'))
    elif(curr == '10A'):
        list.append(key_val(curr, next, '3A', '5A', '1B', '6B', '8B'))
    elif(curr == '5A'):
        list.append(key_val(curr, next, '10A', '0A', '8B', '1B', '3B'))
    elif(curr == '0A'):
        list.append(key_val(curr, next, '5A', '7A', '3B', '8B', '10B'))
    elif(curr == '7A'):
        list.append(key_val(curr, next, '0A', '2A', '10B', '3B', '5B'))
    elif(curr == '2A'):
        list.append(key_val(curr, next, '7A', '9A', '5B', '10B', '0B'))
    elif(curr == '9A'):
        list.append(key_val(curr, next, '2A', '4A', '0B', '5B', '7B'))
    elif(curr == '4A'):
        list.append(key_val(curr, next, '9A', '11A', '7B', '0B', '2B'))
    elif(curr == '11A'):
        list.append(key_val(curr, next, '4A', '6A', '2B', '7B', '9B'))
    elif(curr == '6A'):
        list.append(key_val(curr, next, '11A', '1A', '9B', '2B', '4B'))
    elif(curr == '1A'):
        list.append(key_val(curr, next, '6A', '8A', '4B', '9B', '11B'))


    elif(curr == '11B'):
        list.append(key_val(curr, next, '6B', '4B', '8A', '3A', '1A'))
    elif(curr == '6B'):
        list.append(key_val(curr, next, '1B', '11B', '3A', '10A', '8A'))
    elif(curr == '1B'):
        list.append(key_val(curr, next, '8B', '6B', '10A', '5A', '3A'))
    elif(curr == '8B'):
        list.append(key_val(curr, next, '3B', '1B', '5A', '0A', '10A'))
    elif(curr == '3B'):
        list.append(key_val(curr, next, '10B', '8B', '0A', '7A', '5A'))
    elif(curr == '10B'):
        list.append(key_val(curr, next, '5B', '3B', '7A', '2A', '0A'))
    elif(curr == '5B'):
        list.append(key_val(curr, next, '0B', '10B', '2A', '9A', '7A'))
    elif(curr == '0B'):
        list.append(key_val(curr, next, '7B', '5B', '9A', '4A', '2A'))
    elif(curr == '7B'):
        list.append(key_val(curr, next, '2B', '0B', '4A', '11A', '9A'))
    elif(curr == '2B'):
        list.append(key_val(curr, next, '9B', '7B', '11A', '6A', '4A'))
    elif(curr == '9B'):
        list.append(key_val(curr, next, '4B', '2B', '6A', '1A', '11A'))
    elif(curr == '4B'):
        list.append(key_val(curr, next, '11B', '9B', '1A', '8A', '6A'))

#compares two keys to how close they are based on camelot wheel
#param current song key
#param next song key
#param bottom left key
#param bottom right key
#param top key
#param top left key
#param top right key
def key_val(curr, next, bl, br, t, tl, tr):
    if(curr == next):
        return 0
    elif(next == bl):
        return 1
    elif(next == br):
        return 2
    elif(next == t):
        return 3
    elif(next == tl):
        return 4
    elif(next == tr):
        return 5
    else:
        return 10

#sorts by comparing each track key with the next several track keys and 
#chooses the next track as the most similar in key
#if the next keys are not in range of closeness then the next track stays in place
#param id of playlist
#param list of sorted Track objects
def sort_by_key(playlist_id, tracks):
    limit = 4                           #number of tracks ahead to compare to
    if(len(tracks) > 100):              #if there are more than 100 tracks, the track will be compared
        limit = 7                       #to next 7 tracks instead of 3

    for i in range(len(tracks)-1):                  
        curr_song = tracks[i]                         
        j = 1
        temp = []

        while(i + j < len(tracks) and j < limit): 
            next_song = tracks[i+j]
            compare_keys(temp, curr_song, next_song)
            j += 1

        low = min(temp)
        if min(temp) == 10:
            low = 1
        else:
            low = temp.index(min(temp)) + 1
        #print(low)
        print(curr_song.get_music_avg())

        track = tracks.pop(low + i)     #pops out the track with closest key
        tracks.insert(i+1, track)       #inserts it as the next track

    return tracks

#uses the playlist id and list of track objects
#sorts the list of songs by value then key
#returns the sorted list
#param id of playlist
#param list of Track objects
def sort_by_values(playlist_id, tracks):
    tracks.sort(key=lambda song: song.get_music_avg(), reverse=False)
    new_tracks = sort_by_key(playlist_id, tracks)
    return new_tracks

def reorder_by_date(playlist_id, tracks):
    tracks.sort(key=lambda song: song.get_date(), reverse=False)
    user = sp.me()['id']
    for i in range(len(tracks)):
        sp.user_playlist_reorder_tracks(user, playlist_id, tracks[i].get_index(), i)
        increment_list(tracks[i].get_index(), tracks)
    

#increments the value of each item if it is less than target value
#param target value
#param list
def increment_list(val, list):
    for i in list:
        if(i.get_index() < val):
            i.increment_index()

#reorders the sorted list to actual playlist
#param playlist id
#param sorted track list
def reorder(playlist_id, tracks):
    user = sp.me()['id']
    for i in range(len(tracks)):
        sp.user_playlist_reorder_tracks(user, playlist_id, tracks[i].get_index(), i)
        increment_list(tracks[i].get_index(), tracks)

#sorts one playlist
def reorder_one_playlist_val_key():
    playlist_names = []                                                             #blank list of playlist names
    track_totals = []                                                               #blank list of track totals of each playlist
    ids = get_playlists(playlist_names, track_totals)                               #creates list of playlist ids  
    for i in range(len(playlist_names)):                                            #prints playlist names in order
        print(str(i + 1) + " : " + playlist_names[i])
    print("Enter the playlist number you want sorted")
    playlist_number = int(input(""))-1     #input which playlist number you want sorted 

    playlist_id = ids[playlist_number]                                              #gets the id of playlist wanted
    offset = get_loop_offset(track_totals, playlist_number)                         #get the playlist offset
    tracks = get_tracks(playlist_id, offset)                                        #gets the list of Track objects

    sorted_tracks = sort_by_values(playlist_id, tracks)                            #creates a sorted list with value and key
    reorder(playlist_id, sorted_tracks)                                            #reorders the playlist

def reorder_one_playlist_date():
    playlist_names = []                                                             #blank list of playlist names
    track_totals = []                                                               #blank list of track totals of each playlist
    ids = get_playlists(playlist_names, track_totals)                               #creates list of playlist ids  
    for i in range(len(playlist_names)):                                            #prints playlist names in order
        print(str(i + 1) + " : " + playlist_names[i])

    playlist_number = int(input("Enter the playlist number you want sorted:"))-1     #input which playlist number you want sorted 

    playlist_id = ids[playlist_number]                                              #gets the id of playlist wanted
    offset = get_loop_offset(track_totals, playlist_number)                         #get the playlist offset
    tracks = get_tracks(playlist_id, offset)                                        #gets the list of Track objects
    reorder_by_date(playlist_id, tracks)

def main():
    print("1: reorder by speechiness")
    print("2: reorder by date")
    print("Enter the number you want for you playlist:")
    val = int(input(""))
    if val == 1:
        reorder_one_playlist_val_key()
    elif val == 2:
        reorder_one_playlist_date()
    else:
        print('try again')
        main()

if __name__ == "__main__":
    main()