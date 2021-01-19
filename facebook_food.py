from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PageLoad import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from urllib.parse import parse_qs
import pickle
import requests
import time
import os
import pandas as pd
import json
import psycopg2
from pprint import pprint as pp
import datetime as dt
from pytz import timezone
import string
# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# cur = conn.cursor()

PATH = "\\Users\\User\\Documents\\Junior\\chromedriver.exe"


class FoodScraper:

    # We need the email and password to access Facebook, and optionally the text in the Url that identifies the "view full post".
    def __init__(self, username, password, post_url_text='… More', driverpath = PATH):
        self.username = username
        self.pwd = password
        self.path = driverpath
        self.headers = {  # This is the important part: Nokia C3 User Agent
            'User-Agent': 'NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+'
        }
        self.session = requests.session()  # Create the session for the next requests
        self.cookies_path = 'session_facebook.cki'  # Give a name to store the session in a cookie file.

        # At certain point, we need find the text in the Url to point the url post, in my case, my Facebook is in
        # English, this is why it says 'Full Story', so, you need to change this for your language.
        # Some translations:
        # - English: 'Full Story'
        # - Spanish: 'Historia completa'
        self.post_url_text = post_url_text

        # Evaluate if NOT exists a cookie file, if NOT exists the we make the Login request to Facebook,
        # else we just load the current cookie to maintain the older session.
        if self.new_session():
            self.login()

        self.posts = []  # Store the scraped posts
    
    def new_session(self):
        if not os.path.exists(self.cookies_path):
            return True

        f = open(self.cookies_path, 'rb')
        cookies = pickle.load(f)
        self.session.cookies = cookies
        return False
        # The first time we login


    def login(self):
        # Get the content of HTML of mobile Login Facebook page
        url_home = "https://m.facebook.com/"
        soup = self.make_request(url_home)
        if soup is None:
            raise Exception("Couldn't load the Login Page")
        
        # Here we need to extract this tokens from the Login Page
        lsd = soup.find("input", {"name": "lsd"}).get("value")
        jazoest = soup.find("input", {"name": "jazoest"}).get("value")
        m_ts = soup.find("input", {"name": "m_ts"}).get("value")
        li = soup.find("input", {"name": "li"}).get("value")
        try_number = soup.find("input", {"name": "try_number"}).get("value")
        unrecognized_tries = soup.find("input", {"name": "unrecognized_tries"}).get("value")

        # This is the url to send the login params to Facebook
        url_login = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
        payload = {
            "lsd": lsd,
            "jazoest": jazoest,
            "m_ts": m_ts,
            "li": li,
            "try_number": try_number,
            "unrecognized_tries": unrecognized_tries,
            "email": self.username,
            "pass": self.pwd,
            "login": "Iniciar sesión",
            "prefill_contact_point": "",
            "prefill_source": "",
            "prefill_type": "",
            "first_prefill_source": "",
            "first_prefill_type": "",
            "had_cp_prefilled": "false",
            "had_password_prefilled": "false",
            "is_smart_lock": "false",
            "_fb_noscript": "true"
        }
        soup = self.make_request(url_login, method='POST', data=payload, is_soup=True)
        if soup is None:
            raise Exception(f"The login request couldn't be made: {url_login}")

        redirect = soup.select_one('a')
        if not redirect:
            raise Exception("Please log in desktop/mobile Facebook and change your password")

        url_redirect = redirect.get('href', '')
        resp = self.make_request(url_redirect)
        if resp is None:
            raise Exception(f"The login request couldn't be made: {url_redirect}")

        # Finally we get the cookies from the session and save it in a file for future usage
        cookies = self.session.cookies
        f = open(self.cookies_path, 'wb')
        pickle.dump(cookies, f)

        return {'code': 200}


      # Utility function to make the requests and convert to soup object if necessary
    def make_request(self, url, method='GET', data=None, is_soup=True):
        if len(url) == 0:
            raise Exception(f'Empty Url')

        if method == 'GET':
            resp = self.session.get(url, headers=self.headers)
        elif method == 'POST':
            resp = self.session.post(url, headers=self.headers, data=data)
        else:
            raise Exception(f'Method [{method}] Not Supported')

        if resp.status_code != 200:
            raise Exception(f'Error [{resp.status_code}] > {url}')

        if is_soup:
            return BeautifulSoup(resp.text, 'lxml')
        print(resp.text)
        return resp.text



    def extract_location(self, driver):    
        try:   
            d = driver.find_element_by_id("event_summary")
            time_and_loc = d.find_elements_by_css_selector('div[class*="fbEventInfo"] > dt')
            time = time_and_loc[0].text
            loc = time_and_loc[1].text
            return (time, loc)
        except Exception as e:
            print("couldnt find event location:", e)
            return None
        # class name contains fbEventInfoText

    def connect_and_scrape(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(self.path, chrome_options=chrome_options)
        # driver = webdriver.Chrome(PATH)
        # driver.ChromeOptions().add_argument('headless');
        # options.add_argument('window-size=1200x600'); // optional

        driver.get("https://m.facebook.com")
        username = driver.find_element_by_id("m_login_email")
        username.send_keys(self.username)
        passentry = driver.find_element_by_id("m_login_password")
        passentry.send_keys(self.pwd)
        sign_in = driver.find_element_by_id("u_0_4")
        sign_in.click()
        all_things = []

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Not Now"))
            )
            element.click()
        except Exception:
            print("fail")

        with PageLoad(driver):
            driver.get(url)


        css_group = '#m_group_stories_container > section[class*="storyStream"] > article'  # Select the posts from a Facebook group
        css_page = '#recent > div > div > div'  # Select the posts from a Facebook page

        posts = []
        to_visit = [] # stores indees into posts array, to update later with event details

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "m_group_stories_container"))
            )

            raw_data = driver.find_elements_by_css_selector(css_group)
            data_copy = list(raw_data)
            for index,post in enumerate(data_copy):
                desc_text = ""
                for words in post.find_elements_by_tag_name("p"):
                    desc_text += words.text
                links = post.find_elements_by_css_selector("p a")
                is_event = False

                # parse header to find event link if it exists
                header = post.find_element_by_css_selector('header h3') # "name" shared a event
                header_links = header.find_elements_by_css_selector('a')
                thing_name, person_name = None, None
                location = None
                time = None
                if len(header_links) > 1:
                    thing_link = header_links[1].get_attribute("href")
                    print("got here again")
                    thing_name = header_links[1].text
                    person_name = header_links[0].text
                    if "event" in header.text:
                        is_event = True
                        driver.execute_script("window.open('" + thing_link +"', 'new_window')")
                        to_visit.append(index)

                whole_thing = {"name" : thing_name, "desc" : desc_text, "event": is_event, "location":location, "time" : time, "food": "", "added_date": str(dt.datetime.now(timezone('US/Central')))[0:11]}
                all_things.append(whole_thing)
            
            # now update the events using the open tabs
            for post_idx in to_visit[::-1]:
                driver.switch_to.window(driver.window_handles[-1]) # the first opened one is at index 1?
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "event_header"))
                    )
                except Exception as e:
                    print("failed to find event header", e)
                time, location = self.extract_location(driver)
                driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
                driver.implicitly_wait(1)
                print("befre:   ", time)
                all_things[post_idx]["time"] = ''.join(c for c in time if c not in {',', ';', ':'})
                print("after;   ", all_things[post_idx]["time"])
                all_things[post_idx]["location"] = location
                
            return(all_things)

        # except block for whole thing
        except Exception as e:
            print(e)

