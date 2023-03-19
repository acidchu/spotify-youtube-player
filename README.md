# spotify-youtube-link
This is a Python script that uses Firefox browser with YouTube and Spotify to automatically search for and play YouTube videos based on the currently playing song on Spotify.

### How it works
1. The script opens a Firefox browser.
2. It installs four addons for Firefox.
3. The script loads a configuration file into the YouTube Enhancer addon.
4. It retrieves the name and artist of the currently playing song on Spotify.
5. The script searches YouTube for the song.
6. It retrieves the first result and opens the URL in the browser.
7. Steps 3-5 are repeated if the song on Spotify changes.

Below is an example of how the script looks when running:

![Example](https://github.com/acidchu/spotify-youtube-link/blob/main/img.png?raw=true)



### setup
To set up the script, follow these steps:
1. Go to https://developer.spotify.com/dashboard/.
2. Log in to your Spotify account.
3. Click the "Create an App" button.
4. Give the app a name and description, click "I understand", and then click "Create".
5. Click "Edit Settings".
6. Put http://localhost:8888 in the redirect URL field.
7. Click "Save".
8. Copy your client id and put it in the first line of secret.txt.
9. Click show secret copy your client secret and put it in the second line of secret.txt.
10. Open your editor and run ```pip3 install -r requirements.txt```.
11. Run the script.

### Changes
Since the original version, the script has undergone several changes to improve its functionality:


1. Added a configuration file.
2. Sped up the code by not waiting for the play button to appear.
3. Made the Spotify keys stored in a text file.
4. Added an age restriction bypass extension.
5. Added a YouTube enhancer configuration so quality is set to 4K or closest automatically.
6. so quality is set to 4k or closest automatically
6. Added auto fullscreen into the browser.
6. Made the scope only what is required and removed extra testing code.
7. Made the fullscreen feature less clunky and slow.
8. Made the song search quicker and in the background so it appears faster.
9. Made the script try to set the volume to 0% on Spotify to avoid hearing it in two places.
10. Made it so the script controls Spotify and not the other way around, i.e., the playback length is based on the YouTube video, not the Spotify one.
11. Made the finding of elements more accurate by using CSS selectors instead of XPaths.

### Known Issues
While this script provides convenient automation for playing YouTube videos based on the currently playing song on Spotify, there are a few known issues to keep in mind:

1. The script does not work if the song on Spotify is not found on YouTube.
2. Sometimes, the script may select the wrong video due to the wrong video appearing first in the search results.
3. The script cannot mute phone audio on Spotify.
4. The script can be too fast for some older computers. In such cases, adding a few sleep statements in the code may help to slow down the script and avoid any issues.

### Future Plans
While the current version of the script provides a useful set of features, there are some plans to improve it further in the future:

1. Implement multi-threading to make the script even faster and more efficient.
2. Create a web-based GUI that would allow users to log in and control the script from a remote device.
3. Improve the search algorithm to make it more accurate, potentially by using keywords to weigh search results and improve the chances of selecting the correct video.

