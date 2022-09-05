from webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import time

class Bot:
    def __init__(self, start_page_url, gname):
        self.webdriver = WebDriver()
        self.start_page_url = start_page_url
        self.gname = str(gname)
    
    def go_to_start_page(self):
        self.webdriver.open_url(self.start_page_url)
        time.sleep(5)
        
    def refresh(self):
        self.webdriver.refresh()

    def quit(self):
        self.webdriver.quit()

    def querypage(self, cookieframe, cookieaccept, gid, yid, eyid,  startyear, endyear, vid, votes, sid, avgscore, checkbox, radio, search):
        #time.sleep(5)
        self.webdriver.switch_frames(cookieframe, cookieaccept)
        time.sleep(3)
        self.webdriver.scroll_down()
        self.webdriver.waitings()
        self.webdriver.click_list_item(gid, self.gname)
        self.webdriver.fill_in_input_field(yid, str(startyear))
        if endyear != 2022:
            self.webdriver.fill_in_input_field(eyid, str(endyear))
        self.webdriver.fill_in_input_field(vid, str(votes))
        self.webdriver.fill_in_input_field(sid, str(avgscore))
        time.sleep(2)
        for i in checkbox:
            self.webdriver.clickitem(i)
        self.webdriver.clickitem(radio)
        
        self.webdriver.clickitem(search)
        time.sleep(5)
        
    def get_pages(self):
        try:
            return int(str(self.webdriver.find_element_by_x_path("/html/body/div[4]/div[7]/div/div[1]/div/div/div").text).replace(">", "")[-1]) * 100
        except AttributeError:
            return 0
    
    def get_urls(self, ulpath):
        results = self.webdriver.find_element_by_x_path(ulpath)
        options = results.find_elements_by_tag_name("a")
        return [i.get_attribute("href") for i in options]
    
    def get_all_urls(self, ulpath):
        pages = self.get_pages()
        if pages != 0:
            print("getting all pages")
            urllist = self.get_urls(ulpath)
            #pages = min(pages, 400), if its stuck on 400 either use this or use refresh, it bugs out sometimes
            for page in range(100, pages, 100):
                    time.sleep(3)
                    self.webdriver.open_url(f"https://www.musicmeter.nl/album/searchmisc/{page}#results")
                    urllist.extend(self.get_urls(ulpath))
            print("closing bot")
            return urllist
        print("closing bot")
        return self.get_urls(ulpath)
    
    
    def select_item(self, item_name):
        item = self.webdriver.find_element_by_x_path(f'//*[text()="{item_name}"]')
        return self.webdriver.click_on_element(item)

    def select_item_by_x_path(self, item_x_path):
        item = self.webdriver.find_element_by_x_path(item_x_path)
        return self.webdriver.click_on_element(item)
    
    def getname(self, startyear, endyear):
        return f"Musicmeter|{self.gname}|{startyear}-{endyear}"
