"""

"""

import csv
import glob
import json
import matplotlib.pyplot as plt
from collections import Counter

extracted_path = "./extracted_data"


value_length_counter = Counter()
tracks_17_keys = set()
tracks_18_keys = set()
tracks_19_keys = set()

def number_of_attributes():
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
                
def write_tracks_popularity():
    with open("./tacks_popularity.csv", "w", encoding="UTF8") as tp:
        writer = csv.writer(tp)
        header = ["key", "popularity"]
        
        writer.writerow(header)
        
        for sub_path in ["tracks"]:
            for path in sorted(glob.glob(extracted_path + f"/{sub_path}/*.json")):
                
                with open(path, "r") as f:
                    tmp = json.loads(f.read())
                
                for k, v in tmp.items():
                    
                    try:
                        writer.writerow([k, v["popularity"]])
                    except Exception as e:
                        print(e, path, k)
    
def read_tracks_popularity():
    with open("./tacks_popularity.csv", "r", encoding="UTF8") as tp:
        reader = csv.reader(tp)
        
        result = []
        for idx, line in enumerate(reader):
            if idx == 0:
                pass
            else:
                result.append(int(line[1]))
            
    return result

def show_histogram(nums):
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(nums, bins=range(0,100,10), density=False)
    plt.savefig('./popularity_histogram.png')

    return counts, bins, patches


if __name__ == "__main__":
    # keys in response aren't same. We have to investigate more.

    number_of_attributes()

    print(value_length_counter)
    print(tracks_17_keys)
    print(tracks_18_keys)
    print(tracks_19_keys)
    
    write_tracks_popularity()
    
    tracks_popularity_list = read_tracks_popularity()
    
    counts, bins, patches = show_histogram(tracks_popularity_list)
    
    print(counts)
    print(bins)