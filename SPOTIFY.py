import spotipy, config
from spotipy.oauth2 import SpotifyClientCredentials

if config.clientId == "" or config.clientSecret == "":
    print("Please enter your Spotify client ID and secret in config.py")
    exit()

# Infomation Required
# url, title, duration, thumbnail

# For Playlist all theses info are required for each track in dict in list


def getTrackInfo(url):
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=config.clientId, client_secret=config.clientSecret
        )
    )

    if url.__contains__("track"):
        # Getting The Info of the Track
        try:
            track_id = url.split("track/")[-1]
            track_info = sp.track(track_id)
            title = track_info["name"]
            duration = round(float(track_info["duration_ms"] / 60000), 2)
            thumbnail = track_info["album"]["images"][0]["url"]
            preview_url = track_info["preview_url"]
            if preview_url == None:
                return None, None, None, None
            return preview_url, title, duration, thumbnail
        except:
            return None, None, None, None

    if url.__contains__("playlist"):
        # Getting The Info of the Playlist
        try:
            playlist_id = url.split("playlist/")[-1]
            playlist_info = sp.playlist(playlist_id)
            title = playlist_info["name"]
            tracks = playlist_info["tracks"]["items"]
            track_list = []
            for track in tracks:
                track_title = track["track"]["name"]
                track_duration = round(float(track["track"]["duration_ms"] / 60000), 2)
                track_thumbnail = track["track"]["album"]["images"][0]["url"]
                track_preview = track["track"]["preview_url"]
                if track_preview == None:
                    continue
                track_list.append(
                    {
                        "url": track_preview,
                        "title": track_title,
                        "duration": track_duration,
                        "thumbnail": track_thumbnail,
                    }
                )
            return track_list
        except:
            return None
