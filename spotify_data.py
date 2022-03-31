'''
Uses Spotify API to gather data on Hot 100 songs
'''
import numpy as np
import pandas as pd
from spotify_api import SpotifyAPI

sp = SpotifyAPI()
# Define attributes we want to keep
ATTRIBUTES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
              'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
              'duration_ms', 'time_signature']

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
    # Batch request audio features 100 at a time per Spotify docs
    for i in range(0, 1000, 100):
        subset = charts.iloc[i:i+100]
        audio_features = sp.audio_features_finder(subset['trackid'])

        # Create Dataframe of wanted and set index to merge into main dataframe
        toadd = pd.DataFrame(audio_features)[ATTRIBUTES]
        toadd.set_index(np.arange(i, i+100), inplace=True)
        charts.update(toadd)

    return charts


def clean_data(charts):
    '''
    Clean data by removing any NaNs, reseting the indexing to run from 0
    sequentially, and resetting the weeks to date_time format.
    '''
    charts = charts.dropna()
    charts.reset_index(drop=True, inplace=True)
    return charts

def get_date_information(charts):
    '''
    Add more column information including the decade and the year of the songs,
    and resets the week column to datetime format.

    Args:
        charts (DataFrame): Cleaned charts DataFrame containing Track IDs with
            no NaNs

    Returns:
        The same DataFrame as the input, but with columns added for the songs'
            decade, year, and week each song charted, with the week in
            datetime format.
    '''
    decade = []
    year_info = []
    for i in range(len(charts.loc[:,"week"])):
        # Checking the decade of the songs for each song
        year = str(charts.loc[:,"week"][i])[0:4]
        decade_year = int(year[2])
        year_info.append(year)
        if decade_year in range(5,10):
            decade.append(f"{decade_year}0's")
        else:
            decade.append(f"20{decade_year}0's")

    # Adding the Decade and Year information into the DataFrame
    charts = charts.assign(decade = decade, year = year_info)
    # Converting the week column to dates
    charts['week'] = pd.to_datetime(charts['week'])
    return charts

def main():
    '''
    If ran directly, read in the charts_merged file generated from merging.py,
    add in the track IDs, drop any NaNs, add columns with the song
    characteristics and the year information, and save the output to
    charts_clean.feather.
    '''
    charts = pd.read_feather('charts_merged.feather')
    charts_id = get_track_ids(charts)
    charts_clean = clean_data(charts_id)
    charts_features = get_features(charts_clean)
    charts_year_info = get_date_information(charts_features)
    charts_year_info.to_feather('charts_clean.feather')


if __name__ == '__main__':
    main()
