import contextlib
import requests
from bs4 import BeautifulSoup

url = "https://www.musicmeter.nl/album/searchmisc"
ulpath = "/html/body/div[4]/div[7]/div/ul"
altpath = "/html/body/div[4]/div[7]/div/ul"
gid = 'genre-0'
yid = 'year_min-0'
eyid = 'year_max-0'
vid = "votes_min-0"
sid = "average_min-0"
gdict = {1 : "Hip-Hop", 2: "Rock", 3: "Pop", 4: "R&B", 5 : "Blues", 6: 'Funk', 7 : 'Reggae', 8: 'Soul', 9: 'Jazz', 10 : 'Dance', 11 : 'Electronic' }
radio = "sort-1" #use sort-0 for a-z, sort-2 for year
checkbox = ["live-0", "score-0", "ep-0", "various_new-0", "various_old-0"]
search = "qfauto-8"
cookieframe = "#gdpr-consent-notice"
cookieaccept = "save"
maxsongs = 98

def get_inputs():
    genre = int(input("please select a genre:"))
    topn = int(input("please enter the number of songs per artist, press enter for 3:") or 3)
    startyear = str(input("please enter a start year:"))
    endyear = str(input("please enter an end year, press enter for 2022:") or 2022)
    avgscore = float(input("please enter the minimum average score, press enter for 3.75:") or 3.75)
    votes = int(input("please enter the minimum number of votes, press enter for 50:") or 50)
    #token = str(input("please enter your spotify token: https://developer.spotify.com/console/post-playlists/"))
    #userid = str(input("please enter your spotify user id: https://www.spotify.com/us/account/overview/"))
    return dict(genre = genre, topn = topn, startyear = startyear, endyear = endyear, avgscore = avgscore, votes = votes)

def scrape(x, startyear, endyear, avgscore, votes):
    x.go_to_start_page()
    x.querypage(cookieframe, cookieaccept, gid, yid, eyid, startyear, endyear, vid, votes, sid, avgscore, checkbox, radio, search)
    return x.get_all_urls(ulpath)

def get_artist(url):
    r = requests.get(url)
    x = r.text
    arstart = x.find("<title>")
    arend = x.find("</title>")
    a = x[arstart+7:arend]
    artist = a.split(" - ")[0]
    return artist
    
def get_tracks(url, topn):
    r = requests.get(url)
    x = r.content 
    data = BeautifulSoup(x, "html.parser")
    final = data.find("h2", text="Favoriete tracks").find_next_sibling("ul")
    l = [t.text for t in final.find_all("li")]
    return [i.split(" (")[0] for i in l][0:topn]

def get_artist_tracks(url, topn):
    statsurl = f"{url}/stats"
    artist = get_artist(url)
    tracks = get_tracks(statsurl, topn)
    return [{'artist': artist, 'track': i} for i in tracks]

def get_all_tracks(urllist, topn):
    print("getting tracks")
    x = []
    for i in urllist:
        with contextlib.suppress(AttributeError):
            x.append(get_artist_tracks(i, topn))
    z = []
    for i in x:
        z.extend(iter(i))
    return z

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def set_description(topn, startyear, endyear, genre, avgscore, votes):
    if topn == 1:
                return f"Top song(most votes) per album from {startyear} to {endyear} in genre {gdict.get(genre)}, according to Musicmeter (sorted on (album)rating; min score of {avgscore} out of 5 + min {votes} votes)"
    else:
        return f"Top {topn} songs(most votes) per album from {startyear} to {endyear} in genre {gdict.get(genre)}, according to Musicmeter (sorted on (album)rating; min score of {avgscore} out of 5 + min {votes} votes)"

def post_songs(l, n, name, description, sclient):
    print("posting songs")
    x = sclient.create_playlist(name, description)
    for i in chunks(l, n):
        sclient.add_song_to_playlist(x, i)


def get_uri(tlist, sclient):
    urilist = []
    print("getting uri's")
    for x in tlist:
        with contextlib.suppress(KeyError, IndexError, TypeError):
            urilist.append(sclient.get_spotify_uri(x['track'], x['artist']))
    return urilist

def post_songs(l, n, name, description, sclient):
    print("posting songs")
    x = sclient.create_playlist(name, description)
    for i in chunks(l, n):
        sclient.add_song_to_playlist(x, i)
