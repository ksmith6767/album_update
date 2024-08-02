import os
import sys

import eyed3
from eyed3 import AudioFile
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

clientID = os.environ['SPOTIFY_CLIENT_ID']
clientSecret = os.environ['SPOTIFY_CLIENT_SECRET']


def get_track_name_to_num(spotify_url: str) -> dict[str, int]:
    track_name_to_num: dict[str, int] = {}

    spotify_object = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret))
    if not spotify_object:
        raise Exception('Could not make spotify connection!')

    album_tracks = \
        spotify_object.album_tracks(spotify_url)
    if not album_tracks:
        raise Exception('Could not locate album in spotify!')

    for track in album_tracks['items']:
        track_number = track['track_number']
        track_name = track['name']
        track_name_to_num[track_name] = track_number

    return track_name_to_num


if __name__ == '__main__':
    args: list[str] = sys.argv
    if len(args) != 2:
        raise Exception('Script requires a spotify share link to the album!')

    album_dir: str = os.getcwd()
    spotify_link: str = args[1]

    track_name_to_num: dict[str, int] = get_track_name_to_num(spotify_link)

    file_names: list[str] = os.listdir(album_dir)
    for file_name in file_names:
        if '.mp3' not in file_name:
            continue
        song: AudioFile = eyed3.load(album_dir + '\\' + file_name)
        song.tag.track_num = track_name_to_num.get(song.tag.title)
        song.tag.save()
