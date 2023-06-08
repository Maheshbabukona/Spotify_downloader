import csv
import requests
from dotenv import load_dotenv
import os
import base64
import json
from youtube_search import YoutubeSearch
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from pytube import YouTube
import re

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    """
    Retrieves the access token required for authentication with the Spotify API.
    """
    authorization_string = client_id + ":" + client_secret
    authorization_bytes = authorization_string.encode("utf-8")
    authorization_base64 = base64.b64encode(authorization_bytes).decode("utf-8")
    url = "https://accounts.spotify.com/api/token"

    # Set headers and data for the token request
    headers = {
        "Authorization": "Basic " + authorization_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Send a POST request to the Spotify Accounts service to obtain the token
    response = requests.post(url, headers=headers, data=data)
    json_result = response.json()
    token = json_result["access_token"]
    return token


def get_header(token):
    """
    Generates the header with the access token for making authenticated requests to the Spotify API.
    """
    return {"Authorization": "Bearer " + token}


def get_playlist_id(playlist_url, token):
    """
    Retrieves the playlist ID from a given Spotify playlist URL.
    """
    playlist_id = None
    playlist_regex = r"playlist\/([a-zA-Z0-9]+)"
    match = re.search(playlist_regex, playlist_url)
    if match:
        playlist_id = match.group(1)

    if playlist_id is None:
        print("Invalid playlist URL.")
        return None

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_header(token)

    # Send a GET request to the Spotify API to get the playlist details
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_result = response.json()
        playlist_name = json_result.get("name")
        return playlist_id, playlist_name
    else:
        print("Playlist not found.")
        return None, None


def search_spotify(query, search_type, token):
    """
    Searches Spotify for a given query and returns the top 3 matches based on the search type.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    params = {"q": query, "type": search_type, "limit": 3}

    # Send a GET request to the Spotify API to search for the query
    response = requests.get(url, headers=headers, params=params)
    json_result = response.json()

    if search_type == "playlist":
        playlists = json_result["playlists"]["items"]
        if playlists:
            for i, playlist in enumerate(playlists, 1):
                print(f"{i}. {playlist['name']} by {playlist['owner']['display_name']}")
        else:
            print("No matching playlists found.")
        return playlists

    else:
        print("Invalid search type.")
        return None


def download_song(url, output_path):
    """
    Downloads a song from the provided YouTube URL and saves it to the specified output path.
    """
    try:
        youtube = YouTube(url)
        video = youtube.streams.filter(only_audio=True).first()
        video.download(output_path=output_path)
    except Exception as e:
        print(f"Error downloading song: {e}")


def search_youtube(query):
    """
    Searches YouTube for a given query and returns the URL of the top search result.
    """
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        video_id = results[0]["id"]
        url = "https://www.youtube.com/watch?v=" + video_id
        return url
    else:
        return None


def download_songs_from_playlist(playlist_id, playlist_name, token, output_directory):
    """
    Downloads all the songs from the specified Spotify playlist.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_header(token)
    params = {"limit": 100}  # Maximum limit per request is 100

    print(f"Downloading songs from playlist: {playlist_name}")

    # Use pagination to retrieve all the tracks in the playlist
    while url:
        # Send a GET request to the Spotify API to get a batch of tracks from the playlist
        response = requests.get(url, headers=headers, params=params)
        json_result = response.json()

        for item in json_result["items"]:
            track = item["track"]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            query = f"{track_name} {artist_name} audio"
            url = search_youtube(query)
            if url:
                download_path = os.path.join(output_directory, f"{track_name}.mp3")
                download_song(url, download_path)
                print(f"Downloaded: {track_name} by {artist_name}")
            else:
                print(f"Song not found: {track_name} by {artist_name}")

        url = json_result["next"]  # Fetch the next set of tracks


def main():
    """
    Main function that orchestrates the retrieval of playlist tracks and downloads them.
    """
    token = get_token()
    playlist_input = input("Enter the playlist name or URL: ")

    playlist_id = None
    playlist_name = None

    if "spotify.com/playlist/" in playlist_input:
        playlist_id, playlist_name = get_playlist_id(playlist_input, token)
    else:
        playlists = search_spotify(playlist_input, "playlist", token)
        if playlists:
            selection = input("Enter the index of the playlist you want to download: ")
            try:
                selection_index = int(selection) - 1
                selected_playlist = playlists[selection_index]
                playlist_id = selected_playlist["id"]
                playlist_name = selected_playlist["name"]
            except (ValueError, IndexError):
                print("Invalid selection.")

    if playlist_id:
        output_directory = "downloads"
        os.makedirs(output_directory, exist_ok=True)
        download_songs_from_playlist(playlist_id, playlist_name, token, output_directory)
        print("Songs downloaded successfully!")


if __name__ == "__main__":
    main()
