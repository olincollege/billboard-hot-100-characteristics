'''
PyTest Functions
'''
import pandas as pd
import numpy as np
from merging import replace_featuring
from spotify_data import clean_data
from spotify_data import get_date_information


def test_replace_featuring():
    '''
    Test function that replaces instances of ' Featuring' in artist names with a
    comma
    '''
    test_df = pd.DataFrame()
    test_df['artist'] = ['Future', 'Future Featuring Drake', 'Featuring']

    replaced = replace_featuring(test_df)
    assert (replaced['artist'] == pd.Series(
        ['Future', 'Future, Drake', 'Featuring'])).all()


def test_clean_data():
    '''
    Test function that drops NaN values and resets the index to run sequentially
    '''
    test_df = {'rank': [1, 1, 1], 'title': ['a', 'b', 'c'],
               'artist': ['a1', 'b1', 'c1'],
               'week': ['1958-08-04', '1958-08-04', '1958-08-04'],
               'trackid': ['2qufhsj', np.nan, 'aisfaivu']}

    test_df = pd.DataFrame(test_df)
    clean = clean_data(test_df)

    assert clean.shape == (2, 5)
    assert list(clean.index) == [0, 1]


def test_get_date_information():
    '''
    Test function that retrieves the year and decade information based on the
    `week` category in the dataframe given.
    '''
    test_df = {'rank': [1, 1, 1], 'title': ['a', 'b', 'c'],
               'artist': ['a1', 'b1', 'c1'],
               'week': ['1958-08-04', '2004-08-04', '1967-08-04'],
               'trackid': ['2qufhsj', np.nan, 'aisfaivu']}

    test_df = pd.DataFrame(test_df)
    date_info_df = get_date_information(test_df)

    for i in range(len(date_info_df.loc[:, 'year'])):
        assert date_info_df.loc[i, 'year'] == ['1958', '2004', '1967'][i]
        assert date_info_df.loc[i, 'decade'] == ["50's", "2000's", "60's"][i]
