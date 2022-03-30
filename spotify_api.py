import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
from tqdm import tqdm

class spotify_api:
    '''
    Wrapper class for spotify API that handles authentication and wraps the
    functions we require

    Attributes:
        SPOTIPY_CLIENT_ID: Credential from spotify_creds file
        SPOTIPY_CLIENT_SECRET: Credential from spotify_creds file

        sp (spotipy.Spotify): Object from official API that is used within
            this class
    '''

    def __init__(self):
        '''
        Initialize a Spotify object that can be used to connect to and make
        requests from Spotify Web API

        Args:
            None
        '''
        with open('spotify_creds.txt') as f:
            lines = [line.strip() for line in f.readlines()]
            self.SPOTIPY_CLIENT_ID = lines[0]
            self.SPOTIPY_CLIENT_SECRET = lines[1]

        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = self.SPOTIPY_CLIENT_ID,
                                                client_secret = self.SPOTIPY_CLIENT_SECRET))
    
    def track_id_finder(self, songs, artists):
        '''
        Search Spotify API for track IDs for a list of songs and corresponding
        artists

        Args:
            songs (List[str]): List of songs to find track IDs for
            artists (List[str]): List of artists corresponding to songs

        Returns:
            Pandas Series of track IDs (or NaN for missing data) that can be
                added to a DataFrame containing the songs
        '''

        # Searches for songs using Spotify's search feature
        ids = []
        length = len(songs)
        for song, artist, idx in tqdm(zip(songs, artists, range(length))):
            search_results = self.sp.search(q=f"track:{song} artist:{artist}", limit=1, offset=0, type='track', market="US")
            if (items := search_results["tracks"]["items"]): 
                ids.append(items[0]['id'])
            else:
                ids.append(np.nan)
            if idx % 10 == 0:
                print(idx*100/length)
        return pd.Series(ids)
        

    def audio_features_finder(self, track_ids):
        '''
        Get list of audio features from songs with the input track IDs.

        Args:
            track_ids (List[str]): List of track_ids from which to get audio
                features. Must be cleaned of NaNs and have a length of under
                100 as per the API's limitations.
        Returns: 
            audio_features (List[dict]): List of dictionaries containing all of
                the song features for the given songs in sequential order
        '''
        audio_features = self.sp.audio_features(track_ids)
        return audio_features
