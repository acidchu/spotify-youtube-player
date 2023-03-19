import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from youtubesearchpython import VideosSearch
import datetime

# = start-up =============================================
#
# ========================================================

with open("secret.txt", "r") as f:  # get the ids
    id = f.readline().strip()
    secret = f.readline().strip()

SCOPE ="user-read-playback-state ", "user-read-playback-position ", "app-remote-control ", "user-modify-playback-state ", "user-read-currently-playing ", "streaming "

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,  # spotify authentication
                                               client_secret=secret,
                                               redirect_uri="http://localhost:8888",
                                               scope=SCOPE))

# ========================================================

driver = webdriver.Firefox()  # open firefox
driver.install_addon('extentions/enhancerforyoutube@maximerf.addons.mozilla.org.xpi')  # install the extension
driver.install_addon('extentions/AmbientBlocker.xpi')  # install the extension
driver.install_addon('extentions/simple-youtube-age-restriction-bypass@zerody.one.xpi')  # install the extension
driver.install_addon('extentions/autofullscreen.xpi')  # install the extension

save = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#import-modal-btn")))  # find the import button
save.click()  # click the import button
driver.switch_to.window(driver.window_handles[0])  # switch to the youtube tab
conf = open("extentions/conf.txt", "r+").read()  # extension config loader # open the config file
driver.find_element(By.CSS_SELECTOR, "#import-textarea").send_keys(conf)  # find the text box and send the config
save = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#import-btn")))  # find the save button
save.click()  # click the save button


# = main loop ============================================
#
# ========================================================


def time_get():
    current_time = datetime.datetime.now()
    current_time = int((current_time.hour * 3600) + current_time.minute * 60 + current_time.second)
    return current_time


def playing(sp):  # main loop
    global to_search_old  # global variables
    global skip_time
    current_time = time_get()
    try:
        if (int(current_time) % 10) == 0:
            sp.seek_track(10)

        playing = sp.currently_playing()  # get the currently playing song data
        song = playing['item']['name']  # get the song name
        artist = playing['item']['artists'][0]['name']  # get the artist name
        to_search = song + " " + artist + " offical music video"  # make the search query

        if to_search != to_search_old:  # if the song has changed
            videosSearch = VideosSearch(to_search, limit=1) # search youtube
            url = videosSearch.result()['result'][0]['link'] # get the video url
            duration = videosSearch.result()['result'][0]['duration'] # get the video duration

            driver.get(url)  # go to the youtube video

            img = WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-fullscreen-button"))) # wait and find fullscreen button
            img.click()  # click the fullscreen button

            duration = duration.split(":")
            skip_time = (int(current_time)) + int(duration[1]) + (int(duration[0]) * 60) + 0  # set the time to skip the video
            to_search_old = to_search  # set the old search to the new search

        if current_time > skip_time:  # if the video is not over
            sp.next_track()

    except:
        pass


to_search_old = ""  # the last song that was searched
starttime = time.time()

try:
    sp.volume(0)  # try to set spotify volume to 0 doesnt work on mobile devices
except:
    pass

while True:
    playing(sp)  # call main function
    time.sleep(0.5 - ((time.time() - starttime) % 0.5))  # run every second

