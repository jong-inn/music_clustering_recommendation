

USE spotify;


CREATE TABLE temp_total (
	track_id Varchar(22),
    album_id Varchar(22),
    disc_number Int,
    duration_ms Int,
    explicit Bool,
    track_name Varchar(300),
    album_popularity Int,
    track_number Int,
    duration_m Float,
    release_date Varchar(10),
    release_year Int,
    release_year_bin Int,
    acousticness Float,
    danceability Float,
    energy Float,
    instrumentalness Float,
    liveness Float,
    loudness Float,
    mode Int,
    speechiness Float,
    tempo Float,
    time_signature Int,
    valence Float,
    artist_popularity Int,
    genres_combined Varchar(1800),
	artist_name_combined Varchar(300),
    artist_popularity_max Int
);

CREATE TABLE temp_track_artist (
	track_id Varchar(22),
    artist_id Varchar(22),
    artist_name Varchar(100)
);