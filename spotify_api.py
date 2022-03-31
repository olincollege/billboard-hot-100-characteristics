'''
Wrapper class for Spotify Web API
'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd

class SpotifyAPI:
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
        # This file must be created by the user
        with open('spotify_creds.txt', encoding="utf-8") as creds:
            lines = [line.strip() for line in creds.readlines()]
            self.client_id = lines[0]
            self.client_secret = lines[1]

        # Create and authenticate Spotify object
        authmanager = SpotifyClientCredentials(client_id=self.client_id,
                                               client_secret=self.client_secret)
        self.spotify = spotipy.Spotify(auth_manager=authmanager)

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
        for song, artist in zip(songs, artists):

            search_results = self.spotify.search(
                q=f"track:{song} artist:{artist}", limit=1,
                offset=0, type='track', market="US")

            if (items := search_results["tracks"]["items"]):
                ids.append(items[0]['id'])
            else:
                # Results not found
                ids.append(np.nan)

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
        audio_features = self.spotify.audio_features(track_ids)
        return audio_features
