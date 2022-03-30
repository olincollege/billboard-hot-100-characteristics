from spotify_api import spotify_api
import numpy as np
import pandas as pd
from tqdm import tqdm

sp = spotify_api()

def get_track_ids(charts):
    charts['trackid'] = sp.track_id_finder(charts['title'], charts['artist'])
    return charts

def get_features(charts):
    ATTRIBUTES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                'duration_ms', 'time_signature']
    for i in tqdm(range(0, len(charts), 100)):
        subset = charts.iloc[i:i+100]
        audio_features = sp.audio_features_finder(subset['trackid'])
        toadd = pd.DataFrame(audio_features)[ATTRIBUTES]
        toadd['title'] = subset['title']
        charts = charts.merge(toadd, how='left')
    
    return charts

def clean_data(charts):
    charts = charts.dropna()
    charts.reset_index(drop=True, inplace=True)
    return charts

def main():
    pd.read_feather('charts_clean.feather')
    charts_id = get_track_ids(charts)
    charts_clean = clean_data(charts_id)
    charts_features = get_features(charts_clean)
    charts_features.to_feather('charts_clean.feather')

if __name__ == '__main__':
    main()



