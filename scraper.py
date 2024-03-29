'''
Scrapes Billboard web page for all Hot 100 Charts and saves them locally
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape_chart(url, week):
    '''
    Scrape a singular Billboard Hot 100 chart from a given week

    Args:
        url (string): URL from which to scrape chart
        week (string): The week the chart is from

    Returns:
        DataFrame with all the chart's songs, along with their artist and rank
    '''
    src = requests.get(url).text
    soup = BeautifulSoup(src, 'lxml')
    # Pull out the ul for each chart row
    rows = soup.select('.o-chart-results-list-row')
    songs = {'rank': [], 'title': [], 'artist': []}

    for row in rows:
        songs['rank'].append(row.li.find('span').get_text().strip())
        songs['title'].append(row.find('h3').get_text().strip())
        songs['artist'].append(row.find_all(
            'li')[3].find('span').get_text().strip())

    songs['week'] = len(songs['rank']) * [week]
    return pd.DataFrame(songs)


def scrape_all():
    '''
    Scrape all Billboard Hot 100 charts from its inception in 1958 to the
    present day and saves them as individual feather files within the 'data'
    folder (which must be present in the current directory).

    Args:
        None

    Returns:
        None (writes series of feather files to data folder)
    '''
    # Set initial Timestamp. Change to start from a different date
    current_week = pd.Timestamp('1958-08-04')
    chart = pd.DataFrame()

    while current_week < pd.Timestamp.now():
        week = current_week.strftime('%Y-%m-%d')
        print(week)
        url = f'https://www.billboard.com/charts/hot-100/{week}'
        chart = scrape_chart(url, week)
        chart.to_feather(f'data/{week}.feather')
        current_week += pd.Timedelta(days=7)


def main():
    '''Scrape all charts when run directly'''
    scrape_all()


if __name__ == '__main__':
    main()
