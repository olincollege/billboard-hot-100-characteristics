# Billboard Hot 100 Characteristics

Computational essay and supporting code that explores the relationship between song characteristics and charting on the Billboard Hot 100. Written in Python.

## Setup

To install required dependencies for this project, navigate to the project folder and run:
```
pip install -r requirements.txt
```
The other required step to replicate this project is to acquire access to the Spotify API, for which there is a python library named Spotipy. You can sign up for an API key on the Spotify developer dashboard [here](https://developer.spotify.com/dashboard/login), from which you should receive two numbers - the Client ID and the Client Secret. As written, the code reads them from a text file named spotify\_creds.txt, which you will have to create, with the Client ID on the first line and the Client Secret on the second.  If you don't want to save those values in a plaintext, you can also choose to export them as environment variables and not read them from a file. For more information, see the Spotify Web API [documentation](https://developer.spotify.com/documentation/web-api/) and the Spotipy [documentation](https://spotipy.readthedocs.io).

The functions should be able to scrape the remainder of the data on their own.

## Generating Data

To generate your own data, you can run the following three scripts in order.

1. `scraper.py` will scrape each Billboard Hot 100 chart from the first one in August 1958 to the present day, saving them as individual feather files in the data directory (so that if the program fails or is interrupted, you can simply change the initial Timestamp in the file and continue on without losing progress).
2. `merging.py` combines those 3000+ files into one large dataframe and performs some preliminary data cleaning by replacing any instances of "Featuring" in a songs' artists with a comma for better compatibility with the Spotify API's search function and dropping any duplicate songs in the dataset. This function saves its result to `charts_merged.feather`.
3. Lastly, `spotify_data.py` will attempt to find the unique Spotify track IDs for each song in the dataset, do some more cleaning by dropping any songs that IDs couldn't be found for, and adding in all of the Spotify song characteristics into the dataset, which are danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration\_ms, and time\_signature. This script saves its result to `charts_clean.feather`.

## Visualizations

After importing `charts_clean.feather` as a dataframe using the `pandas` function `.to_feather`, very similar visualizations can be achieved through use of `matplotlib` and `plotly`, with the help of `spotify_data.py` and `data_visualization.py`.

1. To create the line graph comparing multiple characteristics over the course of time, the year that the song charted will be required. This can be attained through the function `get_date_information` in `spotify_data.py`. Afterwards, the characteristics are grouped, averaged, and sorted by year using the `pandas` functions `.groupby`, `.mean`, and `.to_datetime`, respectively. Now using the `plot_yearly_line_graph` function from `data_visualization.py`, the characteristics can be plotted on a line graph.
2. The rank radar graph displays the average characteristics of songs that rank highest and lowest on the Billboard Hot 100. This is used to compare the higher and lower songs and possibly determine what makes the top 10 and bottom 10 songs differ. To do so, you'd use the `rank_data` function from `data_visualization.py`. This data now has to be filtered to drop the attributes that aren't necessary for the radar graph using the `pandas` function `.drop`. The newly filtered data can be plotted using the `plot_rank_radar_graph` from `data_visualization.py`.
3. The decade radar graph displays the song characteristics on the Billboard Hot 100 by decade. This is especially useful for identifying generational trends in how music has evolved over the years. To create a similar plot, you'd first use the `pandas` functions `.groupby` and `.mean`, to group and average the data. Similarly to the rank radar graph, the attributes that aren't necessary for the graph are dropped using the `pandas` function `.drop`. The data can now be plotted using `plot_decade_radar_graph` from `data_visualization.py`, and different decades can be compared through use of this function.
4. The final graph is a histogram that graphs the frequencies at which song characteristics of the Billboard Hot 100 are exhibited. Plotting this graph is simple, it only requires the data acquired to be inputted in the `plot_histogram` function from `data_visualization.py`.