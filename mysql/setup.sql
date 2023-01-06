
-- CREATE DATABASE spotify;
USE spotify;

CREATE TABLE artist (
	artist_id Varchar(22) NOT NULL,
    name Varchar(300),
    genres Varchar(300),
    popularity Int,
    PRIMARY KEY (artist_id)
);

CREATE TABLE album (
	album_id Varchar(22) NOT NULL,
    popularity Int,
    release_date Varchar(20),
    PRIMARY KEY (album_id)
);

CREATE TABLE track (
	track_id Varchar(22) NOT NULL,
    album_id Varchar(22) NOT NULL,
    name Varchar(300),
    duration_ms Int,
    popularity Int,
    PRIMARY KEY (track_id),
    FOREIGN KEY (album_id) REFERENCES album (album_id)
);

CREATE TABLE audio_features (
	pseudo_id Int AUTO_INCREMENT,
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
    PRIMARY KEY (pseudo_id, track_id),
    FOREIGN KEY (track_id) REFERENCES track (track_id)
						   ON DELETE CASCADE
);

CREATE TABLE artist_album (
	artist_id Varchar(22),
    album_id Varchar(22),
    PRIMARY KEY (artist_id, album_id),
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id),
    FOREIGN KEY (album_id) REFERENCES album (album_id)
);

CREATE TABLE artist_track (
	artist_id Varchar(22),
    track_id Varchar(22),
    PRIMARY KEY (artist_id, track_id),
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id),
    FOREIGN KEY (track_id) REFERENCES track (track_id)
);
