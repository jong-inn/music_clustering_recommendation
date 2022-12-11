# packages & path variables

import os
import pandas as pd


# functions

def preprocess_df(df, key_col):
    # remove white spaces in id columns
    ids_col = [c for c in df.columns if c.endswith("id")]
    
    for col in ids_col:
        df[col] = df[col].replace(" ", "", regex=True)
        
    # drop duplicated rows
    print(f"the number of duplicates by key column: {sum(df.duplicated())}")
    df = df.drop_duplicates(subset=[key_col])
    
    return df
    

def sample_df(source_df, target_col, sampled_ids):
    
    sampled_df = source_df.loc[source_df[target_col].isin(sampled_ids[target_col].unique())].reset_index(drop=True)
    target =  target_col.replace("ids", "").replace("id", "").replace("_", "")
    print(f"sampled_{target} shape: {sampled_df.shape}")
    
    # if the numbers of rows between sampled_ids and sampled_df are not same, stop the whole process
    if sampled_ids[target_col].nunique() != len(sampled_df):
        print(f"""
        the number of unique {target_col} in sample_ids: {sampled_ids[target_col].nunique()}
        the number of rows in sampled_df               : {len(sampled_df)}
        """)
        
        raise NameError("the number of ids doesn't match")
    
    return sampled_df


def create_exploded_df(sampled_df, key_col, target_col):
    
    # create another dataframe for key_col and target_col
    sampled_key_target_df = sampled_df.loc[:, [key_col, target_col]]
    multiple_target_condition = sampled_key_target_df[target_col].str.split(",").str.len() >= 2
    multiple_target_indices = sampled_key_target_df.loc[multiple_target_condition].index
    
    key =  key_col.replace("ids", "").replace("id", "").replace("_", "")
    target =  target_col.replace("ids", "").replace("id", "").replace("_", "")
    
    print(f"""
    the number of rows that have multiple {target}: {len(multiple_target_indices)}
    the number of {target} in sampled_{key}       : {sampled_key_target_df[target_col].str.split(",").str.len().sum()}
    """)
    
    # exploding the rows that have multiple artists
    sampled_key_target_df[target_col] =  sampled_key_target_df[target_col].str.split(",")
    exploded = sampled_key_target_df.explode(target_col)
    duplicated_exploded_indices = exploded.index[exploded.index.duplicated()]

    print(f"""
    shape of {key}_{target} before exploding: {sampled_key_target_df.shape}
    shape of {key}_{target} after exploding : {exploded.shape}
    """)

    print(f"""
    compare artists_id that have multiple artists between original and exploded ones
    original - exploded: {set(multiple_target_indices).difference(set(duplicated_exploded_indices))}
    exploded - original: {set(duplicated_exploded_indices).difference(set(multiple_target_indices))}
    """)
    
    return exploded


def write_csv(output_path, sampled_df, exploded, key_col, target_col):
    
    key =  key_col.replace("ids", "").replace("id", "").replace("_", "")
    target =  target_col.replace("ids", "").replace("id", "").replace("_", "")
    
    sampled_df.to_csv(output_path % f"sampled_{key}.csv", header=False)
    
    if exploded:
        exploded.to_csv(output_path % f"{key}_{target}_ids.csv", header=False)
    
    
def main():
    
    """
    set your variables
    load your dataframes from local storage
    """
    
    ######################### load dataframes #########################
    from preprocess.spotify_tracks_preprocess import pre_processed_df as p1
    from preprocess.spotify_audio_features_preprocess import pre_processed_df as p2

    # load sampled ids, tracks, audio_features
    pickle_path = "./sampled_data/sampled_data_200000.pickle"

    sampled_ids = pd.read_pickle(pickle_path)
    tracks = p1()
    audio_features = p2()
    
    print(f"""
    shape of tracks        : {tracks.shape}
    shape of audio_features: {audio_features.shape}
    """)
    
    sampled_ids = preprocess_df(sampled_ids, "track_id")
    tracks = preprocess_df(tracks, "track_id")
    audio_features = preprocess_df(audio_features, "track_id")
    ####################################################################
    
    ########################## set variables ###########################
    source_df = tracks
    key_col = "track_id"
    target_col = "artists_id"
    sampled_ids = sampled_ids
    output_path = "./sampled_data/%s"
    use_explode = True
    
    # source_df = audio_features
    # key_col = "track_id"
    # target_col = "artists_id"
    # sampled_ids = sampled_ids
    # output_path = "./sampled_data/%s"
    # use_explode = False
    ####################################################################
    
    sampled_df = sample_df(
        source_df=source_df,
        target_col=key_col,
        sampled_ids=sampled_ids
    )
    if use_explode:
        exploded = create_exploded_df(
            sampled_df=sampled_df,
            key_col=key_col,
            target_col=target_col
        )
    
        sampled_df = sampled_df.drop(columns=[target_col])
    else:
        exploded = None
    
    write_csv(
        output_path=output_path,
        sampled_df=sampled_df,
        exploded=exploded,
        key_col=key_col,
        # key_col="audio_features", # only for audio-features
        target_col=target_col
    )
    

if __name__ == "__main__":
    
    main()  
    

# # sampling with track_id
# sampled_tracks = tracks.loc[tracks.track_id.isin(sampled_ids.track_id)].reset_index(drop=True)
# print(f"sampled_tracks shape: {sampled_tracks.shape}")

# # create another dataframe for track_id and artist_id

# tracks_artists = sampled_tracks.loc[:, ["track_id", "artists_id"]]
# multiple_artists_indices = tracks_artists.loc[tracks_artists.artists_id.str.len() > 22].index

# ## the number of rows that have multiple artists
# print(f"""
# the number of rows that have multiple artists: {len(multiple_artists_indices)}
# the number of artists in sampled_tracks      : {tracks_artists.artists_id.str.split(",").str.len().sum()}
# """)

# ## exploding the rows that have multiple artists
# tracks_artists["artists_id"] =  tracks_artists.artists_id.str.split(",")
# exploded = tracks_artists.explode("artists_id")
# duplicated_exploded_indices = exploded.index[exploded.index.duplicated()]

# print(f"""
# shape of tracks_artists before exploding: {tracks_artists.shape}
# shape of tracks_artists after exploding : {exploded.shape}
# """)

# print(f"""
# compare artists_id that have multiple artists between original and exploded ones
# original - exploded: {set(multiple_artists_indices).difference(set(duplicated_exploded_indices))}
# exploded - original: {set(duplicated_exploded_indices).difference(set(multiple_artists_indices))}
# """)