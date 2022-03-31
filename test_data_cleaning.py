'''
PyTest Functions
'''
import pandas as pd
import numpy as np
from merging import replace_featuring
from spotify_data import clean_data


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
    Test functoin that drops NaN values and resets the index to run sequentially
    '''
    test_df = {'rank': [1, 1, 1], 'title': ['a', 'b', 'c'],
               'artist': ['a1', 'b1', 'c1'],
               'week': ['1958-08-04', '1958-08-04', '1958-08-04'],
               'trackid': ['2qufhsj', np.nan, 'aisfaivu']}

    test_df = pd.DataFrame(test_df)
    clean = clean_data(test_df)

    assert clean.shape == (2, 5)
    assert list(clean.index) == [0, 1]
