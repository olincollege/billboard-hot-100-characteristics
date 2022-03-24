import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

with open('spotify_creds.txt') as f:
    lines = f.readlines()
    SPOTIPY_CLIENT_ID = lines[0].strip()
    SPOTIPY_CLIENT_SECRET = lines[1].strip()
    SPOTIPY_REDIRECT_URI = lines[2].strip()


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID,
                                               client_secret = SPOTIPY_CLIENT_SECRET,
                                               redirect_uri = SPOTIPY_REDIRECT_URI,
                                               scope = "user-library-read"))


#* Gives the name of the track given a track ID
# track_names = sp.tracks(["6Gg1gjgKi2AK4e0qzsR7sd", "32OlwWuMpZ6b0aN2RZOeMS", "6cUCckpdlqHJ5Ascf2uH2A"])
# print(track_names)

#* Results is formatted in the form of a list of dictionaries, where the indexes 
#* in the list correspond to the different track_ids, and the keys in the
#* dictionary correspond to different Spotify audio features.
# for index in range(len(results)):
#     print(f"these are the song features for: \n{results[index]}")

song = "Bandit"
artist = "Juice WRLD & YoungBoy"

song2 = "No Guidance"
artists = "Chris Brown, Drake"

hours = "Hot"
justin = "Young Thug, Gunna"

#! Create a function where you input the 
#* Searches for song using Spotify's search feature
search_results = sp.search(q=f"track:{hours} artist:{justin}", limit=1, offset=0, type='track', market="US")
song_id = search_results["tracks"]["items"][0]['id']


#* Testing for the song's attributes given track ID
results = sp.audio_features(song_id)
pprint(results)
