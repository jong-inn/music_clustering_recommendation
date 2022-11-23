-- CREATE DATABASE spotify;

DROP TABLE AudioFeatures;
CREATE TABLE AudioFeatures (
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
    valence Float
);