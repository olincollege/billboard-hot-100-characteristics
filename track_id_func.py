import spotipy
from spotipy.oauth2 import SpotifyOAuth

def track_id_finder(song, artist):
    """
    Returns the Spotify Track ID of a song when given the Song name and Artist(s)
    who created the track.

    Args:
        song: A string representing the name of a track.

        artist: A string representing the artist of a track.
    
    Returns:
        A string representing the Spotify Track ID of a song.
    """
    with open('spotify_creds.txt') as f:
        lines = f.readlines()
        SPOTIPY_CLIENT_ID = lines[0].strip()
        SPOTIPY_CLIENT_SECRET = lines[1].strip()
        SPOTIPY_REDIRECT_URI = lines[2].strip()


    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID,
                                               client_secret = SPOTIPY_CLIENT_SECRET,
                                               redirect_uri = SPOTIPY_REDIRECT_URI,
                                               scope = "user-library-read"))

    #* Searches for song using Spotify's search feature
    search_results = sp.search(q=f"track:{song} artist:{artist}", 
                                limit=1, offset=0, type='track', market="US")
    song_id = search_results["tracks"]["items"][0]['id']