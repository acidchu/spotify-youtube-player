# spotify-youtube-link

This Python script uses the Firefox browser to automatically search for and play YouTube videos based on the currently playing song on Spotify.

### How It Works
1. The script opens a Firefox browser.
2. Installs addons for Firefox.
3. Loads a configuration file into the YouTube Enhancer addon.
4. Retrieves the name and artist of the currently playing song on Spotify.
5. Searches YouTube for the top 50 results.
6. Parses the results through a complex search algorithm, pushing the one with the highest score to Firefox.
7. Repeats steps 4-6 if the song on Spotify changes.

Below is an example of how the script looks when running:

![Example](https://github.com/acidchu/spotify-youtube-link/blob/main/img.png?raw=true)

### Setup
To set up the script, follow these steps:
1. Go to https://developer.spotify.com/dashboard/.
2. Log in to your Spotify account.
3. Click the "Create an App" button.
4. Give the app a name and description, click "I understand," and then click "Create."
5. Click "Edit Settings."
6. Put http://localhost:8888 in the redirect URL field.
7. Click "Save."
8. Copy your client ID and put it in the first line of `secret.txt`.
9. Click "Show secret," copy your client secret, and put it in the second line of `secret.txt`.
10. Open your editor and run `pip3 install -r requirements.txt`.

Due to YouTube Vanced and its side effects, Google has made all iOS and Android searches slower. To fix this, we need to modify `yt_dlp`:
1. Go to `venv/Lib/site-packages/yt_dlp/extractor/youtube.py`.
2. Find `def _get_requested_clients(self, url, smuggled_data):` and change the defaults to only "web." It should be around line 3624 in version 2024.4.9.
3. Find `for sd in streaming_data: to yield f` and comment out lines 3966 to 3990.

### Changes
Since the last main version, the script has undergone several changes to improve its functionality:

1. The script now uses the `yt_dlp` library to search for YouTube videos instead of the `youtube-dl` library. This change improves search results and makes the script more reliable.
2. Searches go through a more complex algorithm to find the best video. If the video doesn't meet expectations, it will be skipped.
3. The script searches for the video in the background and changes the video only when the next one is found and checked.
4. Caching is now implemented, making it faster and more reliable. The cache is stored in an easy-to-read format for tuning the algorithm.
5. An override file allows manual override of the search results and cache file to ensure the correct song is played or for a casual rickroll.
6. UTF-8 encoding ensures the script can handle all songs and most languages.
7. Language support is implemented. Currently, only English and Japanese are fully supported, but others may work with varying success.
8. The search algorithm is now tunable to ensure the correct song is played. A script for testing and tuning is planned.
9. The script detects if the track is set to loop in Spotify and will loop as well.
10. The script detects if the song is paused and will pause the video as well.
11. Fullscreen playback is now enabled.
12. Audio is set to 1 to ensure playback, preventing Spotify complaints.
13. The looping Spotify audio is now set to a shorter period to be unheard on phones where volume control isn't possible.

### Known Issues
While this script provides convenient automation for playing YouTube videos based on the currently playing song on Spotify, there are a few known issues to keep in mind:

1. The algorithm may not always select the correct video due to similar song names or multiple versions of the same song on YouTube.
2. Explicit songs on YouTube won't play due to age restrictions. An extension to bypass this used to work but doesn't anymore.
3. The script cannot mute phone audio on Spotify.
4. The script may be too fast for older computers. Adding a few sleep statements in the code may help slow down the script and avoid issues.

### Future Plans
While the current version of the script provides a useful set of features, there are some plans to improve it further in the future:

1. Implement multi-threading to make the script even faster and more efficient.
2. Create a web-based GUI that would allow users to log in and control the script from a remote device.
