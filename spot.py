import requests 
import json 


class Spot:
    def __init__(self, user_id, token) -> None:
        self.user_id = user_id
        self.token = token
        
    def get_spotify_uri(self, song_name, artist):
        query = f"https://api.spotify.com/v1/search?q=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=20"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        uri = songs[0]["uri"]
        return uri
    
    def create_playlist(self, name, description):
        request_body = json.dumps({
            "name": name,
            "description": description,
            "public": True
        })
        
        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()
        return response_json['id']
    
    def add_song_to_playlist(self, playlist_id, uri):
        request_body = json.dumps({
            "uris": uri
        })
        
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()
        return response_json
    

