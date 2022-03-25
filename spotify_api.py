import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

class spotify_api:

    def __init__(self):

        with open('spotify_creds.txt') as f:
            lines = [line.strip() for line in f.readlines()]
            self.SPOTIPY_CLIENT_ID = lines[0]
            self.SPOTIPY_CLIENT_SECRET = lines[1]
            self.SPOTIPY_REDIRECT_URI = lines[2]


        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = self.SPOTIPY_CLIENT_ID,
                                                client_secret = self.SPOTIPY_CLIENT_SECRET,
                                                redirect_uri = self.SPOTIPY_REDIRECT_URI,
                                                scope = "user-library-read"))
    
    def track_id_finder(self, song, artist):
        #* Searches for song using Spotify's search feature
        search_results = self.sp.search(q=f"track:{song} artist:{artist}", limit=1, offset=0, type='track', market="US")
        items = search_results["tracks"]["items"]
        
        if items:
            return items[0]['id']
        return np.nan
        

    def audio_features_finder(self, track_id):
        audio_features = self.sp.audio_features(track_id)
        return audio_features