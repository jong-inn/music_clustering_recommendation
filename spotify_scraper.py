
import os
import json
import time
from spotify_api import SpotifyAPI

path = "./extracted_data"
for sub_path in ["/artists", "/albums", "/tracks", "/audio-features"]:
    if os.path.exists(path + sub_path):
        pass
    else:
        os.mkdir(path + sub_path)
        print(f"make a directory called {sub_path}")

file_list = [f for f in os.listdir(path) if f.startswith("extracted.mpd.slice.") and f.endswith(".json")]
file_list.sort()
if len(file_list) == 0:
    raise ValueError("you have to make source data first")

class SpotifyScraper:
    
    def __init__(self):
        
        pass
    
    def albums_scraper(self):
        
        spotify = SpotifyAPI()
        spotify.get_token()
        
        pass
    
    def artists_scraper(self):
        
        spotify = SpotifyAPI()
        spotify.get_token()
        
        pass
    
    def tracks_scraper(self):
        
        spotify = SpotifyAPI()
        spotify.get_token()
        
        pass
    
    def audio_features_scraper(self):
        
        spotify = SpotifyAPI()
        spotify.get_token()
        
        pass
    
    def extract_targets(self, type_, all=False):
        
        assert type_ in ["albums", "artists", "tracks", "audio-features"], "type_ has to be one of 'artists', 'albums', 'tracks', and 'audio-features'"
        
        for file in file_list:
            # load extracted.mpd.slice file
            with open(os.sep.join((path, file)), "r") as f:
                extracted = json.loads(f.read())
            
            # load type_.extracted.mpd.slice file
            if all:
                type_extracted = None
            else:
                matched_file_path = os.sep.join((path, type_, f"{type_}.{file}"))
                if os.path.exists(matched_file_path):
                    with open(matched_file_path, "r") as f:
                        type_extracted = json.loads(f.read())
                else:
                    type_extracted = None

            # find target keys
            target_keys = self.extract_different_keys(type_, extracted, type_extracted)
            yield matched_file_path, type_extracted, target_keys
    
    def extract_different_keys(self, type_, extracted, type_extracted):
        if type_ == "albums":
            keys_extracted = set(v["album_uri"] for v in extracted.values())
        elif type_ == "artists":
            keys_extracted = set(v["artist_uri"] for v in extracted.values())
        elif type_ == "tracks":
            keys_extracted = set(extracted.keys())
        elif type_ == "audio-features":
            keys_extracted = set(extracted.keys())

        if type_extracted:
            keys_type_extracted = set(type_extracted.keys())
            different_keys = keys_extracted.difference(keys_type_extracted)
            return list(different_keys)
        else:
            return list(keys_extracted)

            
if __name__ == "__main__":
    
    # spotify = SpotifyAPI()
    # spotify.get_token()
    
    # with open(os.sep.join((path, file_list[0])), "r") as f:
    #     tmp = json.loads(f.read())
    #     tmp_keys = list(tmp.keys())
        
    # tmp_dict = {}

    # try:
    #     for idx in range(0, len(tmp), 100):
            
    #         if idx % 1000 == 0:
    #             print(f"progress: {round((idx / len(tmp)) * 100, 2)} %")
            
    #         r = spotify.get_query_by_ids("audio-features", tmp_keys[idx:idx+100])
    #         tmp_dict.update(dict(zip(tmp_keys[idx:idx+100], r["audio_features"])))
    # except Exception as e:
    #     print(e)
    # finally:
    #     with open(f"./extracted_data/{'audio-features.' + file_list[0]}", "w") as f:
    #         f.write(json.dumps(tmp_dict))
    
    # for test
    scraper = SpotifyScraper()
    for matched_file_path, type_extracted, target_keys  in scraper.extract_targets("audio-features"):
        print(f"matched_file_path: {matched_file_path}")
        print(f"type_extracted   : {True if type_extracted else False}")
        print(f"target_keys      : {len(target_keys)}")