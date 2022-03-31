'''
PyTest Functions
'''
import pandas as pd
import numpy as np
from merging import replace_featuring
from spotify_data import clean_data

def test_replace_featuring():
    test_df = pd.DataFrame()
    test_df['artist'] = ['Future', 'Future Featuring Drake', 'Featuring']

    replaced = replace_featuring(test_df)
    assert (replaced['artist'] == pd.Series(['Future', 'Future, Drake', 'Featuring'])).all()

def test_clean_data():
    df = {'rank': [1,1,1], 'title': ['a', 'b', 'c'],
            'artist': ['a1', 'b1', 'c1'],
            'week': ['1958-08-04', '1958-08-04', '1958-08-04'],
            'trackid': ['2qufhsj', np.nan, 'aisfaivu']}

    df = pd.DataFrame(df)
    clean = clean_data(df)

    assert clean.shape == (2, 5)
    assert list(clean.index) == [0,1]

