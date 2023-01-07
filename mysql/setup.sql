
-- CREATE DATABASE spotify;
USE spotify;

-- DROP TABLE artist_album;
-- DROP TABLE artist_track;
-- DROP TABLE track;
-- DROP TABLE audio_features;
-- DROP TABLE album;
-- DROP TABLE artist;

CREATE TABLE artist (
    artist_id Varchar(22) NOT NULL,
    name Varchar(500),
    genres Varchar(500),
    popularity Int,
    PRIMARY KEY (artist_id)
);

CREATE TABLE album (
    album_id Varchar(22) NOT NULL,
    popularity Int,
    release_date Varchar(22),
    PRIMARY KEY (album_id)
);

CREATE TABLE track (
    track_id Varchar(22) NOT NULL,
    album_id Varchar(22) NOT NULL,
    name Varchar(500),
    duration_ms Int,
    popularity Int,
    PRIMARY KEY (track_id)
);

CREATE TABLE audio_features (
    pseudo_id Int,
    tempo Float,
    valence Float,
    danceablitiy Float,
    acousticness Float,
    energy Float,
    instrumentalness Float,
    liveness Float,
    loudness Float,
    speechiness Float,
    track_id Varchar(22),
    PRIMARY KEY (pseudo_id, track_id)
);

CREATE TABLE artist_album (
	artist_id Varchar(22),
    album_id Varchar(22),
    PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE artist_track (
	artist_id Varchar(22),
    track_id Varchar(22),
    PRIMARY KEY (artist_id, track_id)
);

-- after importing data add constraints

ALTER TABLE track
ADD CONSTRAINT FOREIGN KEY (album_id) REFERENCES album (album_id)
;

ALTER TABLE audio_features
ADD CONSTRAINT FOREIGN KEY (track_id) REFERENCES track (track_id) ON DELETE CASCADE
;

ALTER TABLE artist_album
ADD CONSTRAINT FOREIGN KEY (artist_id) REFERENCES artist (artist_id),
ADD CONSTRAINT FOREIGN KEY (album_id) REFERENCES album (album_id)
;

ALTER TABLE artist_track
ADD CONSTRAINT FOREIGN KEY (artist_id) REFERENCES artist (artist_id),
ADD CONSTRAINT FOREIGN KEY (track_id) REFERENCES track (track_id)
;