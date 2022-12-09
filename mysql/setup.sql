-- CREATE DATABASE spotify;

-- DROP TABLE AudioFeatures;
CREATE TABLE AudioFeatures (
    track_id Varchar(24),
	acousticness Float,
    danceability Float,
    duration_ms Int,
    energy Float,
    instrumentalness Float,
    liveness Float,
    loudness Float,
    mode Int,
    speechiness Float,
    tempo Float,
    time_signature Int,
    valence Float,
    PRIMARY KEY (track_id)
);

-- DROP TABLE Tracks;
CREATE TABLE Tracks (
    track_id Varchar(24),
    album_id Varchar(24),
    artists_id Varchar(24),
    disc_number Int,
    duration_ms Int,
    explicit Boolean,
    name Varchar(80),
    popularity Int,
    track_number Int,
    PRIMARY KEY (track_id)
);

-- DROP TABLE Artists;
CREATE TABLE Artists (
    artist_id Varchar(24),
    PRIMARY KEY (artist_id)
);

-- DROP TABLE Albums;
CREATE TABLE Albums (
    album_id Varchar(24),
    PRIMARY KEY (album_id)
)