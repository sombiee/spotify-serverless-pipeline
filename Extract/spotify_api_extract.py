# This code is executable on AWS Lambda
# Additional Lambda Layer is required to use spotipy package

# spotify related package
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# python related package
import json
import os
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlists = sp.user_playlists('spotify')
    
    playlist_link = 'https://open.spotify.com/playlist/2DCBk0AdKhUxb2ANXckhMO'
    playlist_URI = playlist_link.split('/')[-1]
    spotify_data = sp.playlist_tracks(playlist_URI)
    
    client = boto3.client('s3')
    filename = 'spotify_raw' + str(datetime.now()) + '.json'
    
    client.put_object(
        Bucket = 'spotify-etl-somi',
        Key = 'raw_data/to_processed/' + filename,
        Body = json.dumps(spotify_data)
        )