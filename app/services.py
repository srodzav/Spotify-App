import requests
from requests.auth import HTTPBasicAuth
from flask import current_app

def get_spotify_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    auth = HTTPBasicAuth(current_app.config['CLIENT_ID'], current_app.config['CLIENT_SECRET'])
    response = requests.post(url, headers=headers, data=data, auth=auth)
    return response.json()['access_token']

def search_song(query, token):
    url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=15'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()
