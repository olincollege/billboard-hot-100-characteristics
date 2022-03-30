import pandas as pd
from tqdm import tqdm

def merge():
    ts = pd.Timestamp('1958-08-04')
    charts = pd.DataFrame()
    for _ in tqdm(range(3321)): # number of weeks since 1958
        week = ts.strftime('%Y-%m-%d')
        path = f'data/{week}.feather'
        chart = pd.read_feather(path)
        charts = pd.concat([charts, chart])
        ts += pd.Timedelta(days=7)

    charts['rank'] = pd.to_numeric(charts['rank'])
    charts = charts.sort_values('rank')
    charts.drop_duplicates(subset='title', inplace=True)
    charts.reset_index(inplace=True)
    return charts

def replace_featuring(charts):
   for artist in charts['artist']:
       artist = artist.replace(' Featuring', ',')
   return charts

def main():
    charts = merge()
    charts_clean = replace_featuring(charts)
    charts_clean.to_feather('charts_merged.feather')

if __name__ == '__main__':
    main()
