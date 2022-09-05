from bot import Bot 
from spot import Spot
from utils import * 
from creds import user_id, token 

sUser = Spot(user_id, token)

def main():
    print(gdict)
    d = get_inputs()
    print("starting bot")
    
    x = Bot(url, gdict.get(d['genre']))
    name = x.getname(d['startyear'], d['endyear'])
    description = set_description(d['topn'], d['startyear'], d['endyear'], d['genre'], d['avgscore'], d['votes'])
    urllist = scrape(x, d['startyear'], d['endyear'], d['avgscore'], d['votes'])
    
    x.quit()
    tlist = get_all_tracks(urllist, d['topn'])
    urilist = get_uri(tlist, sUser) 
    post_songs(urilist, maxsongs, name, description, sUser)
    return "done, check spotify"

if __name__ == "__main__":
    main()