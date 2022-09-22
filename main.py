import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# = start-up =============================================
#
# ========================================================

id = " "  # client id
secret = " "  # client secret
SCOPE = "ugc-image-upload ", "playlist-modify-private ", "playlist-read-private ", "user-read-private ", "user-read-playback-state ", "user-library-modify ", "user-read-playback-position ", "app-remote-control ", "user-read-recently-played ", "user-modify-playback-state ", "user-read-email ", "user-follow-modify ", "playlist-modify-public ", "user-follow-read ", "user-read-currently-playing ", "playlist-read-collaborative ", "user-library-read ", "streaming ", "user-top-read "

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,  # spotify authentication bullshit
                                               client_secret=secret,
                                               redirect_uri="http://localhost:8888",
                                               scope=SCOPE))

# ========================================================

driver = webdriver.Firefox()  # open firefox
driver.install_addon('extentions/enhancerforyoutube@maximerf.addons.mozilla.org.xpi')  # install the extension
driver.install_addon('extentions/sponsorBlocker@ajay.app.xpi')  # install the extension

driver.get('https://www.youtube.com')  # go to youtube
driver.switch_to.window(driver.window_handles[0])  # switch to the youtube tab


# = main loop ============================================
#
# ========================================================

def full():  # make the video fullscreen
    global fullscreen
    fullscreen = True  # set fullscreen to true
    img = WebDriverWait(driver, 10).until(  # find the fullscreen button
        EC.presence_of_element_located((By.CSS_SELECTOR, ".efyt-control-bar > button:nth-child(9)")))
    img.click()  # click the fullscreen button


def playing(sp):  # main loop
    global to_search_old  # global variables
    global fullscreen
    try:
        playing = sp.currently_playing()  # get the currently playing song data
        song = playing['item']['name']  # get the song name
        artist = playing['item']['artists'][0]['name']  # get the artist name
        to_search = song + " " + artist + " offical music video MV"  # make the search query

        if to_search != to_search_old:  # if the song has changed
            tries = 5  # number of tries to find the search bar and search for the song
            for i in range(tries):  # try x times to find the search bar and search for the song
                try:
                    seach_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  # find the search bar
                                                                                                "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input")))
                    seach_bar.clear()  # clear the search bar
                    seach_bar.send_keys(to_search)  # put text in the search bar
                    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(  # find the search button
                        (By.XPATH, "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button")))
                    button.click() # click the search button
                except KeyError as e:
                    if i < tries - 1:  # if it has errored to many times
                        time.sleep(0.2)
                        continue
                    else:
                        raise
                break
            # time.sleep(1)

            tries = 5  # number of tries to click the first video
            for i in range(tries):
                try:
                    img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  # find the first video
                                                                                          "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a")))
                    img.click()  # click the first video

                    if fullscreen == False:  # if the video is not fullscreen
                        time.sleep(4)
                        full()  # make the video fullscreen

                    to_search_old = to_search  # set the old search to the new search
                except KeyError as e:
                    if i < tries - 1:  # i is zero indexed
                        time.sleep(0.2)
                        continue
                    else:
                        raise
                break
    except:
        pass


fullscreen = False  # is the video fullscreen
to_search_old = ""  # the last song that was searched

starttime = time.time()

pyautogui.press('f11')  # fullscreen youtube

while True:
    playing(sp)  # call main function
    time.sleep(0.5 - ((time.time() - starttime) % 0.5))  # run every second
