import os
from facebook_food import *
from food_finder import *
from calendar_update import *
import psycopg2
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv, find_dotenv
from psycopg2.extras import execute_values
from pprint import pprint as pp
import requests

load_dotenv('.env')

class MainFunctionality():

    def __init__(self):
        # Initializing
        url = urlparse(os.getenv("DATABASE_URL"))
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) #connect to heroku postgres
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.PATH = "\\Users\\User\\Documents\\Junior\\chromedriver.exe"
        self.USERNAME = os.getenv('FBNUM') 
        self.PWD = os.getenv('PWD') 

        self.baker_url = "https://m.facebook.com/groups/bakercollege"

    def retrieve_events(self):
        # if not self.open_conn:
        #     self.connect()
        events = []

        with open("last_pulled.txt", 'r+') as f:
            lp_date = f.readline()[0:11] 
            # query db and get events
            retrieve_sql = "SELECT * FROM EVENTS WHERE added_date >= %s"
            self.cur.execute(retrieve_sql, (lp_date,))
            self.conn.commit()
            ans =self.cur.fetchall()
            for row in ans:
                events.append(dict(row)) # list of psycopg2 dictrow objects
            # overwrite local txt file with today as last pulled date
            today = str(dt.datetime.now(timezone('US/Central')))[0:11]
            f.seek(0)
            f.write(today)
            f.truncate()

        return events 


    def scrape_baker(self):
        # finding food on fb
        fs = FoodScraper(self.USERNAME, self.PWD)
        scraped_events = (fs.connect_and_scrape(self.baker_url)) # scrape all events
        count = FoodFinder().update_dict(scraped_events) # detect food

        # updating the db
        insert_sql = """
            INSERT INTO events(name, about, time, location, food, added_date) 
                VALUES %s;
        """
        execute_values(self.cur, insert_sql, scraped_events, "(%(name)s, %(desc)s, %(time)s, %(location)s, %(food)s, %(added_date)s)") #update our database
        
        db_events = self.retrieve_events()

        self.conn.commit()
        self.conn.close()
        print("done scraping")
        return db_events, count

    def cal_update(self, events):
        # update our calendar automatically with the events
        CalendarUpdater().update_cal_all(events)
        print("done cal updating")


    
