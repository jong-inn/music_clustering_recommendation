# packages & path variables

import os
import pandas as pd
from preprocess.spotify_tracks_preprocess import pre_processed_df as p1
from preprocess.spotify_audio_features_preprocess import pre_processed_df as p2

pickle_path = "./sampled_data/sampled_data_200000.pickle"

sample_ids = pd.read_pickle(pickle_path)
print(sample_ids.head())
print(sample_ids.track_id.nunique())

tracks = p1()
print(tracks.head())

audio_features = p2()
print(audio_features.head())
