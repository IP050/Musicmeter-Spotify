### Overview ###
* Uses https://www.musicmeter.nl/album/searchmisc
* Selects the top albums based on rating, number of votes and year-range 
* Gets the artist + top (n) tracks of each album
* Gets the spotify uri for each track
* Creates a (public) playlist with a title+description based on the query
* Adds al tracks in chunks of 100 to the playlist 
* made for fun so use at own risk and don't blame me if it breaks

### Usage ###
1. pip install -r requirements.txt
2. get spotify token; https://developer.spotify.com/console/post-playlists/ > generate token (scope: playlist-modify-public or private, token expires fast but cba to implement auth flow)
3. get spotify username; userid https://www.spotify.com/us/account/overview/ > username
4. run main.py - follow steps 

### oh no my where my driver go ###
* if web/chromedriver doesn't work from path just download and drag .exe in project folder 
