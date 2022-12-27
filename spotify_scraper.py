"""
    Scraping Spotify data using its API
    Store data as json format
    
    Usage:
    
        python spotify_scraper.py [-h] -t {albums,artists,tracks,audio-features} [-a {True,False}]
    e.g:
        python spotify_scraper.py --type=artists
        python spotify_scraper.py -t=tracks -a=True
        python spotify_scraper.py -h
"""


import os
import argparse
import json
import time
from spotify_api import SpotifyAPI

# check whether the root directory exists and make it if it does not exist
path = "./extracted_data"
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

# check whether the sub directories exist and make them if they do not exist
for sub_path in ["/artists", "/albums", "/tracks", "/audio-features"]:
    if os.path.exists(path + sub_path):
        pass
    else:
        os.mkdir(path + sub_path)
        print(f"make a directory called {sub_path}")

# get raw data's lists from the root directory
file_list = [f for f in os.listdir(path) if f.startswith("extracted.mpd.slice.") and f.endswith(".json")]
file_list.sort()
# if there is no raw data, raise value error
if len(file_list) == 0:
    raise ValueError("you have to make source data first")

class SpotifyScraper:
    
    # initialize the instance
    def __init__(self):
        pass
            
    # main scraping function
    def scraper(self, type_, all=False):
        '''
        type_ : string | one of {albums, artists, tracks, audio-features}
        all   : bool   | true if you want to implement scraping no matter what you've got scraped data
        '''
        
        # make a key for extracting data from response (convert hypen into underbar in audio-features)
        response_key = type_.replace("-", "_")
        
        # create an SpotifyAPI instance
        spotify = SpotifyAPI()
        spotify.get_token() # get access token
        
        # scrape data by type_ for each extracted_data file
        for matched_file_path, type_extracted, target_keys in self.extract_targets(type_, all):
            time.sleep(60)
            start_time = time.time()
            print(f"{matched_file_path}")
            
            try:
                # make batches
                for batch_keys in self.make_batches(type_, target_keys):
                    response = spotify.get_query_by_ids(type_, batch_keys)
                    # update the type_extracted dictionary with the result dictionary
                    type_extracted.update(dict(zip(batch_keys, response[response_key])))
                    # time.sleep(10)
            except Exception as e:
                print(e)
            finally:
                # store data in json format
                with open(matched_file_path, "w") as f:
                    f.write(json.dumps(type_extracted))

                end_time = time.time()
                print(f"elapsed time: {round((end_time - start_time) / 60, 2)} mins")
    
    # extract target data by type_
    def extract_targets(self, type_, all=False):
        '''
        type_ : string | one of {albums, artists, tracks, audio-features}
        all   : bool   | true if you want to implement scraping no matter what you've got scraped data
        '''
        
        assert type_ in ["albums", "artists", "tracks", "audio-features"], "type_ has to be one of 'artists', 'albums', 'tracks', and 'audio-features'"
        
        # load extracted_data and type_.extracted_data if it exists for each extracted_data file
        for file in file_list:
            # load extracted.mpd.slice file
            with open(os.sep.join((path, file)), "r") as f:
                extracted = json.loads(f.read())
            
            # load type_.extracted.mpd.slice file
            # if it does not exist, make an empty dictionary
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
    
    # if extracted_data has already type_.extracted_data, find keys that have not scraped
    def extract_different_keys(self, type_, extracted, type_extracted):
        '''
        type_          : string     | one of {albums, artists, tracks, audio-features}
        exctracted     : dictionary | extracted.mpd.slice
        type_extracted : dictionary | type_.extracted.mpd.slice
        '''
        
        # get keys from extracted_data by type_
        if type_ == "albums":
            keys_extracted = set(v["album_uri"] for v in extracted.values())
        elif type_ == "artists":
            keys_extracted = set(v["artist_uri"] for v in extracted.values())
        elif type_ == "tracks":
            keys_extracted = set(extracted.keys())
        elif type_ == "audio-features":
            keys_extracted = set(extracted.keys())

        # if there is a type_.extracted_data, get keys from it and find the difference
        if type_extracted:
            keys_type_extracted = set(type_extracted.keys())
            different_keys = keys_extracted.difference(keys_type_extracted)
            return list(different_keys)
        else:
            return list(keys_extracted)

    # make batches by type_
    def make_batches(self, type_, target_keys):
        '''
        type_          : string | one of {albums, artists, tracks, audio-features}
        target_keys    : list   | targeted keys
        '''
        
        # batch sizes are different by type_
        if type_ == "albums":
            batch_size = 20
        elif type_ == "artists":
            batch_size = 50
        elif type_ == "tracks":
            batch_size = 50
        elif type_ == "audio-features":
            batch_size = 100
        
        # use a generator to export each batch
        for idx in range(0, len(target_keys), batch_size):
            if idx % 20000 == 0:
                print(f"{type_} scraping progress: {round(idx / len(target_keys) * 100, 2)}")
            
            yield target_keys[idx:idx + batch_size]

    
if __name__ == "__main__":
    # use argparse to get arguments in command line
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
    
    # create an instance and implement scraping
    scraper = SpotifyScraper()
    scraper.scraper(type_ = args.type, all = args.all)