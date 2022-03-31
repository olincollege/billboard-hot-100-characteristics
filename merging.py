'''
Merge and clean individual data files created from scraper.py into one dataset
'''

import pandas as pd

def merge():
    '''
    Read weekly charts from data folder and combine them into one Pandas
    dataframe, keeping one copy of each song along with its peak position.

    Args:
        None (reads files from data folder generated by the scraper)

    Returns:
        Pandas DataFrame with every song that charted on the Billboard Hot 100
    '''

    # Set initial Timestamp. Change if you would like to start from a different
    # start date
    current_week = pd.Timestamp('1958-08-04')
    charts = pd.DataFrame()

    while current_week < pd.Timestamp('2022-03-21'):
        week = current_week.strftime('%Y-%m-%d')
        path = f'data/{week}.feather'
        chart = pd.read_feather(path)
        charts = pd.concat([charts, chart])
        current_week += pd.Timedelta(days=7)

    charts['rank'] = pd.to_numeric(charts['rank'])

    # Sort by rank and drop duplicates, keeping the one with the highest rank
    charts = charts.sort_values('rank')
    charts.drop_duplicates(subset='title', inplace=True)

    charts.reset_index(drop=True, inplace=True)
    return charts


def replace_featuring(charts):
    '''
    Change format for songs with multiple artist by removing the word
    'Featuring' and replacing it with a comma so they are compatible with the
    Spotify search function

    Args:
        charts (DataFrame): DataFrame returned by merge() function

     Returns:
         DataFrame with instances of 'Featuring' in the artists column replaced
         with a comma
    '''

    charts['artist'] = charts['artist'].str.replace(' Featuring', ',')
    return charts


def main():
    '''
    If called directly, merge and clean data
    '''
    charts = merge()
    charts_clean = replace_featuring(charts)
    charts_clean.to_feather('charts_merged.feather')


if __name__ == '__main__':
    main()
