import pprint
import spotipy
from spotipy import SpotifyOAuth
from billboard_scraper import BillboardScraper
from datetime import datetime
import os

scope = "playlist-modify-private"
client_id = os.environ.get('CLIENT_ID')
print(client_id)
client_secret = os.environ.get('CLIENT_SECRET')
print(client_secret)
redirect_uri = "http://localhost:8888/callback"

def is_valid_date(date: str) -> bool:

    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def input_year() -> str:

    date: str = input("To which year would you like to travel to YYYY-MM-DD: ")
    while not is_valid_date(date):
        date = input("Invalid date. Please enter a date in the format YYYY-MM-DD: ")
    return date


if __name__ == '__main__':
    playlist_date = input_year()
    playlist_name = f"Billboard Hot 100 - {playlist_date}"
    song: BillboardScraper = BillboardScraper(playlist_date)
    song_name_lists = song.get_song_list()
    pprint.pprint(song_name_lists)
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            show_dialog=True,
            cache_path='token.txt'
        )
    )
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist['id']

    song_uris = []

    for song in song_name_lists:
        result = sp.search(q=f"track:{song} year:{playlist_date.split('-')[0]}", type="track")
        print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
            song_name_lists.remove(song)

    pprint.pprint(song_uris)

    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print(f"Added {len(song_name_lists)} songs to {playlist_name}.")






