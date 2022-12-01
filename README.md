# __music_clustering_recommendation__
Recommend musics using clustering (the project in database class)

---

## __Scraping Data__
<br>

### __1) Create an application in Spotify for Developers__
<br>

* Spotify App Dashboard: https://developer.spotify.com/dashboard/login

* App setting guide: https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

<br>

### __2) Download extracted.mpd.slice data and script__
<br>

* ./extracted_data/extracted.mpd.slice.*.json

* ./spotify_api.py

* ./spotify_config.py

* ./spotify_scraper.py

<br>

### __3) Set up your config.ini__
<br>

* run script below to initialize config file

```bash
python spotify_config.py
```

* set up client_id and client_secret in authentication section of config.ini

```ini
[authentication]
client_id = 3a...1c
client_secret = tv...0x
```

<br>

### __4) Run spotify_scraper.py__
<br>

* refer to help option in spotify_scraper.py

```bash
python spotify_scraper.py --type=artists --all=False
```

<br>

---

## __AWS RDS__
<br>

sources: https://www.youtube.com/watch?v=bC-G4OcLr5g

<br>

### __1) Create an RDS instance with MySQL__
<br>

### __2) Make the database public__
<br>

### __3) Install MySQL Work bench and establish a connection__
<br>

&ensp;&ensp; 1) Put the endpoint of the database to hostname
<br>
&ensp;&ensp; 2) Put username and password

### __4) Import Data to table__
<br>

---

## __MySQL Local Server__
<br>

### __1) Create a local instance with MySQL__
<br>

### __2) Modify a config file__
<br>

### __3) Grant privilege to users__
<br>