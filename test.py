import argparse
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = '9658408922bd4309aee868f54c6ca714'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'ee1fc29686894896b24d0f6adc7384a9'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://developer.spotify.com/dashboard/applications/9658408922bd4309aee868f54c6ca714'

USER = os.getenv('SPOTIPY_CLIENT_ID')
SECRET = os.getenv('SPOTIPY_CLIENT_ID')
REDIRECT = os.getenv('SPOTIPY_REDIRECT_URI')

print(USER, SECRET, REDIRECT)

logger = logging.getLogger('examples.add_tracks_to_playlist')
logging.basicConfig(level='DEBUG')
scope = 'playlist-modify-public'


def get_args():
    parser = argparse.ArgumentParser(description='Adds track to user playlist')
    
    parser.add_argument('-t', '--tids', action='append',
                        required=True, help='Track ids')
    
    parser.add_argument('-p', '--playlist', required=True,
                        help='Playlist to add track to')
    
    return parser.parse_args()


def main():
    args = get_args()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    sp.user_playlist_add_tracks(user=USER, playlist_id=args.playlist, tracks=args.tids)


if __name__ == '__main__':
    main()
    