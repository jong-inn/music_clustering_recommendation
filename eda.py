

import os
import json

file_path  = "./extracted_data/%s"

audio_features_min_max = {
    "acousticness": (0.0, 1.0),
    "danceability": (0.0, 1.0),
    "duration_ms" : (None, None),
    "energy"      : (0.0, 1.0),
    "instrumentalness": (1.0, None),
    "liveness": (None, None),
    "loudness": (None, None),
    "mode": (0, 1),
    "speechiness": (0.0, 1.0),
    "tempo": (None, None),
    "time_signature": (3, 7),
    "valence": (0.0, 1.0),
}

#%%


def extract_one_fixed_sample(folder):
    
    assert folder == "tracks" or folder == "audio-features"
    
    file_list = [f for f in os.listdir(file_path % folder) if f.startswith(folder) and f.endswith(".json")]
    file_list.sort()
    
    with open(os.sep.join([file_path % folder, file_list[-1]]), "r") as f:
        
        tmp = json.loads(f.read())
        
    print(f"length: {len(tmp)}")
    print(f"type  : {type(tmp)}")
    print(f"file  : {file_list[-1]}")
    print(f"""first sample:
                    {next(iter(tmp.values()))}""")

def extract_min_max_sample(file_list, attr, min_max_func, min_max_val=None):
    
    assert min_max_func in [min, max]
    
    folder = "audio-features"
    record = None
    
    for file in file_list:
        with open(os.sep.join([file_path % folder, file]), "r") as f:
            tmp = json.loads(f.read())
            
        for val in tmp.values():
            if record is None:
                record = val[attr]
            else:
                record = min_max_func(record, val[attr])
                
            if min_max_val is not None and min_max_val == record:
                print(f"find min or max value {min_max_val} and return before compeletion: {val['id']}")
                return val["id"]
    
    print(f"find min or max value {record} and return: {val['id']}")
    return val["id"]
                
            
    

def extract_samples_for_audio_features():
    folder = "audio-features"
    file_list = [f for f in os.listdir(file_path % folder) if f.startswith(folder) and f.endswith(".json")]
    file_list.sort()

    audio_features_min_max
    
    for key, val in audio_features_min_max.items():
        print(val[0], val[1])
        extract_min_max_sample(file_list, key, min, val[0])
        extract_min_max_sample(file_list, key, max, val[1])

    # result = extract_min_max_sample(file_list, "acousticness", min, 0)
    
    # return result
    

    
if __name__ == "__main__":
    
    # extract_one_fixed_sample("audio-features")
    # extract_one_fixed_sample("tracks")

    extract_samples_for_audio_features()