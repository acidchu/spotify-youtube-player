# spotify-youtube-link
This is a bit of code that lets you control a firefox browser with youtube open using spotify localy or remotely

### How it works
1. It opens a firefox broswer
2. Installs 2 addons for firefox
3. It grabs whatever you are playing on spotify grabs the name and artist of the song puts them together
4. Puts that search result into the search bar and clicks search
5. Clicks the first video result
6. Fullscreens if it hasnt alredy
7. Repeat step 3 - 5 if the song on spotify changes

below is an example of how it looks when running
![Example](https://github.com/acidchu/spotify-youtube-link/blob/main/img.png?raw=true)



### setup
1. go to https://developer.spotify.com/dashboard/
2. login to your spotify account 
3. click the create an app button
4. give it a name and decription click i understand and then click create
5. click edit settings
6. put http://localhost:8888 in the redirect url
7. click save
8. copy your client id and put it in the client id variable in the code
9. click show secret copy your client secret and put it in the client secret variable in the code
10. open your editor and insall all requrements
11. run

