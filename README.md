# Billboard Hot 100 Characteristics

Computational essay and supporting code that explores the relationship between song characteristics and charting on the Billboard Hot 100. Written in Python.

## Setup

To install required dependencies for this project, navigate to the project folder and run:
```
pip install -r requirements.txt
```
The other required step to replicate this project is to acquire access to the Spotify API, for which there is a python library named Spotipy. You can sign up for an API key on the Spotify developer dashboard [here](https://developer.spotify.com/dashboard/login), from which you should receive two numbers - the Client ID and the Client Secret. As written, the code reads them from a text file named spotify\_creds.txt, which you will have to create, with the Client ID on the first line and the Client Secret on the second.  If you don't want to save those values in a plaintext, you can also choose to export them as environment variables and not read them from a file. For more information, see the Spotify Web API [documentation](https://developer.spotify.com/documentation/web-api/) and the Spotipy [documentation](https://spotipy.readthedocs.io)

The functions should be able to scrape the remainder of the data on their own.

## Generating Data

To generate your own data, you can run the following three scripts in order.

1. `scraper.py` will scrape each Billboard Hot 100 chart from the first one in August 1958 to the present day, saving them as individual feather files in the data directory (so that if the program fails or is interrupted, you can simply change the initial Timestamp in the file and conitnue on without losing progress).
2. `merging.py` combines those 3000+ files into one large dataframe and performs some preliminary data cleaning by replacing any instances of "Featuring" in a songs' artists with a comma for better compatibility with the Spotify API's search function and dropping any duplicate songs in the dataset. This function saves its result to `charts_merged.feather`.
3. Lastly, `spotify_data.py` will attempt to find the unique Spotify track IDs for each song in the dataset, do some more cleaning by dropping any songs that IDs couldn't be found for, and adding in all of the Spotify song characteristics into the dataset, which are danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration\_ms, and time\_signature. This script saves its result to `charts_clean.feather`.

## Visualizations

