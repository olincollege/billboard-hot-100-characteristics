'''
PyTest Functions
'''
import pandas as pd
import numpy as np
from data_visualization import rank_data


def test_rank_data():
    '''
    Test function that groups song characteristics by rank and averages them.
    '''
    test_df = {'rank': [1, 7, 15, 98, 99], 'title': ['a', 'b', 'c', 'd', 'e'],
               'artist': ['a1', 'b1', 'c1', 'd1', 'e1'],
               'week': ['1958-08-04', '1958-08-04', '1958-08-04', '1958-08-04',
                        '1958-08-04'],
               'trackid': ['2qufhsj', np.nan, 'aisfaivu', 'afiahjia', '18907h'],
               'valence': [0.76, np.nan, 0.25, 0.12, 0.2]}

    test_df = pd.DataFrame(test_df)
    ranked_data = rank_data(test_df)
    ranked_data_df = pd.DataFrame(ranked_data)
    for i in range(len(ranked_data_df.loc[:, "valence"])):
        assert ranked_data_df.loc[i, "valence"] == [0.76, 0.16][i]
