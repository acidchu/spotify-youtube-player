import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp
import datetime
import math
from janome.tokenizer import Tokenizer

# = variables ============================================
# Define constants and configuration variables
# ========================================================

number_of_search_results = 20  # Number of YouTube search results to process
max_search_results = 50  # Maximum number of YouTube search results to fetch
similarity_threshold = 0.5  # Threshold for considering text similarity

# = start-up =============================================
# Initial setup and authentication for Spotify and WebDriver
# ========================================================

# Read Spotify client ID and secret from a file
with open("secret.txt", "r") as f:
    id = f.readline().strip()
    secret = f.readline().strip()

# Define Spotify API scope
SCOPE = "user-read-playback-state", "user-read-playback-position", "app-remote-control", "user-modify-playback-state", "user-read-currently-playing", "streaming"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri="http://localhost:8888", scope=SCOPE))

# Initialize WebDriver (Firefox) and install required browser extensions
driver = webdriver.Firefox()
driver.install_addon('extentions/enhancerforyoutube@maximerf.addons.mozilla.org.xpi')
driver.install_addon('extentions/AmbientBlocker.xpi')
driver.install_addon('extentions/simple-youtube-age-restriction-bypass@zerody.one.xpi')
driver.install_addon('extentions/autofullscreen.xpi')
driver.install_addon('extentions/jid1-q4sG8pYhq8KGHs@jetpack.xpi')  # Ad blocker extension

# Switch to the YouTube tab
driver.switch_to.window(driver.window_handles[0])

# Load and apply extension configuration
save = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#import-modal-btn")))
save.click()
conf = open("extentions/EXTENSION_CONFIG.txt", "r+").read()
driver.find_element(By.CSS_SELECTOR, "#import-textarea").send_keys(conf)
save = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#import-btn")))
save.click()

# = main loop ============================================
# Define the main functionality of the program
# ========================================================


def detect_language(text):
    """Detect whether the text is in English or Japanese based on character sets."""
    # Check if the text contains any Japanese characters (Hiragana, Katakana, Kanji)
    for char in text:
        if '\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FAF':
            return "Japanese"
    return "English"


def sentence_similarity(sentence1, sentence2, lang):
    """Calculate the similarity between two sentences based on common words."""
    print(lang)
    try:
        if lang == "Japanese":
            tokenizer = Tokenizer()
            words1 = set(token.surface for token in tokenizer.tokenize(sentence1))
            words2 = set(token.surface for token in tokenizer.tokenize(sentence2))
        else:
            words2 = set(sentence1.encode('utf-8').lower().split())
            words1 = set(sentence2.encode('utf-8').lower().split())

        common_words = words1.intersection(words2)
        if len(words1) == 0:
            return 0  # Prevent division by zero

        if lang == "Japanese":
            return ((len(common_words) / len(words1)) * 100) * 1.5
        else:
            return (len(common_words) / len(words1)) * 100
    except:
        return 0


def link_check(data, video_data):
    print(len(video_data))

    duration = data['time_length'] / 1000
    artist = data['artist']
    print(f"Initial Data: {data}")
    print(f"Initial Video Data: {video_data}")

    for video_info in video_data:
        language = detect_language(video_info['title'])

        title_similarity = sentence_similarity(video_info['title'], data['song'], language)
        channel_similarity = sentence_similarity(video_info['channel'], artist, language)

        similarity_score = (title_similarity + channel_similarity) / 2
        video_info['score'] += similarity_score

        print(
            f"Updated {video_info['title']} - Similarity Score: {similarity_score}, Total Score: {video_info['score']}")
        print(f"URL: {video_info.get('url', 'No URL provided')}")

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Scores after similarity check:")
    for x in video_data:
        print(f"Title: {x['title']}, Score: {x['score']}, URL: {x.get('url', 'No URL provided')}")

    try:
        if all(video_info['score'] == 30 for video_info in video_data):
            pass
        else:
            video_data = [item for item in video_data if item['score'] >= 40]

        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        video_data = sorted(video_data, key=lambda x: x['view_count'], reverse=True)
        print("Video data sorted by view count:")
        for x in video_data:
            print(
                f"Title: {x['title']}, View Count: {x['view_count']}, Score: {x['score']}, URL: {x.get('url', 'No URL provided')}")

        print("=-= view count check =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        percentage_additions = [10, 6, 3]
        for i, video_info in enumerate(video_data[:3]):
            if i < len(percentage_additions):
                video_info['score'] += percentage_additions[i]
                print(
                    f"Updated {video_info['title']} with view count addition: {percentage_additions[i]}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= duration check =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        video_data = sorted(video_data, key=lambda x: abs(int(x['duration']) - duration))
        percentage_additions = [6, 4, 2]
        for i, video_info in enumerate(video_data[:3]):
            if i < len(percentage_additions):
                video_info['score'] += percentage_additions[i]
                print(
                    f"Updated {video_info['title']} with duration addition: {percentage_additions[i]}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= title word check modif =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        word_amounts_title = {"official": 12, "music video": 18, "mv": 15, "lyric": 8, 'live': -10,
                              "Official HD Video": 12}
        for video_info in video_data:
            title_lower = video_info['title'].lower()
            for word, amount in word_amounts_title.items():
                video_info['score'] += amount if word in title_lower else -amount
                print(
                    f"Updated {video_info['title']} with title word {word}: {amount}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= title word check filter -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        words_to_check = ["歌ってみた", "sped up", "fan-made", "acoustic ver", "remix", "cover", "live",
                          "slowed and reverb", "instrumental", "vocal only", "audio", "Instrument"]
        original_search = data.get('song', '').lower()
        video_data = [
            video_info for video_info in video_data
            if all(word not in video_info['title'].lower() or word in original_search for word in words_to_check)
        ]

        print("=-= artist name in channel =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        word_amounts_channel = {artist.lower(): 20}
        for video_info in video_data:
            channel = video_info['channel'].lower()
            for word, amount in word_amounts_channel.items():
                video_info['score'] += amount if word in channel else 0
                print(
                    f"Updated {video_info['title']} with channel word {word}: {amount}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= verified =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        verified_channel_modifier = 30
        for video_info in video_data:
            if video_info['channel_is_verified']:
                video_info['score'] += verified_channel_modifier
                print(
                    f"Updated {video_info['title']} with verified channel modifier: {verified_channel_modifier}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= title length similarity -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        for video_info in video_data:
            title_length_similarity = abs(len(video_info['title']) - len(data['song']))
            if title_length_similarity > 0:
                video_info['score'] -= title_length_similarity
                print(
                    f"Updated {video_info['title']} with title length similarity: {title_length_similarity}, New Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")

        print("=-= song length within 40 seconds =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        filtered_videos = []
        for video_info in video_data:
            duration_difference = abs(video_info['duration'] - duration)
            if duration_difference <= 40:
                filtered_videos.append(video_info)
                print(
                    f"Kept {video_info['title']} with duration difference: {duration_difference}, Score: {video_info['score']}, URL: {video_info.get('url', 'No URL provided')}")
        video_data = filtered_videos

        video_data = sorted(video_data, key=lambda x: x['score'], reverse=True)
        print("Final sorted video data by score:")
        for x in video_data:
            print(f"Title: {x['title']}, Score: {x['score']}, URL: {x.get('url', 'No URL provided')}")

        return video_data[0] if video_data else "skip"

    except IndexError as e:
        print("IndexError: " + str(e))
        return "skip"


def search_youtube(data):
    print("=-=-=-=-=-=-=-=-=-=-=-=-=")
    search_query = data['song'] + " " + data['artist']
    print("Searching: ", search_query)

    length = int(data['time_length']) / 60000
    uper_length = math.ceil(length + 0.5)
    lower_length = math.floor(length - 0.5)
    print(str(lower_length) + "-" + str(uper_length))

    ydl_opts = {
        # Options for the YouTube downloader documentation unclear as to what options actually do something
        'skip_download': True,
        'no_warnings': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'default_search': 'ytsearchviewcount',  # Search YouTube for the query string and sort by view count
        'prefer_insecure': True,
        # 'max_threads': 1,
        'extract_flat': True,
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)  # Create a YouTube downloader object

    # Extract information for the search query
    search_results = ydl.extract_info("ytsearch" + str(max_search_results) + ":" + search_query,
                                      download=False)  # Search for the query

    result_data = []
    for video in search_results['entries']:  # Iterate over search results and print video titles and URLs
        if video is not None and video["url"].startswith("https://www.youtube.com/watch?v="):
            try:
                result_data.append({"title": video['title'], "channel": video['channel'], 'url': video['url'],
                                    'duration': video['duration'], 'view_count': video['view_count'],
                                    'channel_is_verified': video['channel_is_verified'],
                                    "score": 30})  # Add video data to list
            except KeyError as e:
                print("KeyError: ", e)

    result_data = [video for video in result_data if
                   video.get(
                       'duration') is not None]  # Filter out videos with no duration ie shorts and live streams

    print("Result data: ", result_data[0])

    if len(result_data) > number_of_search_results:  # Limit the number of search results
        result_data = result_data[:number_of_search_results]

    data = link_check(data, result_data)  # Check if the video is the right one
    return data


def playback_state():  # get data from spotify

    playback = sp.current_playback()

    print("=-=-=-=-=-=-=-=-=-=-=-=-=")

    current_time_ms = int(round(time.time() * 1000))

    # Get all artists for the track
    artists_ls = playback['item']['artists']

    # Print the names of all artists associated with the track
    artists = ""
    for artist in artists_ls:
        artists += artist['name'] + ", "

    artists = artists[:-2]

    data = {"is_playing": playback['is_playing'], "supports_volume": playback['device']['supports_volume'],
            "volume_percent": playback['device']['volume_percent'], "song": playback['item']['name'],
            "artist": artists, "time_stamp": playback['progress_ms'],
            "time_length": playback['item']['duration_ms'], "time_current": current_time_ms,
            "loop": playback['repeat_state']}

    return data


def load_songs(filename):  # load the overrides from the file
    songs = {}
    with open(filename, 'r', encoding='utf-16') as file:
        for line in file:
            if '=' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    song_info = parts[0].strip()
                    youtube_link = parts[1].strip()
                    duration = convert_to_seconds(parts[2].strip())
                    songs[song_info] = {'url': youtube_link, 'duration': duration}
    return songs


def check_song(song_name, filename):
    songs = load_songs(filename)
    for song_info in songs:  # Check if the song name is in the dictionary
        if song_name in song_info:
            return songs[song_info]
    return None


def cache_song(title, results):  # Cache the song name and youtube link to a file
    try:
        with open('song_cache.txt', 'a', encoding='utf-16') as file:
            duration = convert_seconds_to_minutes(int(results['duration']))
            file.write(title + ' | ' + results['url'] + ' | ' + str(duration) + '\n')
    except Exception as e:
        print("Error: ", e)


def time_get():
    current_time = datetime.datetime.now()
    current_time = int(
        (current_time.hour * 3600) + current_time.minute * 60 + current_time.second)  # Convert time to seconds
    return current_time


def convert_to_seconds(time_str):  # convert time (4:21) to seconds
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        return 0


def convert_seconds_to_minutes(seconds):
    minutes = int(seconds) // 60
    remaining_seconds = int(seconds) % 60
    return f"{minutes}:{remaining_seconds:02}"


class MusicPlayer:
    def __init__(self, sp, driver):
        self.sp = sp
        self.driver = driver
        self.old_song = ""
        self.skip_time = 0
        self.paused = False
        self.duration = 0

    def main(self):
        current_time = time_get()  # Get the current time
        try:
            data = playback_state()  # Get the current playback state from Spotify
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        if data['is_playing']:  # If the song is playing
            if self.paused:  # If the song was paused, play the song
                video = self.driver.find_element(By.TAG_NAME, "video")
                video.send_keys(Keys.SPACE)  # Play the video
            self.paused = False

            new_song = data['song'] + " " + data['artist']  # format the song name
            if new_song != self.old_song:  # If the song has changed
                self.old_song = new_song

                result = check_song(new_song, "overrides.txt")  # Check for a specific song in the overrides file
                if result:  # if song found in file
                    results = result  # need to add a check to get video length
                else:  # if song not found in file
                    result = check_song(new_song, "song_cache.txt")  # Check for a specific song in the cache file
                    if result:  # if song found in file
                        results = result  # need to add a check to get video length
                    else:  # if song not found in file
                        results = search_youtube(data)
                        cache_song(new_song, results)  # cache the song

                if results == "skip":  # if the song is not found
                    self.sp.next_track()
                else:  # if the song is found
                    self.url = results['url']
                    self.driver.get(self.url)  # go to the youtube video

                    img = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".ytp-fullscreen-button")))  # wait and find fullscreen button
                    time.sleep(1)
                    img.click()  # click the fullscreen button

                    self.duration = results['duration']
                    self.skip_time = (int(current_time)) + (self.duration) + 1  # set the time to skip the video


            else:
                self.sp.seek_track(1)  # seek the song to the beginning

                if self.skip_time <= current_time:

                    if data['loop'] == "track":
                        self.skip_time = (int(current_time)) + (self.duration) + 1  # set the time to skip the video

                        self.driver.get(self.url)  # go to the youtube video

                        img = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".ytp-fullscreen-button")))  # wait and find fullscreen button
                        time.sleep(1)
                        img.click()  # click the fullscreen button


                    else:
                        self.sp.next_track()  # skip the song

        else:  # If the song is paused
            if not self.paused:
                video = self.driver.find_element(By.TAG_NAME, "video")
                video.send_keys(Keys.SPACE)  # Play the video
            self.paused = True

    def run(self):
        starttime = time.time()
        data = playback_state()
        self.paused = False
        self.old_song = ""
        if data['supports_volume']:
            self.sp.volume(1)

        while True:
            self.main()  # call main function
            time.sleep(0.5 - ((time.time() - starttime) % 0.5))  # run every second


# Assuming `sp` is the Spotify object and `driver` is the Selenium WebDriver object
player = MusicPlayer(sp, driver)
player.run()
