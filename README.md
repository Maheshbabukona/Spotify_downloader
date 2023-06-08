# Spotify_downloader
Spotify Playlist Downloader is a Python script that allows users to download songs from Spotify playlists by searching and downloading from YouTube

This Python script allows users to download songs from Spotify playlists. It utilizes the Spotify API to search for playlists and retrieve their tracks. Users can either provide the name or URL of a playlist. The script presents the top 3 matches based on the user's input and allows them to select a playlist for downloading.

Features:
- Authenticates with the Spotify API using client credentials
- Searches Spotify for playlists based on user input
- Retrieves the tracks from the selected playlist
- Searches YouTube for the corresponding audio of each track
- Downloads the songs in MP3 format from YouTube

Usage:
1. Obtain the required credentials from the Spotify Developer Dashboard and set them as environment variables.
2. Run the script and enter the playlist name or URL when prompted.
3. If multiple playlists match the input, choose the desired playlist from the presented options.
4. The script will display the playlist name and start downloading the songs from YouTube.
5. The downloaded songs will be saved in a "downloads" directory in the current working directory.

Note: Ensure you comply with the terms of use and copyright laws when using this script to download songs.

Dependencies:
- requests
- dotenv
- base64
- json
- youtube_search
- bs4
- youtubesearchpython
- pytube

Feel free to contribute, report issues, or suggest improvements by opening an issue or submitting a pull request.

