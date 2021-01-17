from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Retrieving top 100 songs from billboard.com
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
response.raise_for_status()

billboard_page = response.text
soup = BeautifulSoup(billboard_page, "html.parser")

songs_list = [song.getText() for song in
              soup.find_all(name="span", class_="chart-element__information__song text--truncate "
                                                "color--primary")]
# Authenticating to Spotify

client_id = "your client ID"
client_secret = "your client secret"

scope = "playlist-modify-public"
redirect_uri = "http://example.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True,
    cache_path=".cache",
))

my_id = sp.current_user()["id"]

# Adding the songs to a spotify playlist

url_list = []

for track in songs_list:
    try:
        song = sp.search(q=f"{track} year:{year}", type="track", limit=3)
        song_url = song["tracks"]["items"][0]["external_urls"]["spotify"]
        url_list.append(song_url)
    except IndexError:
        pass


playlist = sp.user_playlist_create(user=my_id,
                                      name=f"{date} Billboard 100",
                                      public=True,
                                      collaborative=False,
                                      description=f"The 100 most popular songs of {date}"
                                      )


sp.playlist_add_items(playlist_id=playlist["id"], items=url_list)
