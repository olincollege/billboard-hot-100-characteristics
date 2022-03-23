from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pprint import pprint

def scrape_chart(url, week):
    src = requests.get(url).text
    soup = BeautifulSoup(src, 'lxml')
    rows = soup.select('.o-chart-results-list-row') # Pull out the ul for each chart row
    songs = {'rank': [], 'title': [], 'artist': []}

    for row in rows:
        songs['rank'].append(row.li.find('span').get_text().strip())
        songs['title'].append(row.find('h3').get_text().strip())
        songs['artist'].append(row.find_all('li')[3].find('span').get_text().strip())    
    
    songs['week'] = len(songs['rank']) * [week]
    return pd.DataFrame(songs)

def scrape_all():
    ts = pd.Timestamp('1958-08-04')
    chart = pd.DataFrame()

    while ts < pd.Timestamp.now():
        week = ts.strftime('%Y-%m-%d')
        print(week)
        url = f'https://www.billboard.com/charts/hot-100/{week}'
        chart = scrape_chart(url, week)
        chart.to_feather(f'data/{week}.feather')
        ts += pd.Timedelta(days=7)

def main():
    scrape_all()

if __name__ == '__main__':
    main()
