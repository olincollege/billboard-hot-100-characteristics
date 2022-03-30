from spotify_api import spotify_api
import numpy as np
import pandas as pd

sp = spotify_api()

def get_track_ids(charts):
    '''
    Add column to charts DataFrame containing Spotify track IDs for each song
    where they could be found and NaN where they couldn't

    Args:
        charts (DataFrame): Charts dataframe containing Billboard songs
            generated from merging.py

    Returns:
        The same DataFrame as the input, but with a column added for the songs'
            track IDs
    '''
    charts['trackid'] = sp.track_id_finder(charts['title'], charts['artist'])
    return charts

def get_features(charts):
    '''
    Add columns to charts DataFrame containing Spotify track characteristics
    for each song

    Args:
        charts (DataFrame): Cleaned charts DataFrame containing Track IDs with
            no NaNs

    Returns:
        The same DataFrame as the input, but with columns added for the songs'
            relevant Spotify characteristics
    '''
    ATTRIBUTES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                'duration_ms', 'time_signature']
    for i in range(0, len(charts), 100):
        subset = charts.iloc[i:i+100]
        audio_features = sp.audio_features_finder(subset['trackid'])
        toadd = pd.DataFrame(audio_features)[ATTRIBUTES]
        toadd['title'] = subset['title']
        charts = charts.merge(toadd, how='left')
    
    return charts

def clean_data(charts):
    '''
    Clean data by removing any NaNs and reseting the indexing to run from 0
    sequentially
    '''
    charts = charts.dropna()
    charts.reset_index(drop=True, inplace=True)
    return charts

def main():
    '''
    If ran directly, read in the charts_merged file generated from merging.py,
    add in the track IDs, drop any NaNs, add columns with the song
    characteristics, and save the output to charts_clean.feather
    '''
    pd.read_feather('charts_merged.feather')
    charts_id = get_track_ids(charts)
    charts_clean = clean_data(charts_id)
    charts_features = get_features(charts_clean)
    charts_features.to_feather('charts_clean.feather')

if __name__ == '__main__':
    main()



