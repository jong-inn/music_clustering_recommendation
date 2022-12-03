# pacakges

import os, json

# variables

input_file_path  = "./extracted_data/%s"
output_file_path = "./extracted_data/pre-processed/%s"

audio_features_features = {
    "track_id"         : ["id"],
    "acousticness"     : ["acousticness"],
    "danceability"     : ["danceability"],
    "energy"           : ["energy"],
    "instrumentalness" : ["instrumentalness"],
    "liveness"         : ["liveness"],
    "loudness"         : ["loudness"],
    "mode"             : ["mode"],
    "speechiness"      : ["speechiness"],
    "tempo"            : ["tempo"],
    "time_signature"   : ["time_signature"],
    "valence"          : ["valence"]
}

# functions

def extract_features(sample_value):
    """
    sample_value: dictionary value
    """
    
    # initialize output
    result_dict = {}
    
    # make an output with audio_features_features
    for output_feature, input_feature_list in audio_features_features.items():
        
        tmp = sample_value.copy()
        
        # get value from nested dictionary
        for input_feature in input_feature_list:
            tmp = tmp[input_feature]
        result_dict.update({output_feature: tmp})
    
    return result_dict


def pre_process():
    folder = "audio-features"
    file_list = [f for f in os.listdir(input_file_path % folder) if f.startswith(folder) and f.endswith(".json")]
    file_list.sort()
    
    for file in file_list:
        print(file)
        
        result_list = []
        
        # read a json file
        with open(os.sep.join([input_file_path % folder, file]), "r") as f:
            tmp = json.loads(f.read())
            print("Read JSON file")

        try:
            # extract values for each feature and store them in result_list
            for key, sample_value in tmp.items():
                if sample_value == None:
                    continue
                else:
                    result_list.append(extract_features(sample_value))
                    
        except Exception as e:
            print(e)
        
        finally:
            # write a json file with specific format
            with open(os.sep.join([output_file_path % folder, "pre_processed." + file]), "w", encoding="utf-8") as f:
                f.write(",\n".join(json.dumps(d) for d in result_list) + "\n")
            print("Wrote JSON file")


def get_the_number_of_rows():
    folder = "audio-features"
    file_list = [f for f in os.listdir(output_file_path % folder) if f.startswith("pre_processed") and f.endswith(".json")]
    file_list.sort()
    
    count = 0
    for file in file_list:
        with open(os.sep.join([output_file_path % folder, file]), "r", encoding="utf-8") as f:
            count += len(f.readlines())
            
    print(count)


def pre_processed_df():
    folder = "audio-features"
    target_file_path = os.sep.join([output_file_path % folder, "pre_processed.%s.extracted.mpd.pickle" % folder])
    
    if os.path.isfile(target_file_path):
        return pd.read_pickle(target_file_path)
    
    file_list = [f for f in os.listdir(input_file_path % folder) if f.startswith(folder) and f.endswith(".json")]
    file_list.sort()
    
    result_list = []
    
    try:
        for file in file_list:
            print(file)

            # read a json file
            with open(os.sep.join([input_file_path % folder, file]), "r") as f:
                tmp = json.loads(f.read())
                print("Read JSON file")
                
            # extract values for each feature and store them in result_list
            for key, sample_value in tmp.items():
                if sample_value == None:
                    continue
                else:
                    result_list.append(extract_features(sample_value))
    
    except Exception as e:
        print(e)
    
    finally:
        df = pd.DataFrame(result_list)
        df.to_pickle(os.sep.join([output_file_path % folder, "pre_processed.%s.extracted.mpd.pickle" % folder]))
        
        return df


if __name__ == "__main__":

    # pre_process()
    
    get_the_number_of_rows()