"""
    Extract track, artist, and album data from raw data
    Store the data under ./extracted_data
    Data structure: {track_uri: {track_name, artist_name, artist_uri, album_name, album_uri}}
    
    Usage:
    
        python extract_data.py
"""

import os
import json

path = "./spotify_million_playlist_dataset/data"
track_set = set()
data_dict = {}

def extract_track_info(playlists):
    for playlist in playlists:
        for track in playlist["tracks"]:
            track_uri = track["track_uri"].split(":")[-1]
            if track_uri in track_set:
                pass
            else:
                track_set.add(track_uri)
                data_dict.update({
                    track_uri: {
                          "track_name" : track["track_name"]
                        , "artist_name": track["artist_name"]
                        , "artist_uri" : track["artist_uri"].split(":")[-1]
                        , "album_name" : track["album_name"]
                        , "album_uri"  : track["album_uri"].split(":")[-1]
                    }
                })

def create_data_dict(file_list):
    for file in sorted(file_list):
        if file.startswith("mpd.slice.") and file.endswith(".json"):
            full_path = os.sep.join((path, file))
            with open(full_path, "r") as f:
                mpd_slice = json.loads(f.read())
                
            extract_track_info(mpd_slice["playlists"])
            
if __name__ == "__main__":
    
    if os.path.exists("./extracted_data"):
        pass
    else:
        os.mkdir("./extracted_data")
    
    file_list = os.listdir(path)
    
    for idx in range(0, len(file_list), 100):
        create_data_dict(file_list[idx:(idx+100)])
        
        with open(f"./extracted_data/extracted.mpd.slice.{idx}-{idx+100}.json", "w") as f:
            f.write(json.dumps(data_dict))
            
        print(f"extracted.mpd.slice.{idx}-{idx+100}.json is done.")
        del data_dict
        data_dict = {}
