from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import spotipy

load_dotenv()

class Fetcher:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET'),
                redirect_uri='http://127.0.0.1:8000/callback',
                scope='playlist-read-private playlist-read-collaborative',
            )
        )

    def fetch_songs_in_playlist(self, target: str) -> list[str]:
        data = self.get_playlists(targets=[target])

        if not data:
            raise ValueError(f'{target} not a valid playlist')

        data = data[0]

        tracks = []

        results = self.sp.playlist_items(data['id'])
        tracks.extend(results["items"])

        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])

        track_strs = []

        for track in tracks:
            track = track['track']
            artists = ", ".join([a["name"] for a in track["artists"]])
            track_strs.append(f'{track["name"]} by {artists}')

        return track_strs

    def get_playlists(self, targets: list[str] = None, name_only: bool = False):
        if targets is None:
            targets = []

        targets = set(targets)

        playlists = []
        results = self.sp.current_user_playlists()
        playlists.extend(results["items"])

        # paginate
        while results["next"]:
            results = self.sp.next(results)
            playlists.extend(results["items"])

        if targets:
            playlists = [x for x in playlists if x['name'] in targets]

        if name_only:
            playlists = [x['name'] for x in playlists]

        return playlists

def main():
    fetcher = Fetcher()

    for x in fetcher.fetch_songs_in_playlist('hades faves'):
        print(x)


if __name__ == '__main__':
    main()