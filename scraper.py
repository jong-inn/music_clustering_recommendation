
import os
import json
import time
from spotify_api import SpotifyAPI

path = "./extracted_data"
file_list = [f for f in os.listdir(path) if f.startswith("extracted.mpd.slice.") and f.endswith(".json")]
            
if __name__ == "__main__":
    
    spotify = SpotifyAPI()
    spotify.get_token()
    
    with open(os.sep.join((path, file_list[0])), "r") as f:
        tmp = json.loads(f.read())
        tmp_keys = list(tmp.keys())
        
    tmp_dict = {}

    try:
        for idx in range(0, len(tmp), 100):
            
            if idx % 1000 == 0:
                print(f"progress: {round((idx / len(tmp)) * 100, 2)} %")
            
            r = spotify.get_query_by_ids("audio-features", tmp_keys[idx:idx+100])
            tmp_dict.update(dict(zip(tmp_keys[idx:idx+100], r["audio_features"])))
    except Exception as e:
        print(e)
    finally:
        with open(f"./extracted_data/{'audio-features.' + file_list[0]}", "w") as f:
            f.write(json.dumps(tmp_dict))
