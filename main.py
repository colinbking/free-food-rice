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

def main():
    url = urlparse(os.getenv("DATABASE_URL"))
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) #connect to heroku postgres
    cur = conn.cursor()

    PATH = "\\Users\\User\\Documents\\Junior\\chromedriver.exe"
    USERNAME = os.getenv('FBNUM') 
    PWD = os.getenv('PWD') 

    url = "https://m.facebook.com/groups/bakercollege"
    fs = FoodScraper(USERNAME, PWD)
    events = (fs.connect_and_scrape(url)) # scrape all events
    
    FoodFinder().update_dict(events) # detect food

    insert_sql = """
        INSERT INTO events(name, about, time, location, food) 
            VALUES %s;
    """
    execute_values(cur, insert_sql, events, "(%(name)s, %(desc)s, %(time)s, %(location)s, %(food)s)") #update our database
    conn.commit()
    
    conn.close()
    # update our calendar automatically with the events
    CalendarUpdater().update_cal()




if __name__ == "__main__":
    main()
    
