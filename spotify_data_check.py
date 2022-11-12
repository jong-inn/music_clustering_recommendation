"""

"""

import glob
import json
from collections import Counter

extracted_path = "./extracted_data"


value_length_counter = Counter()
tracks_17_keys = set()
tracks_18_keys = set()
tracks_19_keys = set()

for sub_path in ["tracks", "audio-features"]:
    for path in sorted(glob.glob(extracted_path + f"/{sub_path}/*.json")):
        
        with open(path, "r") as f:
            tmp = json.loads(f.read())
            
        for k, v in tmp.items():
            if v != None:
                value_length_counter.update({sub_path + f"_{len(v)}": 1})
                
                if (sub_path == "tracks") and (len(v) == 17):
                    tracks_17_keys.add(tuple(v.keys()))
                elif (sub_path == "tracks") and len(v) == 18:
                    tracks_18_keys.add(tuple(v.keys()))
                elif (sub_path == "tracks") and len(v) == 19:
                    tracks_19_keys.add(tuple(v.keys()))
            else:
                value_length_counter.update({sub_path + "_0": 1})
                

# keys in response aren't same. We have to investigate more.

print(value_length_counter)
print(tracks_17_keys)
print(tracks_18_keys)
print(tracks_19_keys)