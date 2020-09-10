import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import web_scrape
from selenium import webdriver

def createPlaylist():
    scope = "playlist-modify-public"
    cache_path= 'user_cache/.cache'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=cache_path))

    username = sp.me()
    username = username['id']

    if not os.path.isfile(cache_path + str(username)):
        sp.auth_manager.cache_path = cache_path + str(username)
        os.rename(cache_path, cache_path + str(username))

    song_list = web_scrape.songList()
    playlist_date = song_list[1]
    song_list = song_list[0]

    track_ids = []

    for song in song_list:
        results = sp.search(q=song, limit=1, type='track')

        if results['tracks']['total'] == 0:
            continue
        else:
            track_ids.append(results['tracks']['items'][0]['id'])

    track_ids = list(dict.fromkeys(track_ids))

    sp.user_playlist_create(user=username, name='Radio Kampus ' + playlist_date, public=True, description='Radio Kampus Playlist from ' + playlist_date)

    playlist_name = 'Radio Kampus ' + playlist_date
    playlist_id = ''
    playlists = sp.user_playlists(username)

    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    track_ids = list(chunks(track_ids, 100))

    for track_list in track_ids:
        sp.user_playlist_add_tracks(username, playlist_id, track_list)

createPlaylist()