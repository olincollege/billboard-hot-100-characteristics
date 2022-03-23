import pandas as pd

ts = pd.Timestamp('1958-08-04')
charts = pd.DataFrame()
while ts < pd.Timestamp.now():
    week = ts.strftime('%Y-%m-%d')
    path = f'data/{week}.feather'
    chart = pd.read_feather(path)
    charts = pd.concat([charts, chart])
    ts += pd.Timedelta(days=7)

charts.reset_index(inplace=True)
charts.to_feather('charts.feather')

