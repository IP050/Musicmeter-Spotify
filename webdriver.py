import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

TIMEOUT_THRESHOLD = 15


class WebDriver:
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path=get_chromedriver_path(), options=self.get_options())

    def get_current_url(self):
        return self.driver.current_url

    def open_url(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def waitings(self):
        return self.driver.implicitly_wait(15)

    def find_element_by_x_path(self, element_x_path):
        try:
            return WebDriverWait(self.driver, TIMEOUT_THRESHOLD).until(
                EC.visibility_of_element_located((By.XPATH, element_x_path))
            )
        except TimeoutException:
            logging.warning(
                "Element isn't located yet: {}".format(element_x_path))

    def find_element_by_visible_text(self, element_text):
        case_insensitive_element_x_path = "//*[text()[contains(translate(., '{}', '{}'), '{}')]]" \
            .format(element_text.upper(), element_text.lower(), element_text.lower())
        return self.find_element_by_x_path(case_insensitive_element_x_path)

    def scroll_down(self):
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)

    def switch_frames(self, css_selector, id):
        iframe = self.driver.find_element_by_css_selector(css_selector)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element_by_id(id).click()
        
    def click_on_element(self, element):
        try:
            element.click()
            return True
        except:
            logging.warning("Unable to click on the element")
            return False

    def clear_input_field(self, id):
        input_field = self.driver.find_element_by_id(id)
        try:
            input_field.clear()
            return True
        except:
            logging.warning(
                "Unable to clear the input field: {}".format(id))
            return False
    def clickitem(self, id):
        self.driver.find_element_by_id(id).click()
        
        return "done"
    
    def click_list_item(self,id, text):
        self.driver.find_element_by_id(id).click()
        x = self.find_element_by_visible_text(text)
        x.click()
        return "done"
        
    def fill_in_input_field(self, id, text):
        self.clear_input_field(id)
        input_field = self.driver.find_element_by_id(id)
        try:
            for character in text:
                input_field.send_keys(character)
            return True
        except:
            logging.warning(
                "Unable to fill in the input field: {}".format(id))
            return False

    def quit(self):
        self.driver.quit()

    def get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=nl-BE")
        options.add_argument("start-maximized");
        return options


def get_chromedriver_path():
    current_dir_path = os.path.dirname(__file__)
    chromedriver_path = os.path.join(current_dir_path, "chromedriver")
    # for Windows users
    if os.name == "nt":
        chromedriver_path += ".exe"
    return chromedriver_path
