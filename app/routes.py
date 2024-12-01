from flask import Blueprint, current_app, render_template, request, redirect, session, jsonify, url_for
from .services import get_spotify_token, search_song
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

main = Blueprint('main', __name__)

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

SCOPES = "user-read-private user-read-email"

# Cambiar por tu ruta de producción
REDIRECT_URI = "http://127.0.0.1:5000/callback" # LOCAL 

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    """Redirect to Spotify's OAuth 2.0 endpoint."""
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode({'client_id': current_app.config['CLIENT_ID'], 'response_type': 'code', 'redirect_uri': REDIRECT_URI, 'scope': SCOPES})}"
    return redirect(auth_url)

@main.route('/callback')
def callback():
    """Handle Spotify's redirect after login."""
    code = request.args.get('code')
    if not code:
        return "Error: No code provided", 400

    # Exchange the authorization code for an access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": current_app.config['CLIENT_ID'],
        "client_secret": current_app.config['CLIENT_SECRET']
    }
    token_response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    token_response_data = token_response.json()

    # Store the access token in session
    session['access_token'] = token_response_data['access_token']

    return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
    """Fetch the user's profile using the access token."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('main.login'))

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me", headers=headers)

    if response.status_code == 200:
        profile_data = response.json()
        return render_template('profile.html', profile=profile_data)
    else:
        return "Error: Unable to fetch profile data", 500

@main.route('/get_profile')
def get_profile():
    """Fetch the user's profile as JSON for the frontend."""
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({"logged_in": False})

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me", headers=headers)

    if response.status_code == 200:
        profile_data = response.json()
        return jsonify({"logged_in": True, "profile": profile_data})
    else:
        return jsonify({"logged_in": False})

@main.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    token = get_spotify_token()
    results = search_song(query, token)
    tracks = []
    for item in results['tracks']['items']:
        tracks.append({
            'artist': item['artists'][0]['name'],
            'name': item['name'],
            'image': item['album']['images'][0]['url'],
            'url': item['external_urls']['spotify']
        })
    return jsonify(tracks)

@main.route('/logout')
def logout():
    """Clear the session and redirect to the homepage."""
    session.clear()
    return redirect(url_for('main.index'))

@main.route('/track/<track_id>', methods=['GET'])
def get_track(track_id):
    token = get_spotify_token()
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        track_data = response.json()
        track_info = {
            'artist': track_data['artists'][0]['name'],
            'name': track_data['name'],
            'image': track_data['album']['images'][0]['url'],
            'url': track_data['external_urls']['spotify']
        }
        return jsonify(track_info)
    else:
        return jsonify({'error': 'Track not found'}), 404