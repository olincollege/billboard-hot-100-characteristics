'''
Graphs plots based on characteristics provided by the Spotify API
'''
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def rank_data(charts):
    '''
    Averages the spotify characteristics of the songs based on rank, and
    if the song charted in the top ten songs, or in the bottom ten songs.

    Args:
        charts (DataFrame): A dataframe containing Billboard songs
            and Spotify API characteristics.

    Returns:
        A list of 2 dataframes representing the average characteristics for the
            top 10 songs, and the bottom 10 songs.
    '''
    # Converting the ranks to integers
    charts['rank'] = pd.to_numeric(charts['rank'])

    # Grouping and averaging the songs that rank in the top 10
    top_ranks = charts[(charts['rank'] <= 10) &
                       (charts['rank'] >= 1)].mean(numeric_only=True)

    # Grouping and averaging the songs that rank in the bottom 10
    bottom_ranks = charts[(charts['rank'] <= 100) &
                          (charts['rank'] >= 90)].mean(numeric_only=True)

    ranked_charts = [top_ranks, bottom_ranks]

    return ranked_charts


def plot_rank_radar_graph(ranked_charts):
    '''
    Plots a radar graph based on the average characteristics of the songs that
    ranked either in the top or bottom 10 songs in the Billboard Hot 100.

    Args:
        ranked_charts (list): A list containing two dataframes with the averaged
            characteristics, based on rank.
    '''
    # List of characteristics
    top_ranks_clean = ranked_charts[0]
    bottom_ranks_clean = ranked_charts[1]
    categories = top_ranks_clean.index
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        # Characteristics values for the top 10 songs
        r=top_ranks_clean.values,
        theta=categories,
        fill='toself',
        name='Top 10 Songs'
    ))
    fig.add_trace(go.Scatterpolar(
        # Characteristics values for the bottom 10 songs
        r=bottom_ranks_clean.values,
        theta=categories,
        fill='toself',
        name='Bottom 10 Songs'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 0.7]
            )),
        showlegend=True
    )

    fig.show()


def plot_decade_radar_graph(charts_by_decades, decade_1, decade_2):
    '''
    Plots a radar graph based on the average characteristics of the songs
    averaged by decade.

    Args:
        ranked_charts (list): A list containing two dataframes with the averaged
            characteristics, based on rank.

        decade_1 (string): A string representing a decade to be plotted.

        decade_2 (string): A string representing another decade to be plotted.
    '''
    categories = charts_by_decades.columns
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        # 50's characteristics
        r=charts_by_decades.loc[decade_1],
        theta=categories,
        fill='toself',
        name=f'Top Songs in the {decade_1}'
    ))
    fig.add_trace(go.Scatterpolar(
        r=charts_by_decades.loc[decade_2],
        theta=categories,
        fill='toself',
        name=f'Top Songs in the {decade_2}'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True
    )

    fig.show()


def plot_yearly_line_graph(charts_yearly):
    '''
    Plots a radar graph based on the average yearly characteristics of the
    Billboard Hot 100 songs.

    Args:
        charts_yearly (DataFrame): A Dataframe with the yearly averaged
            Spotify API characteristics.
    '''
    # Taking the year index as time_stamp for the graph
    time_stamp = charts_yearly.index

    # Plotting the line-graph
    plt.figure(num=1, figsize=(15, 8))

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'danceability'],
             label='Dancibility')

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'acousticness'],
             label='Acousticness')

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'energy'],
             label='Energy')

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'instrumentalness'],
             label='Instrumentalness')

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'speechiness'],
             label='Speechiness')

    plt.plot(time_stamp,
             charts_yearly.loc[:, 'valence'],
             label='Valence')

    plt.title('Characteristics of the Billboard Hot 100 over the Decades')
    plt.xlabel('Year')
    plt.ylabel('Average Song Characteristic')
    plt.legend()
    plt.show()


def plot_histogram(charts):
    '''
    Plots a radar graph based on the average yearly characteristics of the
    Billboard Hot 100 songs.

    Args:
        charts (DataFrame): A dataframe containing Billboard songs
            and Spotify API characteristics.
    '''
    # fig, plot = plt.subplots(figsize =(10, 7))
    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot(111)

    plot.hist(charts.loc[:, 'danceability'], color='blue',
              alpha=0.5, label='Danceability')
    plot.hist(charts.loc[:, 'energy'], color='yellow',
              alpha=0.5, label='Energy')
    plot.hist(charts.loc[:, 'acousticness'], color='red',
              alpha=0.5, label='Acousticness')
    plot.hist(charts.loc[:, 'valence'], color='pink',
              alpha=0.5, label='Valence')

    # Show plot
    plt.title('Frequency of the Characteristics in the Top Songs')
    plt.xlabel('Characteristic Level Per Song')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()
