
import os
import argparse
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
    
    # initialize the instance
    def __init__(self):
        pass
            
    def scraper(self, type_, all=False):
        
        response_key = type_.replace("-", "_")
        
        spotify = SpotifyAPI()
        spotify.get_token()
        
        for matched_file_path, type_extracted, target_keys in self.extract_targets(type_, all):
            start_time = time.time()
            print(f"{matched_file_path}")
            
            try:
                for batch_keys in self.make_batches(type_, target_keys):
                    response = spotify.get_query_by_ids(type_, batch_keys)
                    type_extracted.update(dict(zip(batch_keys, response[response_key])))
            except Exception as e:
                print(e)
            finally:
                with open(matched_file_path, "w") as f:
                    f.write(json.dumps(type_extracted))
                
                end_time = time.time()
                print(f"elapsed time: {round((end_time - start_time) / 60, 2)} mins")
    
    def extract_targets(self, type_, all=False):
        
        assert type_ in ["albums", "artists", "tracks", "audio-features"], "type_ has to be one of 'artists', 'albums', 'tracks', and 'audio-features'"
        
        for file in file_list:
            # load extracted.mpd.slice file
            with open(os.sep.join((path, file)), "r") as f:
                extracted = json.loads(f.read())
            
            # load type_.extracted.mpd.slice file
            if all:
                type_extracted = {}
            else:
                matched_file_path = os.sep.join((path, type_, f"{type_}.{file}"))
                if os.path.exists(matched_file_path):
                    with open(matched_file_path, "r") as f:
                        type_extracted = json.loads(f.read())
                else:
                    type_extracted = {}

            # find target keys
            target_keys = self.extract_different_keys(type_, extracted, type_extracted)
            if len(target_keys) == 0:
                continue
            else:
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

    def make_batches(self, type_, target_keys):
        if type_ == "albums":
            batch_size = 20
        elif type_ == "artists":
            batch_size = 50
        elif type_ == "tracks":
            batch_size = 50
        elif type_ == "audio-features":
            batch_size = 100
        
        for idx in range(0, len(target_keys), batch_size):
            if idx % 20000 == 0:
                print(f"{type_} scraping progress: {round(idx / len(target_keys) * 100, 2)}")
            
            yield target_keys[idx:idx + batch_size]

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="scraping spotify data using its api")
    
    parser.add_argument("-t", "--type"
                        , action="store"
                        , type=str
                        , choices=["albums", "artists", "tracks", "audio-features"]
                        , help="one of albums, artists, tracks, audio-features"
                        , required=True
                        )
    
    parser.add_argument("-a", "--all"
                        , action="store"
                        , type=bool
                        , choices=[True, False]
                        , default=False
                        , help="if it is true, scrape all"
                        , required=False
                        )
    args = parser.parse_args()
    
    scraper = SpotifyScraper()
    scraper.scraper(type_ = args.type, all = args.all)