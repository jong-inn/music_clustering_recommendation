"""
    Get data from Spotify using API
    

"""


import requests
import base64
import json
from urllib.parse import urlencode
from spotify_config import config_read

client_id = config_read(section="authentication", key="client_id")
client_secret = config_read(section="authentication", key="client_secret")
token_endpoint = "https://accounts.spotify.com/api/token"
query_endpoint = "https://api.spotify.com/v1/%s"

class SpotifyAPI:
    
    def __init__(self, client_id=client_id, client_secret=client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def encode_client_creds(self):
        client_creds = f"{self.client_id}:{self.client_secret}"
        self.encoded_client_creds = base64.b64encode(client_creds.encode('utf-8'))
        
    def get_token(self):
        self.encode_client_creds()
        headers = {
            "Authorization": f"Basic {self.encoded_client_creds.decode('ascii')}"
        }
        token_data = {
            "grant_type": "client_credentials"
        }
        
        req = requests.post(token_endpoint, data=token_data, headers=headers)
        print(f"response status code: {req.status_code}")
        
        if req.status_code == 200:
            self.access_token = req.json()['access_token']
            self.expires_in = req.json()['expires_in']
            self.token_type = req.json()['token_type']
        else:
            raise ValueError("token access is denied")

    def get_query_by_search(self, type_, query):
        '''
        type_: artist, album, track
        query: name
        '''
        
        assert type_ in ['artist', 'album', 'track'], "type_ has to be one of 'artist', 'album', and 'track'"
        assert type(query) == str, "query has to be string format"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        query_data = urlencode({
              "q": query
            , "type": type_
        })
        lookup_endpoint = f"{query_endpoint % 'search'}?{query_data}"
        
        req = requests.get(lookup_endpoint, headers=headers)
        
        return self.distinguish_status_code(req)

    def get_query_by_id(self, type_, id_):
        '''
        type_: albums, artists, tracks, audio-features
        id_  : id
        '''
        
        assert type_ in ["albums", "artists", "tracks", "audio-features"], "type_ has to be one of 'artists', 'albums', 'tracks', and 'audio-features'"
        assert type(id_) == str, "id_ has to be string format"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        lookup_endpoint = f"{query_endpoint % type_}/{id_}"
        
        req = requests.get(lookup_endpoint, headers=headers)
        
        return self.distinguish_status_code(req)
    
    def get_query_by_ids(self, type_, ids):
        '''
        type_: albums, artists, tracks, audio-features
        ids  : array of ids
        '''
        
        assert type_ in ["albums", "artists", "tracks", "audio-features"], "type_ has to be one of 'artists', 'albums', 'tracks', and 'audio-features'"
        assert iter(ids), "ids has to be iterable format"
        assert sum(map(lambda x: type(x) == str, ids)) == len(ids), "an element in ids has to be string format"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        query_data = urlencode({
            "ids": ",".join(ids)
        })
        lookup_endpoint = f"{query_endpoint % type_}?{query_data}"
        
        req = requests.get(lookup_endpoint, headers=headers)
        
        return self.distinguish_status_code(req)
        

    def distinguish_status_code(self, request):
        if request.status_code == 200:
            return request.json()
        elif request.status_code == 401:
            raise ValueError("token might be expired")
        elif request.status_code == 403:
            raise ValueError("bad OAuth request")
        elif request.status_code == 429:
            raise ValueError("exceed rate limits")
        else:
            raise ValueError("new error")

if __name__ == '__main__':
    
    spotify = SpotifyAPI(client_id, client_secret)
    spotify.get_token()
    
    print(f"""
        access_token : {spotify.access_token}
        expires_in   : {spotify.expires_in}
        token_type   : {spotify.token_type}  
          """)
    
    # result = spotify.get_query_by_id("tracks", "6QHYEZlm9wyfXfEM1vSu1P")
    result = spotify.get_query_by_id("audio-features", "6QHYEZlm9wyfXfEM1vSu1P")
    
    for k, v in result.items():
        print(f"key: {k}, value: {v}")
